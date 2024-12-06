#include "Variables.h"
extern int check_for_error();

// // //DECLARE TOOL FRAME
// extern double toolFrame[4][4];
// extern float R06_neg_matrix[4][4];

// // //DECLARE JOINT MATRICES
// extern double JointMatrix[4][4][4]

// extern float J1matrix_rev[4][4];
// extern float J2matrix_rev[4][4];
// extern float J3matrix_rev[4][4];

// extern double R02matrix[4][4];
// extern double R03matrix[4][4];
// extern double R04matrix[4][4];
// extern double R0Tmatrix[4][4];

// extern float R02matrix_rev[4][4];
// extern float R03matrix_rev[4][4];

// extern float R0T_rev_matrix[4][4];
// extern float InvtoolFrame[4][4];
// extern float InvR03matrix_rev[4][4];

// extern float blank[4][4];

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//CONSTRUCT DH MATRICES FORWARD KINEMATICS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void DH_Matrices_3() {

  for(int i = 0; i < NUMBER_OF_JOINTS; i++){
    if (robot[i].PosJEnd == 0) {
      robot[i].PosJEnd = .001;
    }    
  }

  for(int i = 0; i < 4; i++){
    JointMatrix[i][0][0] = cos(radians(robot[i].PosJEnd + DHparams[i][0]));
    JointMatrix[i][0][1] = -sin(radians(robot[i].PosJEnd + DHparams[i][0])) * cos(radians(DHparams[i][1]));
    JointMatrix[i][0][2] = sin(radians(robot[i].PosJEnd + DHparams[i][0])) * sin(radians(DHparams[i][1]));
    JointMatrix[i][0][3] = DHparams[i][3] * cos(radians(robot[i].PosJEnd + DHparams[i][0]));
    JointMatrix[i][1][0] = sin(radians(robot[i].PosJEnd + DHparams[i][0]));
    JointMatrix[i][1][1] = cos(radians(robot[i].PosJEnd + DHparams[i][0])) * cos(radians(DHparams[i][1]));
    JointMatrix[i][1][2] = -cos(radians(robot[i].PosJEnd + DHparams[i][0])) * sin(radians(DHparams[i][1]));
    JointMatrix[i][1][3] = DHparams[i][3] * sin(radians(robot[i].PosJEnd + DHparams[i][0]));
    JointMatrix[i][2][0] = 0;
    JointMatrix[i][2][1] = sin(radians(DHparams[i][1]));
    JointMatrix[i][2][2] = cos(radians(DHparams[i][1]));
    JointMatrix[i][2][3] = DHparams[i][2];
    JointMatrix[i][3][0] = 0;
    JointMatrix[i][3][1] = 0;
    JointMatrix[i][3][2] = 0;
    JointMatrix[i][3][3] = 1;
  }

  toolFrame[0][0] = cos(radians(TOOL_FRAME[3])) * cos(radians(TOOL_FRAME[4]));
  toolFrame[0][1] = cos(radians(TOOL_FRAME[3])) * sin(radians(TOOL_FRAME[4])) * sin(radians(TOOL_FRAME[5]));
  toolFrame[0][2] = cos(radians(TOOL_FRAME[3])) * sin(radians(TOOL_FRAME[4])) * cos(radians(TOOL_FRAME[5])) + sin(radians(TOOL_FRAME[3])) * sin(radians(TOOL_FRAME[5]));
  toolFrame[0][3] = TOOL_FRAME[0];
  toolFrame[1][0] = sin(radians(TOOL_FRAME[3])) * cos(radians(TOOL_FRAME[4]));
  toolFrame[1][1] = sin(radians(TOOL_FRAME[3])) * sin(radians(TOOL_FRAME[4])) * sin(radians(TOOL_FRAME[5])) + cos(radians(TOOL_FRAME[3])) * cos(radians(TOOL_FRAME[5]));
  toolFrame[1][2] = cos(radians(TOOL_FRAME[3])) * sin(radians(TOOL_FRAME[4])) * cos(radians(TOOL_FRAME[5])) - cos(radians(TOOL_FRAME[3])) * sin(radians(TOOL_FRAME[5]));
  toolFrame[1][3] = TOOL_FRAME[1];
  toolFrame[2][0] = -sin(radians(TOOL_FRAME[4]));
  toolFrame[2][1] = cos(radians(TOOL_FRAME[4])) * sin(radians(TOOL_FRAME[5]));
  toolFrame[2][2] = cos(radians(TOOL_FRAME[4])) * cos(radians(TOOL_FRAME[5]));
  toolFrame[2][3] = TOOL_FRAME[2];
  toolFrame[3][0] = 0;
  toolFrame[3][1] = 0;
  toolFrame[3][2] = 0;
  toolFrame[3][3] = 1;
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//CONSTRUCT ROTATION MATRICES FORWARD KINEMATICS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void FwdMatrices_3() {
  int i, j, k = 0;
  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R02matrix[j][i] = 0;
    }
  }
  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R03matrix[j][i] = 0;
    }
  }
  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R04matrix[j][i] = 0;
    }
  }
  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R0Tmatrix[j][i] = 0;
    }
  }

  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R02matrix[k][i] = R02matrix[k][i] + (JointMatrix[0][k][j] * JointMatrix[1][j][i]);
      }
    }
  }



  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R03matrix[k][i] = R03matrix[k][i] + (R02matrix[k][j] * JointMatrix[2][j][i]);
      }
    }
  }



  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R04matrix[k][i] = R04matrix[k][i] + (R03matrix[k][j] * JointMatrix[3][j][i]);
      }
    }
  }



  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R0Tmatrix[k][i] = R0Tmatrix[k][i] + (R04matrix[k][j] * toolFrame[j][i]);
      }
    }
  }
  /*
  Serial.println("R02matrix");
  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(R02matrix[i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  Serial.println("R03matrix");
  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(R03matrix[i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  Serial.println("R04matrix");
  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(R04matrix[i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  Serial.println("R0Tmatrix");
  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(R0Tmatrix[i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }
*/
}

