#ifndef Robot_commands_H
#define Robot_commands_H

void MotorMoveJ(float ACC1, float VEL1, float VEL_0, float VEL_1);
void sent_message(String message);
void sendPos();

void set_number_of_joints();
void set_motor_pin();
void set_switch_pin();
void set_lim_pos();
void set_max_pos();
void set_step_deg();
void set_direction_joint();
void set_homing();
void set_dh_par();
void set_speed();

void home_Joints();
void offsetJ();
void jogJ();
void MoveJ();
void MoveL();


//// settings update
void set_number_of_joints(String command){
  int pos = command.indexOf('A');

  NUMBER_OF_JOINTS = command.substring(pos + 1).toInt();

  sent_message("Number of joints are set");
  sent_message("END");
}

void set_extra_joint(String command){
  int pos = command.indexOf('A');

  EXTRA_JOINT = command.substring(pos + 1).toInt();

  sent_message("Extra joint is set");
  sent_message("END");
}

void set_motor_pin(String command){
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
    if (!motors[i].motor_type){
      pinMode(motors[i].step_pin, OUTPUT);
      pinMode(motors[i].dir_pin, OUTPUT);
    }
    else{
      Serial.print("Joint is servo: ");
      Serial.println(i);
    }
  }

  sent_message("Motor pins settings are updated");
  sent_message("END");
}

void set_enable_pin(String command){
  int pos_setting[6];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].ena_pin = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      motors[i].ena_pin = command.substring(pos_setting[i] + 1).toInt();
    }
  }


  for(int i=0; i < NUMBER_OF_JOINTS; i++) {  
    // set the motor pin & scale
    if (!motors[i].motor_type){
      pinMode(motors[i].ena_pin, OUTPUT);
      digitalWrite(motors[i].ena_pin, LOW);
    }
    else{
      Serial.print("Joint is servo: ");
      Serial.println(i);
    }
  }

  sent_message("Enable pins settings are updated");
  sent_message("END");
}

void set_motor_type(String command){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].motor_type = (command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt() != 0); // convert it toa true (1) or false (0)
    } else{
      motors[i].motor_type = (command.substring(pos_setting[i] + 1).toInt() != 0); // convert it toa true (1) or false (0)
    }
  }

  sent_message("Motor types are set");
  sent_message("END");
}


void set_servo_pos(String command){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].PosZeroServo = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt(); // convert it toa true (1) or false (0)
    } else{
      motors[i].PosZeroServo = command.substring(pos_setting[i] + 1).toInt(); // convert it toa true (1) or false (0)
    }
  }

  for(int i=0; i < NUMBER_OF_JOINTS; i++) {  
    if (motors[i].motor_type){
      Serial.print("Joint is servo: ");
      Serial.println(i);
      robot[i].PosJCur = motors[i].servo_min;

      Serial.print("PosJCur: ");
      Serial.println(robot[i].PosJCur);

      robot[i].PosJStart = - motors[i].PosZeroServo;
      robot[i].PosJEnd = 0;
      MotorMoveJ(50, 80, 0, 0);
    }
  }

  sent_message("Servo pos settings are set");
  sent_message("END");
}

void set_servo_pin(String command){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].servo_pin = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt(); // convert it toa true (1) or false (0)
    } else{
      motors[i].servo_pin = command.substring(pos_setting[i] + 1).toInt(); // convert it toa true (1) or false (0)
    }
  }

  for(int i=0; i < NUMBER_OF_JOINTS; i++) {  
    if (motors[i].motor_type){
      Serial.print("Joint is servo: ");
      Serial.println(i);

      motors[i].servo = &servoInstances[i];
      motors[i].servo->attach(motors[i].servo_pin);
    }
  }

  sent_message("Servo pin settings are set");
  sent_message("END");
}



