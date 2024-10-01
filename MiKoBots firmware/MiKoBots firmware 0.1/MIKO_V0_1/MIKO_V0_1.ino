// FIRMWARE for the robot
// Version 0.1  

#define DEVICE "IO" // DEVICE is ROBOT or IO

#define MAX_NUMBER_OF_JOINTS 6
#include <math.h>
#include <ESP32Servo.h>

int NUMBER_OF_JOINTS = 6;

float DHparams[6][4];
float TOOL_FRAME[6];
int KinematicError = 0;
int error = 0;

char alphabet[] = {
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
};
char Axis_name[] = {'X', 'Y', 'Z', 'y', 'p', 'r'};
char Joint_name[] = {'J1', 'J2', 'J3', 'J4', 'J5','J6'};

String Joint_name_string[] = {"J1", "J2", "J3", "J4", "J5","J6"};


// structure of the Joint information
typedef struct{
  float StepPerDeg;
  int PosLimitSwitch;
  int HomingOrder;
  int HomingPos;
  int DirJoint;
  int MinPos;
  int MaxPos;
  int MaxSpeed;
  int MaxAccel;
} jointInfo;
jointInfo JointsInfo[MAX_NUMBER_OF_JOINTS];

// structure of motors
typedef struct {
  int step_pin;
  int dir_pin;
  int limit_switch_pin;
} Motor;
Motor motors[MAX_NUMBER_OF_JOINTS];

// structure positions
typedef struct{
  float PosStart; // XYZUVW
  double PosEnd; // XYZUVW
  float PosDelta; 
  float PosJStart; // J1 J2 J3 J4 J5 J6
  double PosJEnd; // J1 J2 J3 J4 J5 J6
  long PosJDelta;
} robot_struct;
robot_struct robot[MAX_NUMBER_OF_JOINTS];

// variables tools
int tool_pin; 
int tool_type;
int servo_min;
int servo_max;

int tool_pos; 

Servo servoTool;


// Variables io
int io_pin[10]; 
int io_type[10];
int io_state[10];

String serialBuffer;

void readSerialInput();
void executeCommands();
void sendPos();
void ForwardKinematic_6_PosEnd();
void ForwardKinematic_3_PosEnd();

TaskHandle_t Task1;
TaskHandle_t Task2;
SemaphoreHandle_t mutex;
SemaphoreHandle_t stopSemaphore;

int stop = 0;
int pauze = 0;

//#include <Servo.h>
#include "Variables.h"
#include "Motor_move.h"
#include "Kinematics_6.h"
#include "Kinematics_3.h"
#include "error.h"
#include <Arduino.h>
#include <TaskScheduler.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  
  for(int i = 0; i < MAX_NUMBER_OF_JOINTS; i++){
    robot[i].PosJStart = 0.01;
  }

  mutex = xSemaphoreCreateMutex();
  if (mutex == NULL) {
    // Mutex creation failed, handle the error
    Serial.println("Mutex creation failed!");
    while (1); // Halts the program
  }

  stopSemaphore = xSemaphoreCreateBinary();
  if (stopSemaphore == NULL) {
    // Semaphore creation failed, handle the error
    Serial.println("Semaphore creation failed!");
    while (1); // Halts the program
  }

  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
                    Task1code,   /* Task function. */
                    "Task1",     /* name of task. */
                    6000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task1,      /* Task handle to keep track of created task */
                    0);          /* pin task to core 0 */                  
  delay(300); 

  //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  xTaskCreatePinnedToCore(
                    Task2code,   /* Task function. */
                    "Task2",     /* name of task. */
                    8000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task2,      /* Task handle to keep track of created task */
                    1);          /* pin task to core 1 */
  delay(300);

  Serial.println("");
}


void loop() {
  // Empty loop since most of the work is done in tasks
  //taskScheduler.execute();
}


const int BUFFER_SIZE = 5;
String lines[BUFFER_SIZE];

volatile int lineIndex = 0;

const int MAX_BUFFER_SIZE = 256; // Adjust size according to your requirements
char buffer[MAX_BUFFER_SIZE]; // Character array to hold serial input

