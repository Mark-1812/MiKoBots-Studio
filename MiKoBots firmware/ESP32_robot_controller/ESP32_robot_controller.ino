// FIRMWARE for the robot
// Version 1.22
// date 18-2-2025

/*
The current version of the firmware allows you to use also arduino mega boards and
use servo for the joints besides stepper motors. 

The firmware is still in development if you have issues please contact info@mikobots.com

ps. diclaimer I'm not an software engineer, if you have any tips please share
*/


#define type_device "IO"       /// change to IO if you installing the IO box
#define board_expansion "Braccio" // Needed for Braccio robot arm can be set to "None" if not use, else set to "Braccio"


#include <math.h>
#define MAX_NUMBER_OF_JOINTS 6
int NUMBER_OF_JOINTS = 6;
int EXTRA_JOINT = 0;


int KinematicError = 0;
int error = 0;

char alphabet[] = {
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
  'a', 'b', 'c', 'd', 'e', 'f', 'g'
};

char Axis_name[] = {'X', 'Y', 'Z', 'y', 'p', 'r'};
const char* Joint_name[] = {"J1", "J2", "J3", "J4", "J5","J6"};

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

// structure positions
typedef struct{
  float PosStart; // XYZUVW
  double PosEnd; // XYZUVW
  float PosDelta; 
  float PosJStart; // J1 J2 J3 J4 J5 J6
  double PosJEnd; // J1 J2 J3 J4 J5 J6
  float PosJCur;
  long PosJDelta;
} robot_struct;
robot_struct robot[MAX_NUMBER_OF_JOINTS];

// variables tools
int tool_pin; 
int tool_type;
int servo_min;
int servo_max;
int tool_pos; 

// Variables io
int io_pin[10]; 
int io_type[10];
int io_state[10];

int stop = false;
int pauze = false;

bool deviceConnected = false;
bool deviceDisconnected = false;

void sendPos();
void ForwardKinematic_6_PosEnd();
void ForwardKinematic_3_PosEnd();


// get the type of microcontroller
#if defined(ARDUINO_ARCH_ESP32)
#define platform "ESP32"
#include <ESP32Servo.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <TaskScheduler.h>


typedef struct {
  int step_pin;
  int dir_pin;
  int ena_pin;
  int limit_switch_pin;
  bool motor_type; // if it true it is a servo, false means stepper motor
  bool servo_dir;
  int servo_pin;
  int servo_max;
  int servo_min;
  int servo_degree;
  int PosZeroServo;
  Servo* servo;
} Motor;
Motor motors[MAX_NUMBER_OF_JOINTS];
Servo servoInstances[MAX_NUMBER_OF_JOINTS];

Servo servoTool;
String serialBuffer;

TaskHandle_t Task1;
TaskHandle_t Task2;
SemaphoreHandle_t mutex;
SemaphoreHandle_t stopSemaphore;


#include "Motor_move.h"
#include "Kinematic_functions.h"
#include "Kinematics_6.h"
#include "Kinematics_5.h"
#include "Kinematics_3.h"
#include "Robot_commands.h"
#include "Tool_commands.h"
#include "IO_commands.h"
#include "error.h"


///// Bluetooth settings and libraries
#define CHARACTERISTIC_UUID_ROBOT "c42e42e4-8214-420c-944d-e127cc0f20ba"
#define SERVICE_UUID_ROBOT        "a917e658-9c1a-4901-bbb8-92d54cfa2fdd" 

#define CHARACTERISTIC_UUID_IO "19680482-86af-4892-ab79-962e98f41045"  // UUID for IO
#define SERVICE_UUID_IO        "30a96603-6e34-49d8-9d64-a13f68fefab6"

const int BUFFER_SIZE = 10;
String lines[BUFFER_SIZE];
volatile int lineIndex = 0;

const int MAX_BUFFER_SIZE = 256; // Adjust size according to your requirements
char buffer[MAX_BUFFER_SIZE]; // Character array to hold serial input


// Create a BLE server and characteristic
BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;


void sent_message(String message){
  if (deviceConnected & platform == "ESP32"){
    if (pCharacteristic->getValue() == "") {
      String responseData = message;
      pCharacteristic->setValue(responseData.c_str());
      pCharacteristic->notify(); // Notify the client that data has been sent
      vTaskDelay(3 / portTICK_PERIOD_MS);
      pCharacteristic->setValue("");
    }
  }
  Serial.println(message);
}

