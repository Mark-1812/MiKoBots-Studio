int check_for_error(){
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if(robot[i].PosJEnd > JointsInfo[i].MaxPos){
      Serial.print(i);
      Serial.println("ERROR: destination is out of reach");
      return 1;
    }
    if(robot[i].PosJEnd < JointsInfo[i].MinPos){
      Serial.print(i);
      Serial.println("ERROR: destination is out of reach");
      return 1;
    }
    if(isnan(robot[i].PosJEnd)){
      Serial.println("ERROR: cannot calculate the joint angles for this position");
      return 1;
    }
  }
  return 0;
}