void Task1code(void * pvParameters) {
  while (true) {
    while (Serial.available() > 0) {
      char c = Serial.read();
      if (c == '\n') {
        String str(buffer);
        if (str == "stop") {
          stop = 1;  
        }
        else if (str == "pauze"){
          Serial.println("pauze");
          pauze = 1;
        } 
        else if (str == "play"){
          stop = 0;
          pauze = 0;
          Serial.println("END");
        }
        else if (str == "CONNECT"){
          Serial.print(DEVICE);
          Serial.println("_CONNECTED");
        }
        else if (str != "stop" and str != "pauze" and str != "play" and str != "") {
          // Store the line in the buffer
          if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE){
            if (lineIndex < BUFFER_SIZE) {
              lines[lineIndex] = str;
              lineIndex = (lineIndex + 1); //% BUFFER_SIZE; // Wrap around if the buffer is full
            }

            else{
               Serial.println("Error: Buffer overflow");
            }

            if (lineIndex > BUFFER_SIZE - 2 ){
              Serial.println("wait");
            }

            xSemaphoreGive(mutex);
          }
        }

        memset(buffer, 0, sizeof(buffer));
      } else {
        strncat(buffer, &c, 1);
      }
    }

    // check for signals from inputs
    for(int i = 0; i < 10; i++){
      if(io_type[i] == 1){
        if (!digitalRead(io_pin[i]) and io_state[i] == 0){
          Serial.print("Input ");
          Serial.print(i);
          Serial.print(" ");
          Serial.println(1);
          io_state[i] = 1;
        }
        if (digitalRead(io_pin[i]) and io_state[i] == 1){
          Serial.print("Input ");
          Serial.print(i);
          Serial.print(" ");
          Serial.println(0);
          io_state[i] = 0;          
        }
      }
    }

    delay(2);
  }
}

String command;
String coordinates;
void Task2code(void * pvParameters) {
  while (true) {
    while (stop == 0){
      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE){
        if (lines[0] == ""){
          xSemaphoreGive(mutex);
          break;
        }
        command = lines[0];
        xSemaphoreGive(mutex);
      }

      int spaceIndex = command.indexOf(' ');
      String typeOfCommand = command.substring(0, spaceIndex);
      coordinates = command.substring(spaceIndex + 1);

      // Commands
      if (DEVICE == "ROBOT" and typeOfCommand == "MoveL") MoveL();
      else if (DEVICE == "ROBOT" and typeOfCommand == "MoveJ") MoveJ();
      else if (DEVICE == "ROBOT" and typeOfCommand == "jogL") jogL();
      else if (DEVICE == "ROBOT" and typeOfCommand == "jogJ") jogJ();
      else if (DEVICE == "ROBOT" and typeOfCommand == "OffsetJ") offsetJ();
      else if (DEVICE == "ROBOT" and typeOfCommand == "OffsetL") offsetL();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Home") home_Joints();

      // commands tool
      else if (typeOfCommand == "Tool_move_to") tool_move_to();
      else if (typeOfCommand == "Tool_state") tool_state();  

      // commands IO
      else if (typeOfCommand == "IO_digitalWrite") IO_digitalWrite();

      // Settings robot
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_number_of_joints") set_number_of_joints();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_motor_pin") set_motor_pin();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_switch_pin") set_switch_pin();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_max_pos") set_max_pos();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_lim_pos") set_lim_pos();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_step_deg") set_step_deg();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_dir_joints") set_direction_joint();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_dh_par") set_dh_par();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_speed") set_speed();
      else if (DEVICE == "ROBOT" and typeOfCommand == "Set_home_settings") set_homing();

      // Settings Tool
      else if (typeOfCommand == "Set_tools") set_TOOL();
      else if (typeOfCommand == "Set_tool_frame") set_tool_frame();

      // Settings IO
      else if (typeOfCommand == "Set_IO_pin") set_IO_pin();

      // If the command does not match send END
      else{
        Serial.print("Error< do not regonize this command: ");
        Serial.println(typeOfCommand);
        Serial.println("END");
      }
    

      if ((xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE) and (command != "")){
        for (int i = 0; i < BUFFER_SIZE - 1; i++) {
          lines[i] = lines[i+1];
        }      

        lines[BUFFER_SIZE - 1] = ""; // Clear the last line'
        lineIndex--;

        if(lineIndex < BUFFER_SIZE - 1){
          Serial.println("go");
        } 
        xSemaphoreGive(mutex);
      }

    }
    if (stop == 1){

      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE){
        for (int i = 0; i < BUFFER_SIZE; i++) {
          lines[i] = "";
        } 

        lineIndex = 0; // Wrap around if the buffer is full
        xSemaphoreGive(mutex);
      }
    }
    delay(5);
  }
  delay(5);
}