void sent_message_task1(String message){
  if (deviceConnected & platform == "ESP32"){
      String responseData = message;
      pCharacteristic->setValue(responseData.c_str());
      pCharacteristic->notify(); // Notify the client that data has been sent
      vTaskDelay(3 / portTICK_PERIOD_MS);
      pCharacteristic->setValue("");
  }
  Serial.println(message);
}

// Callback class to handle connection events
class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) override {
    deviceConnected = true;
    Serial.println("Device connected");
    deviceDisconnected = false;
  }

  void onDisconnect(BLEServer* pServer) override {
    deviceConnected = false;
    Serial.println("Device disconnected");
    pServer->startAdvertising();

    for(int i = 0; i < BUFFER_SIZE; i++){
      lines[i] = "";
    }
    lineIndex = 0;
    stop = false;
    pauze = false;

    deviceDisconnected = true;

    // release all the pins on discontection
    for (int pin = 0; pin < 38; pin++) {
      pinMode(pin, INPUT); 
    }
  }
};


/// send a message with bluetooth

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  
  if(platform == "ESP32"){
    initializeBLE();
    initializeTasks();
  }


  for(int i = 0; i < MAX_NUMBER_OF_JOINTS; i++){
    robot[i].PosJStart = 0.01;
  }

  String Message = String(type_device) + "_CONNECTED";
  sent_message(Message);

}

void loop() {
}

void initializeTasks(){
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

  

  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("BLE Device is Ready to Pair");

  Serial.print("Free heap: ");
  Serial.println(ESP.getFreeHeap());

  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
                    Task1code,   /* Task function. */
                    "Task1",     /* name of task. */
                    8192,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task1,      /* Task handle to keep track of created task */
                    0);          /* pin task to core 0 */                  
  delay(300); 

  //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  xTaskCreatePinnedToCore(
                    Task2code,   /* Task function. */
                    "Task2",     /* name of task. */
                    15000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task2,      /* Task handle to keep track of created task */
                    1);          /* pin task to core 1 */
  delay(300);
}

void initializeBLE(){
  // Initialize BLE
  BLEDevice::init("Robot_MiKoBots");  // Custom BLE name here

  // Create BLE server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  if (pServer == NULL) {
    Serial.println("Failed to create BLE server");
    while (1); // Halt the program
  }

  String SERVICE_UUID = "";
  String CHARACTERISTIC_UUID = "";
  if (type_device == "ROBOT"){
    SERVICE_UUID = SERVICE_UUID_ROBOT;
    CHARACTERISTIC_UUID = CHARACTERISTIC_UUID_ROBOT;
  }
  if (type_device == "IO"){
    SERVICE_UUID = SERVICE_UUID_IO;
    CHARACTERISTIC_UUID = CHARACTERISTIC_UUID_IO;
  }

  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                    CHARACTERISTIC_UUID_ROBOT,
                    BLECharacteristic::PROPERTY_READ |
                    BLECharacteristic::PROPERTY_WRITE |
                    BLECharacteristic::PROPERTY_NOTIFY
                  );

  // Add descriptor for notifications
  pCharacteristic->addDescriptor(new BLE2902());

  // Start the BLE service
  pService->start();
}

void Task1code(void * pvParameters) {
  while (true) {
    // Process Serial Input
    while (Serial.available() > 0) {
      deviceDisconnected = false;
        char c = Serial.read();
        if (c == '\n') {
            String str(buffer);
            processCommand(str);  // Process command in a separate function
            memset(buffer, 0, sizeof(buffer));  // Clear buffer
        } else {
            if (strlen(buffer) < (sizeof(buffer) - 1)) {
                strncat(buffer, &c, 1);
            }
        }
    }

    // Process Bluetooth Input
    if (deviceConnected && pCharacteristic->getValue() != "") {
        String recievedData = pCharacteristic->getValue().c_str();
        pCharacteristic->setValue("");  // Clear after reading
        processCommand(recievedData);  // Process command in a separate function
        recievedData = "";
    }


    checkInputs();  // Separate function for input checks
    vTaskDelay(100 / portTICK_PERIOD_MS);  // Use vTaskDelay instead of delay
  }
}

