#include "Variables.h"
extern int check_for_error();




void FwdMatrices_3() {

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (robot[i].PosJEnd == 0) {
      robot[i].PosJEnd = .001;
    }    
  }

  resetMatrix(T);  



  for(int i = 0; i < 4; i++){
    float dh_param[4] = {DHparams[i][0], DHparams[i][1], DHparams[i][2], DHparams[i][3]};

    if (i == 3){
      dh_param[0] = dh_param[0] - ((DHparams[1][0] + robot[1].PosJEnd) + (DHparams[2][0] + robot[2].PosJEnd- robot[1].PosJEnd));
    }
    else if (i == 2){
      dh_param[0] = dh_param[0] + robot[i].PosJEnd - robot[1].PosJEnd;
    }
    else{
      dh_param[0] = dh_param[0] + robot[i].PosJEnd;
    }

    

    T_i[0][0] = cos(radians(dh_param[0]));
    T_i[0][1] = -sin(radians(dh_param[0])) * cos(radians(dh_param[1]));
    T_i[0][2] = sin(radians(dh_param[0])) * sin(radians(dh_param[1]));
    T_i[0][3] = dh_param[3] * cos(radians(dh_param[0]));
    T_i[1][0] = sin(radians(dh_param[0]));
    T_i[1][1] = cos(radians(dh_param[0])) * cos(radians(dh_param[1]));
    T_i[1][2] = -cos(radians(dh_param[0])) * sin(radians(dh_param[1]));
    T_i[1][3] = dh_param[3] * sin(radians(dh_param[0]));
    T_i[2][0] = 0;
    T_i[2][1] = sin(radians(dh_param[1]));
    T_i[2][2] = cos(radians(dh_param[1]));
    T_i[2][3] = dh_param[2];
    T_i[3][0] = 0;
    T_i[3][1] = 0;
    T_i[3][2] = 0;
    T_i[3][3] = 1;

    matrixMultiply(T, T_i, result);

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            T[i][j] = result[i][j];
        }
    }

  }

  tool_matrix();
  
  matrixMultiply(T, toolFrame, result);

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      T[i][j] = result[i][j];
    }
  }



}

void ForwardKinematic_3_PosEnd() {
  FwdMatrices_3();

  robot[0].PosEnd = T[0][3];
  robot[1].PosEnd = T[1][3];
  robot[2].PosEnd = T[2][3];
  robot[4].PosEnd = atan2(-T[2][0], pow((pow(T[2][1], 2) + pow(T[2][2], 2)), 0.5));
  robot[3].PosEnd = degrees(atan2(T[1][0] / cos(robot[4].PosEnd), T[0][0] / cos(robot[4].PosEnd)));
  robot[5].PosEnd = degrees(atan2(T[2][1] / cos(robot[4].PosEnd), T[2][2] / cos(robot[4].PosEnd)));
  robot[4].PosEnd = degrees(robot[4].PosEnd);
}

void ForwardKinematic_3_PosStart() {
  FwdMatrices_3();

  robot[0].PosStart = T[0][3];
  robot[1].PosStart = T[1][3];
  robot[2].PosStart = T[2][3];
  robot[4].PosStart = atan2(-T[2][0], pow((pow(T[2][1], 2) + pow(T[2][2], 2)), 0.5));
  robot[3].PosStart = degrees(atan2(T[1][0] / cos(robot[4].PosStart), T[0][0] / cos(robot[4].PosStart)));
  robot[5].PosStart = degrees(atan2(T[2][1] / cos(robot[4].PosStart), T[2][2] / cos(robot[4].PosStart)));
  robot[4].PosStart = degrees(robot[4].PosStart);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//REVERSE KINEMATICS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void InverseKinematic_3() {
  /*
  Serial.println("solve kine ");

  Serial.println("POS START");
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    Serial.print(robot[i].PosStart);
    Serial.print(", ");
  }
  Serial.println("");

  Serial.println("POS END");
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    Serial.print(robot[i].PosEnd);
    Serial.print(", ");
  }
  Serial.println("");

*/

  float tool_X = TOOL_FRAME[0];
  float tool_Y = TOOL_FRAME[1];
  float tool_Z = TOOL_FRAME[2];


  float X = robot[0].PosEnd - tool_X;
  float Y = robot[1].PosEnd - tool_Z;
  float Z = robot[2].PosEnd - tool_Y;

  float L1 = DHparams[0][2];
  float L2 = DHparams[1][3];
  float L3 = DHparams[2][3];
  float L4 = DHparams[3][3];



  float J1 = degrees(atan(Y / X));

  float r = sqrt(pow(X, 2) + pow(Y, 2)) - L4;
  float D = sqrt(pow((Z - L1), 2) + pow(r, 2));

  float a1 = acos((pow(D, 2) + pow(L2, 2) - pow(L3, 2)) / (2 * D * L2));
  float a2 = atan((Z - L1) / r);

  float J2 = degrees(a1) + degrees(a2) - 90;

  float J3 = acos((pow(D, 2) - pow(L3, 2) - pow(L2, 2)) / (2 * L3 * L2));
  J3 = 90 - degrees(J3) + J2;

  robot[0].PosJEnd = J1;
  robot[1].PosJEnd = J2;
  robot[2].PosJEnd = J3;
/*
  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    Serial.print(robot[i].PosJEnd);
    Serial.print(", ");
  }
  Serial.println("");
*/
  if (error){
    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJEnd = robot[i].PosJStart;
      robot[i].PosEnd = robot[i].PosStart;
    }
  }

}