float read_String(char code, float val) {
  unsigned int startPos = 0;  // Start at the beginning of the buffer
  while (startPos >= 0 && startPos < coordinates.length()) {
    int foundPos = coordinates.indexOf(code, startPos); // Find the position of the code
    if (foundPos >= 0) {
      // If you find the code, extract the digits that follow into a float and return it
      String numberStr = coordinates.substring(foundPos + 1, coordinates.indexOf(' ', foundPos));
      return numberStr.toFloat();
    }
    startPos = coordinates.indexOf(' ', startPos) + 1; // Take a step to the letter after the next space
  }
  return val; // End reached, nothing found, return the default value
}

//// settings update
void set_number_of_joints(){
  int pos = command.indexOf('A');

  NUMBER_OF_JOINTS = command.substring(pos + 1).toInt();

  Serial.println("Number of joints are set");
  Serial.println("END"); 
}

void set_motor_pin(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS * 2; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    motors[i].step_pin = command.substring(pos_setting[j] + 1, pos_setting[j + 1]).toInt();
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].dir_pin = command.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toInt();
    } else{
      motors[i].dir_pin = command.substring(pos_setting[j + 1] + 1).toInt();
    }
    j = j + 2;
  }


  for(int i=0; i < NUMBER_OF_JOINTS; i++) {  
    // set the motor pin & scale
    pinMode(motors[i].step_pin,OUTPUT);
    pinMode(motors[i].dir_pin,OUTPUT);
  }

  Serial.println("Motor pins settings are updated");
  Serial.println("END");
}

void set_switch_pin(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }


  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].limit_switch_pin = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      motors[i].limit_switch_pin = command.substring(pos_setting[i] + 1).toInt();
    }
  }

  for(int i=0; i < NUMBER_OF_JOINTS; i++) {  
    pinMode(motors[i].limit_switch_pin,INPUT_PULLUP);
  }

  Serial.println("Switch pins settings are updated");
  Serial.println("END");
}

void set_lim_pos(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      JointsInfo[i].PosLimitSwitch = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      JointsInfo[i].PosLimitSwitch = command.substring(pos_setting[i] + 1).toInt();
    }
  }

  Serial.println("Position limit switch settings are updated");
  Serial.println("END");
}

void set_max_pos(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS * 2; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    JointsInfo[i].MinPos = command.substring(pos_setting[j] + 1, pos_setting[j + 1]).toInt();
    if (i < NUMBER_OF_JOINTS - 1){
      JointsInfo[i].MaxPos = command.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toInt();
    } else{
      JointsInfo[i].MaxPos = command.substring(pos_setting[j + 1] + 1).toInt();
    }
    j = j + 2;
  }

  Serial.println("Position settings are updated");
  Serial.println("END");
}

void set_step_deg(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      JointsInfo[i].StepPerDeg = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      JointsInfo[i].StepPerDeg = command.substring(pos_setting[i] + 1).toInt();
    }
  }

  Serial.println("Steps per degree settings are updated");
  Serial.println("END");
}

void set_direction_joint(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      JointsInfo[i].DirJoint = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      JointsInfo[i].DirJoint = command.substring(pos_setting[i] + 1).toInt();
    }
  }

  Serial.println("Direction of the joints settings are updated");
  Serial.println("END");
}

void set_homing(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS * 2; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    JointsInfo[i].HomingOrder = command.substring(pos_setting[j] + 1, pos_setting[j + 1]).toInt();
    if (i < NUMBER_OF_JOINTS - 1){
      JointsInfo[i].HomingPos = command.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toInt();
    } else{
      JointsInfo[i].HomingPos = command.substring(pos_setting[j + 1] + 1).toInt();
    }
    j = j + 2;
  }

  Serial.println("Homing settings are updated");
  Serial.println("END");
}