String coordinates;
void Task2code(void * pvParameters) {
  String command;
  while (true) {
    while (stop == false){
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

      typeOfCommand.trim();

      // Commands
      if (type_device  == "ROBOT" and typeOfCommand.equals("MoveL")) MoveL(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("MoveJ")) MoveJ(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("MoveJoint")) MoveJoint(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("jogL")) jogL(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("jogJ")) jogJ(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("OffsetJ")) offsetJ(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("OffsetL")) offsetL(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Home")) home_Joints(command);

      // commands tool
      else if (typeOfCommand.equals("Tool_move_to")) tool_move_to(command);
      else if (typeOfCommand.equals("Tool_state")) tool_state(command);  

      // commands IO
      else if (typeOfCommand.equals("IO_digitalWrite")) IO_digitalWrite(command);

      // Settings robot
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_number_of_joints")) set_number_of_joints(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_motor_type")) set_motor_type(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_servo_pin")) set_servo_pin(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_servo_pulse")) set_servo_pulse(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_ena_pin")) set_enable_pin(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_servo_position")) set_servo_pos(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_motor_pin")) set_motor_pin(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_switch_pin")) set_switch_pin(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_max_pos")) set_max_pos(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_lim_pos")) set_lim_pos(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_step_deg")) set_step_deg(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_dir_joints")) set_direction_joint(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_dh_par")) set_dh_par(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_speed")) set_speed(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_home_settings")) set_homing(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_extra_joint")) set_extra_joint(command);
      

      // Settings Tool
      else if (typeOfCommand.equals("Set_tools")) set_TOOL(command);
      else if (typeOfCommand.equals("Set_tool_frame")) set_tool_frame(command);

      // Settings IO
      else if (typeOfCommand.equals("Set_io_pin")) set_IO_pin(command);

      //If the command does not match send END
      // else{
      //   String message = "Error: do not regonize this command: " + typeOfCommand;
      //   sent_message(message);
      //   sent_message("END");
      // }
    

      if ((xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE) and (command != "")){
        for (int i = 0; i < BUFFER_SIZE - 1; i++) {
          lines[i] = lines[i+1];
        }      

        lines[BUFFER_SIZE - 1] = ""; // Clear the last line'
        lineIndex--;

        if(lineIndex < BUFFER_SIZE - 1){
          sent_message("go");
        } 
        xSemaphoreGive(mutex);
      }

    }
    if (stop){

      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE){
        for (int i = 0; i < BUFFER_SIZE; i++) {
          lines[i] = "";
        } 

        lineIndex = 0; // Wrap around if the buffer is full
        xSemaphoreGive(mutex);
      }
    }
    vTaskDelay(5 / portTICK_PERIOD_MS);  
  }
  vTaskDelay(10 / portTICK_PERIOD_MS);
}

void processCommand(const String& command) {
    if (command == "stop") {
        stop = true;  
        
    } else if (command == "pauze") {
        sent_message_task1("pauze");
        pauze = true;
    } else if (command == "play") {
        stop = false;
        pauze = false;
        sent_message_task1("END");
    } else if (command == "CONNECT") {
        String Message = String(type_device) + "_CONNECTED";
        sent_message_task1(Message);
    } else if (command != "stop" and command != "pauze" and command != "play" and command != "" and command != "go" and command != "wait" and command != "END" and command != "POS" and command != "POS:") {
        storeInBuffer(command);  // Separate function to store data
    }
}

void storeInBuffer(const String& data) {
  if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE) {
    if (lineIndex < BUFFER_SIZE) {
      lines[lineIndex] = data;
      lineIndex++;
    } else {
      sent_message_task1("Error: Buffer overflow");
    }
    if (lineIndex > BUFFER_SIZE - 2) {
      sent_message_task1("wait");
    }
    xSemaphoreGive(mutex);
  }
}

void checkInputs() {
  for (int i = 0; i < 10; i++) {
    if (io_type[i] == 1) {
      if (!digitalRead(io_pin[i]) && io_state[i] == 0) {
        String command = String("Input " + String(i) + " 1");
        sent_message(command);
        io_state[i] = 1;
      }
      if (digitalRead(io_pin[i]) && io_state[i] == 1) {
        String command = String("Input " + String(i) + " 0");
        sent_message(command);
        io_state[i] = 0;          
      }
    }
  }
}



#elif defined(ARDUINO_ARCH_AVR)
#define platform "UNO"
#include <Arduino.h>
#include <Servo.h>

Servo servoTool;

// structure of motors
typedef struct {
  int step_pin;
  int dir_pin;
  int ena_pin;
  int limit_switch_pin;
  bool motor_type; // if it true it is a servo, false means stepper motor
  bool servo_dir;
  int servo_pin;
  int servo_max;
  int servo_min;
  int PosZeroServo;
  int servo_degree;
  Servo* servo;
} Motor;

Motor motors[MAX_NUMBER_OF_JOINTS];
Servo servoInstances[MAX_NUMBER_OF_JOINTS];

// The Servo can not directly be used in the the struct, so store pointer to servo object