void ForwardKinematic_3_PosEnd() {


  DH_Matrices_3();
  
  /*
  Serial.println("Forward kinematics 3");

  for(int i = 0; i < 4; i++){
    Serial.print(robot[i].PosJEnd);
    Serial.print(", ");
  }
  Serial.println("");

  Serial.println("DH param");
  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(DHparams[i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(JointMatrix[0][i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(JointMatrix[1][i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(JointMatrix[2][i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }

  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(JointMatrix[3][i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }


  for(int i = 0; i < 4; i++){
    Serial.print(i);
    Serial.print(" ");
    for(int j = 0; j < 4; j++){
      Serial.print(toolFrame[i][j]);
      Serial.print(", ");
    }
    Serial.println("");
  }
  */
  FwdMatrices_3();

  robot[0].PosEnd = R0Tmatrix[0][3];
  robot[1].PosEnd = R0Tmatrix[1][3];
  robot[2].PosEnd = R0Tmatrix[2][3];
  robot[4].PosEnd = atan2(-R0Tmatrix[2][0], pow((pow(R0Tmatrix[2][1], 2) + pow(R0Tmatrix[2][2], 2)), 0.5));
  robot[3].PosEnd = degrees(atan2(R0Tmatrix[1][0] / cos(robot[4].PosEnd), R0Tmatrix[0][0] / cos(robot[4].PosEnd)));
  robot[5].PosEnd = degrees(atan2(R0Tmatrix[2][1] / cos(robot[4].PosEnd), R0Tmatrix[2][2] / cos(robot[4].PosEnd)));
  robot[4].PosEnd = degrees(robot[4].PosEnd);
}

void ForwardKinematic_3_PosStart() {

  DH_Matrices_3();
  FwdMatrices_3();

  robot[0].PosStart = R0Tmatrix[0][3];
  robot[1].PosStart = R0Tmatrix[1][3];
  robot[2].PosStart = R0Tmatrix[2][3];
  robot[4].PosStart = atan2(-R0Tmatrix[2][0], pow((pow(R0Tmatrix[2][1], 2) + pow(R0Tmatrix[2][2], 2)), 0.5));
  robot[3].PosStart = degrees(atan2(R0Tmatrix[1][0] / cos(robot[4].PosStart), R0Tmatrix[0][0] / cos(robot[4].PosStart)));
  robot[5].PosStart = degrees(atan2(R0Tmatrix[2][1] / cos(robot[4].PosStart), R0Tmatrix[2][2] / cos(robot[4].PosStart)));
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