void set_dh_par(){
  int pos_setting[24];

  int posA = command.indexOf('A');
  String NEWcommand = command.substring(posA);

  for(int i = 0; i < NUMBER_OF_JOINTS * 4; i++){
    pos_setting[i] = NEWcommand.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    DHparams[i][0] = NEWcommand.substring(pos_setting[j] + 1, pos_setting[j + 1]).toFloat();
    DHparams[i][1] = NEWcommand.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toFloat();
    DHparams[i][2] = NEWcommand.substring(pos_setting[j + 2] + 1, pos_setting[j + 3]).toFloat();

    if (i < NUMBER_OF_JOINTS - 1){
      DHparams[i][3] = NEWcommand.substring(pos_setting[j + 3] + 1, pos_setting[j + 4]).toFloat();
    } else{
      DHparams[i][3] = NEWcommand.substring(pos_setting[j + 3] + 1).toFloat();
    }
    j = j + 4;
  }

  //DECLARE R06 NEG FRAME
  R06_neg_matrix[2][3] = -DHparams[5][2];

  Serial.println("DH parameters settings are updated");
  Serial.println("END");
}

void set_speed(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS * 2; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    JointsInfo[i].MaxSpeed = command.substring(pos_setting[j] + 1, pos_setting[j + 1]).toInt();
    if (i < NUMBER_OF_JOINTS - 1){
      JointsInfo[i].MaxAccel = command.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toInt();
    } else{
      JointsInfo[i].MaxAccel = command.substring(pos_setting[j + 1] + 1).toInt();
    }
    j = j + 2;
  }

  Serial.println("Speed settings are updated");
  Serial.println("END");
}


// Settings Tool
void set_TOOL(){
  /*
    Tool pin
    Relay 0 or 1 
    Servo min
    Servo max
  */

  int pos_1_TOOL = command.indexOf('A');
  int pos_2_TOOL = command.indexOf('B');
  int pos_3_TOOL = command.indexOf('C');
  int pos_4_TOOL = command.indexOf('D');

  tool_pin = command.substring(pos_1_TOOL + 1, pos_2_TOOL).toInt();
  tool_type = command.substring(pos_2_TOOL + 1, pos_3_TOOL).toInt();
  servo_min = command.substring(pos_3_TOOL + 1, pos_4_TOOL).toInt();
  servo_max = command.substring(pos_4_TOOL + 1).toInt();

  if (tool_type == 0) {
    servoTool.attach(tool_pin);
  }

  Serial.println("TOOL is set");
  Serial.println("END");
}

void set_tool_frame(){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      TOOL_FRAME[i] = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      TOOL_FRAME[i] = command.substring(pos_setting[i] + 1).toInt();
    }
  }

  Serial.println("Tool frame is updated");
  Serial.println("END");
}

// Settings IO
void set_IO_pin(){
  int pos_IO_1_PIN = command.indexOf('A');
  int pos_IO_2_PIN = command.indexOf('B');
  int pos_IO_3_PIN = command.indexOf('C');

  int io_number = command.substring(pos_IO_1_PIN + 1, pos_IO_2_PIN).toInt();
  io_pin[io_number] = command.substring(pos_IO_2_PIN + 1, pos_IO_3_PIN).toInt();

  String type = command.substring(pos_IO_3_PIN + 1);

  if (type == "INPUT"){
    pinMode(io_pin[io_number], INPUT_PULLUP);
    io_type[io_number] = 1;
    
  } else if (type == "OUTPUT"){
    pinMode(io_pin[io_number], OUTPUT);
    io_type[io_number] = 0;
  }

  Serial.println("IO pins are set");
  Serial.println("END");
}


// functions Move robot
void home_Joints(){

  /*
    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJStart = 0.01;
    }

    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      Serial.print(i + 1);
      Serial.print(" out of ");
      Serial.println(NUMBER_OF_JOINTS);

      // look for the joint that has to be homed first
      for(int j = 0; j < NUMBER_OF_JOINTS; j++){
        // See if the joint order is the same 
        if(JointsInfo[j].HomingOrder == i + 1){

          Serial.print("Home joint: ");
          Serial.println(JointsInfo[j].HomingOrder);

          moveToLimit(j);
          robot[j].PosJEnd = JointsInfo[j].HomingPos;
          MotorMoveJ(50, 80, 0, 0);
        }
      }
  }

    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJEnd = 0;
    }

    if(NUMBER_OF_JOINTS == 6){
      ForwardKinematic_6_PosEnd();
    }
    if(NUMBER_OF_JOINTS == 3){
      ForwardKinematic_3_PosEnd();
    }
    
  */

  Serial.println("home");
  Serial.println("END");
}