void set_servo_pulse(String command){
  // the setting for servo is build like this
  // A servo_pin(1) B servo_max(1) C servo_min(1) D servo_degree(1) E servo_pin(2) F servo_max(2).............
  int pos_setting[30];

  for(int i = 0; i < NUMBER_OF_JOINTS * 3; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    motors[i].servo_max = command.substring(pos_setting[j] + 1, pos_setting[j + 1]).toFloat();
    motors[i].servo_min = command.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toFloat();
    if (i < NUMBER_OF_JOINTS - 1){
      motors[i].servo_degree = command.substring(pos_setting[j + 2] + 1, pos_setting[j + 3]).toInt();
      
    } else{
      motors[i].servo_degree = command.substring(pos_setting[j + 3] + 1).toInt();
    }
    
    j = j + 3;
  }

  for(int i=0; i < NUMBER_OF_JOINTS; i++) {  
    if (motors[i].motor_type){
      Serial.print("Joint is servo: ");
      Serial.println(i);


      // set the step per deg
      JointsInfo[i].StepPerDeg = (motors[i].servo_max - motors[i].servo_min) / float(motors[i].servo_degree);
    }
  }

  sent_message("Servo pulse settings are updated");
  sent_message("END");
}

void set_switch_pin(String command){
  int pos_setting[24];

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

  sent_message("Switch pins settings are updated");
  sent_message("END");
}

void set_lim_pos(String command){
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

  sent_message("Position limit switch settings are updated");
  sent_message("END");
}

void set_max_pos(String command){
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

  sent_message("Position settings are updated");
  sent_message("END");
}

void set_step_deg(String command){
  int pos_setting[12];

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS - 1 & !motors[i].motor_type){
      JointsInfo[i].StepPerDeg = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else if(!motors[i].motor_type){
      JointsInfo[i].StepPerDeg = command.substring(pos_setting[i] + 1).toInt();
    }
  }


  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    Serial.println(JointsInfo[i].StepPerDeg);
  }

  sent_message("Steps per degree settings are updated");
  sent_message("END");
}

void set_direction_joint(String command){
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

  sent_message("Direction of the joints settings are updated");
  sent_message("END");
}

void set_homing(String command){
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

  sent_message("Homing settings are updated");
  sent_message("END");
}

void set_dh_par(String command){

  int pos_setting[24];

  int posA = command.indexOf('A');
  String NEWcommand = command.substring(posA);

  for(int i = 0; i < (NUMBER_OF_JOINTS + EXTRA_JOINT) * 4; i++){
    pos_setting[i] = NEWcommand.indexOf(alphabet[i]);
  }

  int j = 0;
  for(int i = 0; i < (NUMBER_OF_JOINTS + EXTRA_JOINT); i++){
    DHparams[i][0] = NEWcommand.substring(pos_setting[j] + 1, pos_setting[j + 1]).toFloat();
    DHparams[i][1] = NEWcommand.substring(pos_setting[j + 1] + 1, pos_setting[j + 2]).toFloat();
    DHparams[i][2] = NEWcommand.substring(pos_setting[j + 2] + 1, pos_setting[j + 3]).toFloat();

    if (i < (NUMBER_OF_JOINTS + EXTRA_JOINT) - 1){
      DHparams[i][3] = NEWcommand.substring(pos_setting[j + 3] + 1, pos_setting[j + 4]).toFloat();
    } else{
      DHparams[i][3] = NEWcommand.substring(pos_setting[j + 3] + 1).toFloat();
    }
    j = j + 4;
  }

  //DECLARE R06 NEG FRAME
  R06_neg_matrix[2][3] = -DHparams[5][2];

  if (NUMBER_OF_JOINTS == 3){
    ForwardKinematic_3_PosStart();
  }
  if(NUMBER_OF_JOINTS == 5){
    ForwardKinematic_5_PosEnd();
    ForwardKinematic_5_PosStart();
  }
  if (NUMBER_OF_JOINTS == 6){
    ForwardKinematic_6_PosStart();
  }

  sent_message("DH parameters settings are updated");
  sent_message("END");
}

void set_speed(String command){
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

  sent_message("Speed settings are updated");
  sent_message("END");

}



