void sent_message(String message);

void MotorMoveJ(float ACC1, float VEL1, float VEL_0, float VEL_1){
  // ACC:       acceleration in     ->  (steps/seconds)2
  // VEL:       maximum velocity    ->  steps/seconds
  // VelStart:  start speed         ->  steps/seconds
  // VelEnd:    end speed           ->  steps/seconds

  long maxSteps = 0;
  float maxDeg = 0;
  long JointMaxMove = 0;
  int JointMaxDeg = 0;

  for (int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosJDelta = (robot[i].PosJEnd - robot[i].PosJStart) * JointsInfo[i].StepPerDeg;

    // Serial.print("J");
    // Serial.print(i);

    // Serial.print(" Pos J end ");
    // Serial.print(robot[i].PosJEnd);

    // Serial.print(" Pos J start ");
    // Serial.println(robot[i].PosJStart);

    // Serial.print(" step per deg ");
    // Serial.print(JointsInfo[i].StepPerDeg);

    // Serial.print(" Pos J delta ");
    // Serial.println(robot[i].PosJDelta);

    // delay(50);


    if (robot[i].PosJDelta < 0){
      digitalWrite(motors[i].dir_pin, ((JointsInfo[i].DirJoint == 0) ? HIGH : LOW));
    }
    if (robot[i].PosJDelta > 0){
      digitalWrite(motors[i].dir_pin, ((JointsInfo[i].DirJoint == 1) ? HIGH : LOW));
    }
    robot[i].PosJDelta = abs(robot[i].PosJDelta);
    if (robot[i].PosJDelta/JointsInfo[i].StepPerDeg > maxDeg){
      maxDeg = robot[i].PosJDelta/JointsInfo[i].StepPerDeg;
      JointMaxDeg = i;
    }
    if (robot[i].PosJDelta > maxSteps){
      maxSteps = robot[i].PosJDelta;
      JointMaxMove = i;
    }

  }

  // Serial.println(maxSteps);

  float ACC = (ACC1/100) * JointsInfo[JointMaxDeg].MaxAccel;
  float VEL = (VEL1/100) * JointsInfo[JointMaxDeg].MaxSpeed * JointsInfo[JointMaxDeg].StepPerDeg;

  long Max_delay = 1000000/VEL;
  // Serial.print("VEL 1: ");
  // Serial.println(VEL);

  // calculate the percentage of move of each joint compared to the maximum joint movement
  float percentage[NUMBER_OF_JOINTS];
  for (int i = 0; i < NUMBER_OF_JOINTS; i++){
    if ((float)robot[i].PosJDelta/maxSteps < 0.01) {
      percentage[i] = 0.01;
    }
    else{
      percentage[i] = (float)robot[i].PosJDelta/maxSteps;  // percentyage of aantal graden
    }
    // Serial.print("pos J delta ");
    // Serial.print(robot[i].PosJDelta);
    // Serial.print(", maxsteps ");
    // Serial.println(maxSteps);
    // Serial.print(i);
    // Serial.print(") percentage: ");
    // Serial.println(percentage[i]);
  }  

  int JointMaxSpeed = JointMaxMove;
  // look if the speed is higher than the maximum speed of each joint
  for (int i = 0; i < NUMBER_OF_JOINTS; i++){
    if ((percentage[i] * VEL) > (JointsInfo[i].MaxSpeed * JointsInfo[i].StepPerDeg * (VEL1 / 100))){
      JointMaxSpeed = i;
      VEL = (VEL1/100) * (JointsInfo[JointMaxSpeed].MaxSpeed/percentage[JointMaxSpeed]) * JointsInfo[JointMaxSpeed].StepPerDeg;
      // Serial.println(VEL);

      // Serial.println(JointsInfo[JointMaxSpeed].MaxSpeed);
      // Serial.println(percentage[i]);
      // Serial.println(JointsInfo[JointMaxSpeed].StepPerDeg);

      ACC = (ACC1/100) * JointsInfo[JointMaxSpeed].MaxAccel;
      Max_delay = 1000000/VEL;
      // Serial.print("snelheid aangepast aan joint ");
      // Serial.print(i);
      // Serial.print(") VEL: ");
      // Serial.println(VEL);
    }
  }

  long AB = 0;
  long CD = 0;
  float ACCt = 0;
  float DACCt = 0;

  if (VEL == VEL_0){
    ACCt = 0;
    AB = 0;
  }
  else{
    ACCt = (VEL - VEL_0)/ACC;
    AB = (VEL_0 * ACCt)+((ACCt*(VEL-VEL_0))/2);
  }

  if (VEL == VEL_1){
    DACCt = 0;
    CD = 0;
  }
  else{
    DACCt = (VEL - VEL_1)/ACC;
    CD =(VEL_1*DACCt)+((DACCt*(VEL-VEL_1))/2);
  }

  // if the acceleration takes longer than the max steps
  if ((AB + CD) > robot[JointMaxSpeed].PosJDelta)
  {
    AB = (((VEL-VEL_0)/VEL)/((VEL-VEL_0)/VEL+(VEL-VEL_1)/VEL))*robot[JointMaxSpeed].PosJDelta;
    CD = (((VEL-VEL_1)/VEL)/((VEL-VEL_0)/VEL+(VEL-VEL_1)/VEL))*robot[JointMaxSpeed].PosJDelta;
  }


  long over[NUMBER_OF_JOINTS];
  for (int i = 0; i < NUMBER_OF_JOINTS; i++){
    over[i] = maxSteps / 2;
  }

  // start delay
  long Start_delay;
  if (VEL_0 == 0) Start_delay = Max_delay * 5;
  else Start_delay = Max_delay;//1000000/(JointsInfo[axis_vel_max_move].StepPerDeg * VEL_0);

  // end delay
  long End_delay;
  if (VEL_1 == 0) End_delay = Max_delay * 5;
  else End_delay = Max_delay;//1000000/(JointsInfo[axis_vel_max_move].StepPerDeg * VEL_0);

  // calculate how many steps is to take to accelerate
  float AccelIncrease = static_cast<float>(Start_delay - Max_delay) / AB;
  float DecelDecrease = static_cast<float>(End_delay - Max_delay) / CD;

  float curDelay = Start_delay; // the current delay is the start delay

  // for loop
  long steps_to_do = maxSteps;

  // Serial.println(curDelay);

  if (curDelay > 500000){
    curDelay = 3000;
  }

  // for (int k = 0; k < NUMBER_OF_JOINTS; k++){
  //   Serial.println(motors[k].step_pin);
  // }

  for (int i = 0; i < maxSteps; i++){
    if(stop == 1){    // when the stop button is pressed go out of this for loop
      break;
    }
    
    while(pauze){  // when the pauze button is pressed wait until the the play button is pressed or break if the stop button is pressed
      delay(10);
      if(stop == 1) break;
    }  

    for (int k = 0; k < NUMBER_OF_JOINTS; k++){
      digitalWrite(motors[k].step_pin,HIGH);
    }
    delayMicroseconds(curDelay / 2);
    for (int j = 0; j < NUMBER_OF_JOINTS; j++){
      over[j] += robot[j].PosJDelta; 
      if (over[j] >= maxSteps){
        over[j] -= maxSteps;   
        digitalWrite(motors[j].step_pin,LOW);
      }
    }
    if (i < AB){
      curDelay -= AccelIncrease;
    }
    else if (i > (maxSteps - CD)){
      curDelay += DecelDecrease;
    }
    delayMicroseconds(curDelay / 2);
    steps_to_do--;

    if (deviceDisconnected){
      break;
    }

  }

  // calculate the current position when the stop button is pressed
  if(stop == 1){
    // Serial.println("Program stopped");

    float pos_done;
    for (int i = 0; i < NUMBER_OF_JOINTS; i++){
      pos_done = ((float(maxSteps - steps_to_do) / maxSteps) * robot[i].PosJDelta)/JointsInfo[i].StepPerDeg;  
      if (robot[i].PosJStart < robot[i].PosJEnd){
        robot[i].PosJEnd = robot[i].PosJStart + pos_done;
      }
      else{
        robot[i].PosJEnd = robot[i].PosJStart - pos_done;
      }
    }
    if(NUMBER_OF_JOINTS == 6){
      ForwardKinematic_6_PosEnd();
    }
    if(NUMBER_OF_JOINTS == 3){
      ForwardKinematic_3_PosEnd();
    }

  }

  // position start is now position begining
  for (int i = 0; i < NUMBER_OF_JOINTS; i++){
    robot[i].PosJStart = robot[i].PosJEnd;

  }
}