void moveToLimit(int joint){
  
  // set the direction of the joint towards the limit
  int direction;
  if (JointsInfo[joint].DirJoint == 1){
    if (JointsInfo[joint].PosLimitSwitch < 0){
      direction = 0;
    }
    else{
      direction = 1;
    }
  }
  if (JointsInfo[joint].DirJoint == 0){
    if (JointsInfo[joint].PosLimitSwitch < 0){
      direction = 1;
    }
    else{
      direction = 0;
    }
  }
  

  Serial.println("move back");

  // if the endswitch is already detected first move away from the endswitch
  unsigned long switchStartTime = 0;
  float speed_del = 1000000 / ((20.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  Serial.println(float((40 / 100)) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  Serial.println((40.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  Serial.println(speed_del);
  digitalWrite(motors[joint].dir_pin, ((direction == 0) ? HIGH : LOW));
  while(true)
  {
    // Start the timer if the switch signal is just detected
    if (digitalRead(motors[joint].limit_switch_pin) == 0) {
        switchStartTime = switchStartTime;
        Serial.println("do not touch the limit switch");
    }
    else{
      switchStartTime = millis();
    }
    if (millis() - switchStartTime >= 30) {
      // Stop moving
      break;
    }

    digitalWrite(motors[joint].step_pin, HIGH);
    delayMicroseconds(5);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del);
  }


  Serial.println("move till switch is touched");
  delay(500);
  // move to the limit switch until the switch is activated
  switchStartTime = 0;
  speed_del = 1000000/((40.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  digitalWrite(motors[joint].dir_pin, ((direction == 0) ? LOW : HIGH));
  while(true)
  {
    // Start the timer if the switch signal is just detected
    if (digitalRead(motors[joint].limit_switch_pin) == 1) {
        switchStartTime = switchStartTime;
    }
    else{
      switchStartTime = millis();
    }
    if (millis() - switchStartTime >= 30) {
      // Stop moving
      break;
    }

    digitalWrite(motors[joint].step_pin, HIGH);
    delayMicroseconds(5);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del);
  }
  switchStartTime = 0;




  Serial.println("move 5 degrees back");
  delay(500);
  // move away from the limit switch
  speed_del = 1000000/((40.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  int steps_to_move = JointsInfo[joint].StepPerDeg * 12;
  digitalWrite(motors[joint].dir_pin, ((direction == 0) ? HIGH : LOW));
  for(int i = 0; i < steps_to_move; i++){
    digitalWrite(motors[joint].step_pin, HIGH);
    delayMicroseconds(5);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del);
  }



  Serial.println("move till switch is touched");
  delay(500);
  // move slowly back to the limit switch
  switchStartTime = 0;
  speed_del = 1000000/((5.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  digitalWrite(motors[joint].dir_pin, ((direction == 0) ? LOW : HIGH));
  while(true)
  {
    // Start the timer if the switch signal is just detected
    if (digitalRead(motors[joint].limit_switch_pin) == 1) {
        switchStartTime = switchStartTime;
    }
    else{
      switchStartTime = millis();
    }
    if (millis() - switchStartTime >= 30) {
      // Stop moving
      break;
    }

    digitalWrite(motors[joint].step_pin, HIGH);
    delayMicroseconds(5);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del);
  }
  switchStartTime = 0;

  robot[joint].PosJStart = JointsInfo[joint].PosLimitSwitch;
}

void offsetJ(){
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosEnd = robot[i].PosStart + read_String(Axis_name[i],robot[i].PosStart);
  }

  int speed = read_String('s',50);
  int accel = read_String('a',50);

  if (NUMBER_OF_JOINTS == 6){
    InverseKinematic_6();
  }

  MotorMoveJ(accel, speed, 0, 0);

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosStart = robot[i].PosEnd;
  }

  sendPos();
}

void offsetL(){
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosEnd = robot[i].PosStart + read_String(Axis_name[i],robot[i].PosStart);
  }

  int speed = read_String('s',50);
  int accel = read_String('a',50);

  //error = check_for_error();

  if(error){
    Serial.println("f\n");
  }
  else{
    int direction[NUMBER_OF_JOINTS];
    int maxDelta = 0;
    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      if(robot[i].PosEnd > robot[i].PosStart) direction[i] = 1;
      else direction[i] = 0;
      robot[i].PosDelta = abs(robot[i].PosEnd - robot[i].PosStart);
      if (robot[i].PosDelta > maxDelta){
        maxDelta = robot[i].PosDelta;
      }
    }

    float pointDistance = 0.5;
    int totalPoints = maxDelta / pointDistance;
    float incremants[NUMBER_OF_JOINTS];

    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      incremants[i] = robot[i].PosDelta / totalPoints;
    }

    for (int i = 0; i < totalPoints; i++){
      if (stop == 1) break;
      for (int L = 0; L < NUMBER_OF_JOINTS; L++){
        if (direction[L] == 1) robot[L].PosEnd = robot[L].PosStart + incremants[L];
        if (direction[L] == 0) robot[L].PosEnd = robot[L].PosStart - incremants[L];
      }

      if(NUMBER_OF_JOINTS == 6){
        InverseKinematic_6();
      }
      

      //error = check_for_error();
      if (error != 1){
        MotorMoveJ(accel, speed, speed, speed);
        for (int j = 0; j < NUMBER_OF_JOINTS; j++){
          robot[j].PosStart = robot[j].PosEnd;
        }
      }
      else{
        i = totalPoints;
      }
    }
  }
  sendPos();
}

void jogJ(){
  // find the new position of the robot
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosJEnd = robot[i].PosJStart + read_String(Joint_name[i], robot[i].PosStart);
  }

  int speed = read_String('s',50);
  int accel = read_String('a',50);

  error = check_for_error();
  if (error != 1)
  {
    MotorMoveJ(accel, speed, 0, 0);

    if(NUMBER_OF_JOINTS == 6){
      ForwardKinematic_6_PosEnd();
    }
    if(NUMBER_OF_JOINTS == 3){
      ForwardKinematic_3_PosEnd();
    }    

    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJStart = robot[i].PosJEnd;
    }
  }
  sendPos();
}