#include "Motor_move.h"
#include "Kinematic_functions.h"
#include "Kinematics_6.h"
#include "Kinematics_5.h"
#include "Kinematics_3.h"
#include "Robot_commands.h"
#include "Tool_commands.h"
#include "IO_commands.h"
#include "error.h"



const int MAX_BUFFER_SIZE = 256; // Adjust size according to your requirements
char buffer[MAX_BUFFER_SIZE]; // Character array to hold serial input



void setup() {
  Serial.begin(57600);

  if (board_expansion == "Braccio"){
    pinMode(12, OUTPUT);
    digitalWrite(12, HIGH);
  }

  String Message = String(type_device) + "_CONNECTED";
  sent_message(Message);
}

void loop() {
  while (Serial.available() > 0) {
    deviceDisconnected = false;
      char c = Serial.read();
      if (c == '\n') {
          String str(buffer);
          processCommand(str);  // Process command in a separate function
          memset(buffer, 0, sizeof(buffer));  // Clear buffer
      } else {
        if (strlen(buffer) < (sizeof(buffer) - 1)) {
            strncat(buffer, &c, 1);
        }
      }
  }

  delay(10);

}

String coordinates;
void processCommand(const String& command) {
    if (command == "stop") {
        stop = true;  
    } else if (command == "pauze") {
        sent_message("pauze");
        pauze = true;
    } else if (command == "play") {
        stop = false;
        pauze = false;
        sent_message("END");
    } else if (command == "CONNECT") {
        String Message = String(type_device) + "_CONNECTED";
        sent_message(Message);
    } 

    int spaceIndex = command.indexOf(' ');
    String typeOfCommand = command.substring(0, spaceIndex);
    coordinates = command.substring(spaceIndex + 1);

    typeOfCommand.trim();

    if (type_device  == "ROBOT" and typeOfCommand.equals("MoveL")) MoveL(command);
    else if (type_device  == "ROBOT" and typeOfCommand.equals("MoveJ")) MoveJ(command);
    else if (type_device  == "ROBOT" and typeOfCommand.equals("MoveJoint")) MoveJoint(command);
    else if (type_device  == "ROBOT" and typeOfCommand.equals("jogL")) jogL(command);
    else if (type_device  == "ROBOT" and typeOfCommand.equals("jogJ")) jogJ(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("OffsetJ")) offsetJ(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("OffsetL")) offsetL(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Home")) home_Joints(command);

    // commands tool
    else if (typeOfCommand.equals("Tool_move_to")) tool_move_to(command);
    else if (typeOfCommand.equals("Tool_state")) tool_state(command);  

    // commands IO
    else if (typeOfCommand.equals("IO_digitalWrite")) IO_digitalWrite(command);

    // Settings robot
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_number_of_joints")) set_number_of_joints(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_motor_type")) set_motor_type(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_servo_pin")) set_servo_pin(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_servo_pulse")) set_servo_pulse(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_servo_position")) set_servo_pos(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_motor_pin")) set_motor_pin(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_ena_pin")) set_enable_pin(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_switch_pin")) set_switch_pin(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_max_pos")) set_max_pos(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_lim_pos")) set_lim_pos(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_step_deg")) set_step_deg(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_dir_joints")) set_direction_joint(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_dh_par")) set_dh_par(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_speed")) set_speed(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_home_settings")) set_homing(command);
    else if (type_device == "ROBOT" and typeOfCommand.equals("Set_extra_joint")) set_extra_joint(command);
    

    // Settings Tool
    else if (typeOfCommand.equals("Set_tools")) set_TOOL(command);
    else if (typeOfCommand.equals("Set_tool_frame")) set_tool_frame(command);

    // Settings IO
    else if (typeOfCommand.equals("Set_io_pin")) set_IO_pin(command);
}

void sent_message(String message){
  Serial.println(message);
}


#endif


void sendPos(){
  String command = "POS: ";

  for(int i = 0; i< NUMBER_OF_JOINTS; i++){
    command += String(Axis_name[i]) + " " + String(robot[i].PosEnd) + " ";
  }

  for(int i = 0; i< NUMBER_OF_JOINTS; i++){
    command += String(Joint_name[i]) + " " + String(robot[i].PosJEnd) + " ";
  }

  sent_message(command);

  String command1 = "PSJstart: ";

  for(int i = 0; i< NUMBER_OF_JOINTS; i++){
    command1 += String(Axis_name[i]) + " " + String(robot[i].PosEnd) + " ";
  }

  for(int i = 0; i< NUMBER_OF_JOINTS; i++){
    command1 += String(Joint_name[i]) + " " + String(robot[i].PosJEnd) + " ";
  }

  sent_message(command1);
  sent_message("END");


}