// functions Move robot
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
  

  // if the endswitch is already detected first move away from the endswitch
  unsigned long switchStartTime = 0;
  float speed_del = 1000000 / ((20.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  digitalWrite(motors[joint].dir_pin, ((direction == 0) ? HIGH : LOW));
  while(true)
  {
    // Start the timer if the switch signal is just detected
    if (digitalRead(motors[joint].limit_switch_pin) == 0) {
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
    delayMicroseconds(speed_del / 2);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del);

    if (deviceDisconnected || stop){
      break;
    }
  }


  //  Serial.println("move till switch is touched");
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
    delayMicroseconds(speed_del / 2);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del / 2);

    if (deviceDisconnected || stop){
      break;
    }
  }
  switchStartTime = 0;




  // Serial.println("move 5 degrees back");
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


  // Serial.println("move till switch is touched");
  delay(500);
  // move slowly back to the limit switch
  switchStartTime = 0;
  speed_del = 1000000/((5.0 / 100.0) * JointsInfo[joint].MaxSpeed * JointsInfo[joint].StepPerDeg);
  digitalWrite(motors[joint].dir_pin, ((direction == 0) ? LOW : HIGH));
  while(true)
  {
    if (deviceDisconnected || stop){
      break;
    }

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
    delayMicroseconds(speed_del / 2);
    digitalWrite(motors[joint].step_pin, LOW);
    delayMicroseconds(speed_del / 2);
  }
  switchStartTime = 0;

  robot[joint].PosJStart = JointsInfo[joint].PosLimitSwitch;
}

void home_Joints(String command){
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosJStart = 0.01;
    robot[i].PosJEnd = 0.0001;
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (deviceDisconnected || stop){
      break;
    }

    // Serial.print(i + 1);
    // Serial.print(" out of ");
    // Serial.println(NUMBER_OF_JOINTS);

    // look for the joint that has to be homed first
    for(int j = 0; j < NUMBER_OF_JOINTS; j++){
      if (deviceDisconnected || stop){
        break;
      }

      // See if the joint order is the same 
      if(JointsInfo[j].HomingOrder == i + 1 & !motors[j].motor_type){
        
        moveToLimit(j);
        robot[j].PosJEnd = JointsInfo[j].HomingPos;
        MotorMoveJ(50, 80, 0, 0);
        
      } else if(JointsInfo[j].HomingOrder == i + 1 & motors[j].motor_type){
        // when the motor of the joint is a servo there is no limit switch 
        // posLimitSwitch is the position of the servo when the joint is in 0 position
        MotorMoveJ(50, 80, 0, 0);
      }

    }
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosJStart = JointsInfo[i].HomingPos;
    robot[i].PosJEnd = 0;
  }

  MotorMoveJ(50, 50, 0, 0);

  if(NUMBER_OF_JOINTS == 6){
    ForwardKinematic_6_PosEnd();
    ForwardKinematic_6_PosStart();
  }
  if(NUMBER_OF_JOINTS == 5){
      ForwardKinematic_5_PosEnd();
      ForwardKinematic_5_PosStart();
  }
  if(NUMBER_OF_JOINTS == 3){
    ForwardKinematic_3_PosEnd();
    ForwardKinematic_3_PosStart();
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosJStart = robot[i].PosJEnd;
  }
    
  if (!deviceDisconnected || !stop){
    sent_message("home");
    sent_message("END");
  }  
  sendPos();
}

void offsetJ(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosEnd = robot[i].PosStart + command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();

  if (NUMBER_OF_JOINTS == 6){
    InverseKinematic_6();
  }
  else if (NUMBER_OF_JOINTS == 5){
    InverseKinematic_5();
  }
  else if (NUMBER_OF_JOINTS == 3){
    InverseKinematic_3();
  }

  MotorMoveJ(accel, speed, 0, 0);

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosStart = robot[i].PosEnd;
  }

  sendPos();
}