void jogL(){
  // find the new position of the robot
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosEnd = robot[i].PosStart + read_String(Axis_name[i],robot[i].PosStart);
  }

  int speed = read_String('s',50);
  int accel = read_String('a',50);

  if(NUMBER_OF_JOINTS == 6){
    InverseKinematic_6();
  }
  
  error = check_for_error();

  if(error != 1){
    int direction[NUMBER_OF_JOINTS];
    float maxDelta = 0;
    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      if (stop == 1) break;

      if(robot[i].PosEnd > robot[i].PosStart) direction[i] = 1;
      else direction[i] = 0;
      robot[i].PosDelta = abs(robot[i].PosEnd - robot[i].PosStart);
      if (robot[i].PosDelta > maxDelta){
        maxDelta = robot[i].PosDelta;
      }
    }
    float pointDistance = 1;
    int totalPoints = maxDelta / pointDistance;

    float incremants[NUMBER_OF_JOINTS];

    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      incremants[i] = robot[i].PosDelta / totalPoints;
    }

    for (int i = 0; i < totalPoints; i++){
      for (int L = 0; L < NUMBER_OF_JOINTS; L++){
        if (direction[L] == 1) robot[L].PosEnd = robot[L].PosStart + incremants[L];
        if (direction[L] == 0) robot[L].PosEnd = robot[L].PosStart - incremants[L];
      }

      if(NUMBER_OF_JOINTS == 6){
        InverseKinematic_6();
      }

      //error = check_for_error();
      if(error != 1){
        MotorMoveJ(accel, speed, speed, speed);
        for (int j = 0; j < NUMBER_OF_JOINTS; j++){
          robot[j].PosStart = robot[j].PosEnd;
        }
      }
      else{
        i = totalPoints;;
      }
    }
  }
  sendPos();
}

void MoveJ(){
  // MoveJ X400 Y0 Z300 y0 p180 r0 s50 a50
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosEnd = read_String(Axis_name[i],robot[i].PosStart);
  }

  int speed = read_String('s',50);
  int accel = read_String('a',50);

  if(NUMBER_OF_JOINTS == 6){
    InverseKinematic_6();
  }


  //error = check_for_error();
  if (error != 1){
    MotorMoveJ(accel, speed, 0, 0);

    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosStart = robot[i].PosEnd;
    }
  }
  sendPos();
}

void MoveL(){
  // find the new position of the robot
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosEnd = read_String(Axis_name[i],robot[i].PosStart);
  }

  int speed = read_String('s',50);
  int accel = read_String('a',50);

  if(error){
    Serial.println("f\n");
  }
  else{
    int direction[NUMBER_OF_JOINTS];
    int maxDelta = 0;
    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      if(robot[i].PosEnd > robot[i].PosStart) direction[i] = 1;
      else direction[i] = 0;
      robot[i].PosDelta = abs(robot[i].PosEnd - robot[i].PosStart);
      if (robot[i].PosDelta > maxDelta){
        maxDelta = robot[i].PosDelta;
      }
    }

    float pointDistance =2;
    int totalPoints = maxDelta / pointDistance;
    if (totalPoints < 1){
      totalPoints = 1;
    }
    float incremants[NUMBER_OF_JOINTS];

    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      incremants[i] = robot[i].PosDelta / totalPoints;
    }

    for (int i = 0; i < totalPoints; i++){
      if (stop == 1) break;
      for (int L = 0; L < NUMBER_OF_JOINTS; L++){
        if (direction[L] == 1) robot[L].PosEnd = robot[L].PosStart + incremants[L];
        if (direction[L] == 0) robot[L].PosEnd = robot[L].PosStart - incremants[L];
      }

      if(NUMBER_OF_JOINTS == 6){
        InverseKinematic_6();
      }
      
      //error = check_for_error();
      if (error != 1){
        MotorMoveJ(accel, speed, speed, speed);
        for (int j = 0; j < NUMBER_OF_JOINTS; j++){
          robot[j].PosStart = robot[j].PosEnd;
          // Serial.print(robot[j].PosStart);
          // Serial.print(" ");
        }
        // Serial.println("");
      }

      else{
        i = totalPoints;
      }

    }
    
  }

  sendPos();
}


// Functions tool

void tool_state(){
  int pos_1_TOOL = command.indexOf('(');
  int pos_2_TOOL = command.indexOf(')');
  String state = command.substring(pos_1_TOOL + 1, pos_2_TOOL);

  Serial.print("state ");
  Serial.print(state);
  Serial.println(" f");



  if (state == "LOW"){
    digitalWrite(tool_pin, LOW);
  }
  else if (state == "HIGH"){
    digitalWrite(tool_pin, HIGH);
  }


}

void tool_move_to(){
  int pos_1_TOOL = command.indexOf('(');
  int pos_2_TOOL = command.indexOf(')');
  int New_pos = command.substring(pos_1_TOOL + 1, pos_2_TOOL).toInt();

  float togo_pos = New_pos * ((servo_max - servo_min) / 100.0);

  if ((togo_pos - tool_pos) > 0){
    for (int pos = tool_pos; pos <= New_pos; pos += 1){
      delay(20);
      servoTool.write(pos);
    }
  }
  else{
    for (int pos = tool_pos; pos > New_pos; pos -= 1){
      delay(20);
      servoTool.write(pos);
    }
  }

  tool_pos = togo_pos;

  Serial.print("POS: G ");
  Serial.println(tool_pos);

  Serial.println("END");
}

// Functions IO
void IO_digitalWrite(){


  int pos_1_IO = command.indexOf('P');
  int pos_2_IO = command.indexOf('S');

  int io_number = command.substring(pos_1_IO + 1, pos_2_IO).toInt();
  int state = command.substring(pos_2_IO + 1).toInt();

  Serial.print("Pin number: ");
  Serial.println(io_pin[io_number]);

  if (state == 0) digitalWrite(io_pin[io_number], LOW);
  else if (state == 1) digitalWrite(io_pin[io_number], HIGH);
}

void sendPos(){
  Serial.print("POS: ");

  for(int i = 0; i< NUMBER_OF_JOINTS; i++){
    Serial.print(Axis_name[i]);
    Serial.print(" ");
    Serial.print(robot[i].PosEnd);
    Serial.print(" ");
  }

  for(int i = 0; i< NUMBER_OF_JOINTS; i++){
    Serial.print(Joint_name_string[i]);
    Serial.print(" ");
    Serial.print(robot[i].PosJEnd);
    Serial.print(" ");
  }

  Serial.println("");

  Serial.println("END");
}