void offsetL(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosEnd = robot[i].PosStart + command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();


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

    int totalPoints = maxDelta / 0.5;
    float incremants[NUMBER_OF_JOINTS];

    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      incremants[i] = robot[i].PosDelta / totalPoints;
    }

    for (int i = 0; i < totalPoints; i++){
      if (stop) break;
      for (int L = 0; L < NUMBER_OF_JOINTS; L++){
        if (direction[L] == 1) robot[L].PosEnd = robot[L].PosStart + incremants[L];
        if (direction[L] == 0) robot[L].PosEnd = robot[L].PosStart - incremants[L];
      }

      if(NUMBER_OF_JOINTS == 6){
        InverseKinematic_6();
      }
      else if(NUMBER_OF_JOINTS == 5){
        InverseKinematic_5();
      }
      else if(NUMBER_OF_JOINTS == 3){
        InverseKinematic_3();
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

void jogJ(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosJEnd = robot[i].PosJStart + command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();

  //error = check_for_error();
  if (error != 1)
  {
    MotorMoveJ(accel, speed, 0, 0);

    if(NUMBER_OF_JOINTS == 6){
      ForwardKinematic_6_PosStart();
      ForwardKinematic_6_PosEnd();
    }
    else if(NUMBER_OF_JOINTS == 5){
      ForwardKinematic_5_PosStart();
      ForwardKinematic_5_PosEnd();
    }
    else if(NUMBER_OF_JOINTS == 3){
      ForwardKinematic_3_PosStart();
      ForwardKinematic_3_PosEnd();
    }    

    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJStart = robot[i].PosJEnd;
    }
  }
  sendPos();
}

void MoveJoint(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosJEnd = command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();

  //error = check_for_error();
  if (error != 1)
  {
    MotorMoveJ(accel, speed, 0, 0);

    if(NUMBER_OF_JOINTS == 6){
      ForwardKinematic_6_PosEnd();
      ForwardKinematic_6_PosStart();
    }
    else if(NUMBER_OF_JOINTS == 5){
      ForwardKinematic_5_PosEnd();
      ForwardKinematic_5_PosStart();
    }
    else if(NUMBER_OF_JOINTS == 3){
      ForwardKinematic_3_PosEnd();
      ForwardKinematic_3_PosStart();
    }    


    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJStart = robot[i].PosJEnd;
    }
  }
  sendPos();
}

void jogL(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosEnd = robot[i].PosStart + command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();

  if(NUMBER_OF_JOINTS == 6){
    InverseKinematic_6();
  }
  else if(NUMBER_OF_JOINTS == 5){
    InverseKinematic_5();
  }
  else if(NUMBER_OF_JOINTS == 3){
    InverseKinematic_3();
  }
  
  //error = check_for_error();

  if(error != 1){
    int direction[NUMBER_OF_JOINTS];
    float maxDelta = 0;
    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      if (stop) break;

      if(robot[i].PosEnd > robot[i].PosStart) direction[i] = 1;
      else direction[i] = 0;
      robot[i].PosDelta = abs(robot[i].PosEnd - robot[i].PosStart);
      if (robot[i].PosDelta > maxDelta){
        maxDelta = robot[i].PosDelta;
      }
    }
    int totalPoints = maxDelta / 1;

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
      else if(NUMBER_OF_JOINTS == 5){
        InverseKinematic_5();
      }
      else if(NUMBER_OF_JOINTS == 3){
        InverseKinematic_3();
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

void MoveJ(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosEnd = command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();

  if(NUMBER_OF_JOINTS == 6){
    InverseKinematic_6();
  }
  else if(NUMBER_OF_JOINTS == 5){
    InverseKinematic_5();
  }
  else if(NUMBER_OF_JOINTS == 3){
    InverseKinematic_3();
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

void MoveL(String command){
  int pos_command[12];
  for(int i = 0; i < (NUMBER_OF_JOINTS + 2); i++){
    pos_command[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (i < NUMBER_OF_JOINTS ){
      robot[i].PosEnd = command.substring(pos_command[i] + 1, pos_command[i + 1]).toFloat();
    } 
  }

  int speed = command.substring(pos_command[NUMBER_OF_JOINTS] + 1, pos_command[NUMBER_OF_JOINTS + 1]).toInt();
  int accel = command.substring(pos_command[NUMBER_OF_JOINTS + 1] + 1).toInt();

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
      if (stop) break;
      for (int L = 0; L < NUMBER_OF_JOINTS; L++){
        if (direction[L] == 1) robot[L].PosEnd = robot[L].PosStart + incremants[L];
        if (direction[L] == 0) robot[L].PosEnd = robot[L].PosStart - incremants[L];
      }

      if(NUMBER_OF_JOINTS == 6){
        InverseKinematic_6();
      }
      else if (NUMBER_OF_JOINTS == 5){
        InverseKinematic_5();
      }
      else if(NUMBER_OF_JOINTS == 3){
        InverseKinematic_3();
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




#endif
