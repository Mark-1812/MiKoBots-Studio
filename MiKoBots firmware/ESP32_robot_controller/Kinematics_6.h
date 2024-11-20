#include "Variables.h"
extern int check_for_error();


// // //DECLARE TOOL FRAME
// extern double toolFrame[4][4];
// extern float toolFrameRev[4][4];


// extern float R06_neg_matrix[4][4]{};


// // //DECLARE JOINT MATRICES
// extern double JointMatrix[6][4][4];

// extern float J1matrix_rev[4][4];
// extern float J2matrix_rev[4][4];
// extern float J3matrix_rev[4][4];

// extern double R02matrix[4][4];
// extern double R03matrix[4][4];
// extern double R04matrix[4][4];
// extern double R05matrix[4][4];
// extern double R06matrix[4][4];
// extern double R0Tmatrix[4][4];

// extern float R02matrix_rev[4][4];
// extern float R03matrix_rev[4][4];

// extern float R0T_rev_matrix[4][4];
// extern float InvtoolFrame[4][4];
// extern float R06_rev_matrix[4][4];
// extern float R05_rev_matrix[4][4];
// extern float InvR03matrix_rev[4][4];
// extern float R03_6matrix[4][4];

// extern float blank[4][4];

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//CONSTRUCT DH MATRICES FORWARD KINEMATICS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void DH_Matrices_6() {
  for(int i = 0; i < 6; i++){
    if (robot[i].PosJEnd == 0) {
      robot[i].PosJEnd = .001;
    }    
  }

  

  for(int i = 0; i < 6; i++){
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

void FwdMatrices_6() {
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
      R05matrix[j][i] = 0;
    }
  }
  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R06matrix[j][i] = 0;
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
        R05matrix[k][i] = R05matrix[k][i] + (R04matrix[k][j] * JointMatrix[4][j][i]);
      }
    }
  }
  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R06matrix[k][i] = R06matrix[k][i] + (R05matrix[k][j] * JointMatrix[5][j][i]);
      }
    }
  }
  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R0Tmatrix[k][i] = R0Tmatrix[k][i] + (R06matrix[k][j] * toolFrame[j][i]);
      }
    }
  }
}



void ForwardKinematic_6_PosEnd() {

  DH_Matrices_6();
  FwdMatrices_6();

  robot[0].PosEnd = R0Tmatrix[0][3];
  robot[1].PosEnd = R0Tmatrix[1][3];
  robot[2].PosEnd = R0Tmatrix[2][3];
  robot[4].PosEnd = atan2(-R0Tmatrix[2][0], pow((pow(R0Tmatrix[2][1], 2) + pow(R0Tmatrix[2][2], 2)), 0.5));
  robot[3].PosEnd = degrees(atan2(R0Tmatrix[1][0] / cos(robot[4].PosEnd), R0Tmatrix[0][0] / cos(robot[4].PosEnd)));
  robot[5].PosEnd = degrees(atan2(R0Tmatrix[2][1] / cos(robot[4].PosEnd), R0Tmatrix[2][2] / cos(robot[4].PosEnd)));
  robot[4].PosEnd = degrees(robot[4].PosEnd);
}

void ForwardKinematic_6_PosStart() {

  DH_Matrices_6();
  FwdMatrices_6();

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

void InverseKinematic_6() {
  String WristCon;

  if (robot[4].PosJStart > 0){
    WristCon = "F";
  }else{
    WristCon = "N";
  }

  float pX;
  float pY;
  float pX_a1_fwd;
  float pX_a1_mid;
  float pa2H_fwd;
  float pa2H_mid;
  float pa3H;
  float thetaA_fwd;
  float thetaA_mid;
  float thetaB_fwd;
  float thetaB_mid;
  float thetaC_fwd;
  float thetaC_mid;
  float thetaD;
  float thetaE;

  float XatJ1zero;
  float YatJ1zero;
  float Length_1;
  float Length_2;
  float Length_3;
  float Length_4;
  float Theta_A;
  float Theta_B;
  float Theta_C;
  float Theta_D;
  float Theta_E;


  int i, j, k = 0;
  KinematicError = 0;

  //generate matrices for center of spherical wrist location

  R0T_rev_matrix[0][0] = cos(radians(robot[3].PosEnd)) * cos(radians(robot[4].PosEnd));
  R0T_rev_matrix[0][1] = cos(radians(robot[3].PosEnd)) * sin(radians(robot[4].PosEnd)) * sin(radians(robot[5].PosEnd)) - sin(radians(robot[3].PosEnd)) * cos(radians(robot[5].PosEnd));
  R0T_rev_matrix[0][2] = cos(radians(robot[3].PosEnd)) * sin(radians(robot[4].PosEnd)) * cos(radians(robot[5].PosEnd)) + sin(radians(robot[3].PosEnd)) * sin(radians(robot[5].PosEnd));
  R0T_rev_matrix[0][3] = robot[0].PosEnd;
  R0T_rev_matrix[1][0] = sin(radians(robot[3].PosEnd)) * cos(radians(robot[4].PosEnd));
  R0T_rev_matrix[1][1] = sin(radians(robot[3].PosEnd)) * sin(radians(robot[4].PosEnd)) * sin(radians(robot[5].PosEnd)) + cos(radians(robot[3].PosEnd)) * cos(radians(robot[5].PosEnd));
  R0T_rev_matrix[1][2] = sin(radians(robot[3].PosEnd)) * sin(radians(robot[4].PosEnd)) * cos(radians(robot[5].PosEnd)) - cos(radians(robot[3].PosEnd)) * sin(radians(robot[5].PosEnd));
  R0T_rev_matrix[1][3] = robot[1].PosEnd;
  R0T_rev_matrix[2][0] = -sin(radians(robot[4].PosEnd));
  R0T_rev_matrix[2][1] = cos(radians(robot[4].PosEnd)) * sin(radians(robot[5].PosEnd));
  R0T_rev_matrix[2][2] = cos(radians(robot[4].PosEnd)) * cos(radians(robot[5].PosEnd));
  R0T_rev_matrix[2][3] = robot[2].PosEnd;
  R0T_rev_matrix[3][0] = 0;
  R0T_rev_matrix[3][1] = 0;
  R0T_rev_matrix[3][2] = 0;
  R0T_rev_matrix[3][3] = 1;

  

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

  InvtoolFrame[0][0] = toolFrame[0][0];
  InvtoolFrame[0][1] = toolFrame[1][0];
  InvtoolFrame[0][2] = toolFrame[2][0];
  InvtoolFrame[0][3] = -TOOL_FRAME[0];
  InvtoolFrame[1][0] = toolFrame[0][1];
  InvtoolFrame[1][1] = toolFrame[1][1];
  InvtoolFrame[1][2] = toolFrame[2][1];
  InvtoolFrame[1][3] = -TOOL_FRAME[1];
  InvtoolFrame[2][0] = toolFrame[0][2];
  InvtoolFrame[2][1] = toolFrame[1][2];
  InvtoolFrame[2][2] = toolFrame[2][2];
  InvtoolFrame[2][3] = -TOOL_FRAME[2];
  InvtoolFrame[3][0] = 0;
  InvtoolFrame[3][1] = 0;
  InvtoolFrame[3][2] = 0;
  InvtoolFrame[3][3] = 1; 

  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R06_rev_matrix[j][i] = 0;
    }
  }

  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R05_rev_matrix[j][i] = 0;
    }
  }

  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R02matrix_rev[j][i] = 0;
    }
  }

  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R03matrix_rev[j][i] = 0;
    }
  }

  for (int j = 0; j < 4; j++) {
    for (int i = 0; i < 4; i++) {
      R03_6matrix[j][i] = 0;
    }
  }

  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R06_rev_matrix[k][i] = R06_rev_matrix[k][i] + (R0T_rev_matrix[k][j] * InvtoolFrame[j][i]);
      }
    }
  }

  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R05_rev_matrix[k][i] = R05_rev_matrix[k][i] + (R06_rev_matrix[k][j] * R06_neg_matrix[j][i]);
      }
    }
  }

 /* Serial.println("R05 rev matrix:");
  for (int i= 0; i < 4; i++){
    for (int j = 0; j < 4; j++){
      Serial.print(R05_rev_matrix[i][j]);
      Serial.print(" ");
    }
    Serial.println("");
  }

  
  //Serial.println(degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3])));
  // Serial.println(degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3])));
  //Serial.println(-180 + degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3])));
  //Serial.println(180 + degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3])));
  */
  if (R05_rev_matrix[0][3] >= 0 and R05_rev_matrix[1][3] > 0) {
    robot[0].PosJEnd = degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]));
  } else if (R05_rev_matrix[0][3] >= 0 and R05_rev_matrix[1][3] <= 0) {
    robot[0].PosJEnd = degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]));
  } else if (R05_rev_matrix[0][3] < 0 and R05_rev_matrix[1][3] <= 0) {
    robot[0].PosJEnd = -180 + degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]));
  } else if (R05_rev_matrix[0][3] <= 0 and R05_rev_matrix[1][3] > 0) {
    robot[0].PosJEnd = 180 + degrees(atan(R05_rev_matrix[1][3] / R05_rev_matrix[0][3]));
  }

  //calculate J2 & J3 geometry

  XatJ1zero = (R05_rev_matrix[0][3] * cos(radians(-robot[0].PosJEnd))) - (R05_rev_matrix[1][3] * sin(radians(-robot[0].PosJEnd)));
  YatJ1zero = 0;

  Length_1 = abs(XatJ1zero - DHparams[0][3]);
  //Serial.println(Length_1);
  Length_2 = sqrt(pow((XatJ1zero - DHparams[0][3]), 2) + pow((YatJ1zero - YatJ1zero), 2) + pow((R05_rev_matrix[2][3] - DHparams[0][2]), 2));
  //Serial.println(Length_2);
  Length_3 = sqrt(pow(DHparams[3][2], 2) + pow(DHparams[2][3], 2));
  //Serial.println(Length_3);
  Length_4 = R05_rev_matrix[2][3] - DHparams[0][2];
  //Serial.println(Length_4);
  Theta_B = degrees(atan(Length_1 / Length_4));
  Theta_C = degrees(acos((pow(DHparams[1][3], 2) + pow(Length_2, 2) - pow(Length_3, 2)) / (2 * DHparams[1][3] * Length_2)));
  Theta_D = degrees(acos((pow(Length_3, 2) + pow(DHparams[1][3], 2) - pow(Length_2, 2)) / (2 * Length_3 * DHparams[1][3])));
  Theta_E = degrees(atan(DHparams[2][3] / DHparams[3][2]));

  // calc J2 angle

  // robot[1].PosJEnd = Theta_B - Theta_C;
  // Serial.print("1: ");
  // Serial.println(robot[1].PosJEnd);

  // robot[1].PosJEnd = Theta_B - Theta_C + 180;
  // Serial.print("2: ");
  // Serial.println(robot[1].PosJEnd);

  // robot[1].PosJEnd = -(Theta_B + Theta_C);
  // Serial.print("3: ");
  // Serial.println(robot[1].PosJEnd);

  // Serial.print("Theta_B ");
  // Serial.println(Theta_B);

  // Serial.print("Theta_C ");
  // Serial.println(Theta_C);

  // Serial.print("Length_4 ");
  // Serial.println(Length_4);  

  if (XatJ1zero > DHparams[0][3]) {
    if (Length_4 >= 0) {
      robot[1].PosJEnd = Theta_B - Theta_C;
      // Serial.print("1: ");
      // Serial.println(robot[1].PosJEnd);
    } else {
      robot[1].PosJEnd = Theta_B - Theta_C + 180;
      // Serial.print("2: ");
      // Serial.println(robot[1].PosJEnd);
    }
  } else {
    robot[1].PosJEnd = -(Theta_B + Theta_C);
  }

  // calc J3 angle

  robot[2].PosJEnd = -(Theta_D + Theta_E) + 90;


  // generate reverse matrices for wrist orientaion

  J1matrix_rev[0][0] = cos(radians(robot[0].PosJEnd + DHparams[0][0]));
  J1matrix_rev[0][1] = -sin(radians(robot[0].PosJEnd + DHparams[0][0])) * cos(radians(DHparams[0][1]));
  J1matrix_rev[0][2] = sin(radians(robot[0].PosJEnd + DHparams[0][0])) * sin(radians(DHparams[0][1]));
  J1matrix_rev[0][3] = DHparams[0][3] * cos(radians(robot[0].PosJEnd + DHparams[0][0]));
  J1matrix_rev[1][0] = sin(radians(robot[0].PosJEnd + DHparams[0][0]));
  J1matrix_rev[1][1] = cos(radians(robot[0].PosJEnd + DHparams[0][0])) * cos(radians(DHparams[0][1]));
  J1matrix_rev[1][2] = -cos(radians(robot[0].PosJEnd + DHparams[0][0])) * sin(radians(DHparams[0][1]));
  J1matrix_rev[1][3] = DHparams[0][3] * sin(radians(robot[0].PosJEnd + DHparams[0][0]));
  J1matrix_rev[2][0] = 0;
  J1matrix_rev[2][1] = sin(radians(DHparams[0][1]));
  J1matrix_rev[2][2] = cos(radians(DHparams[0][1]));
  J1matrix_rev[2][3] = DHparams[0][2];
  J1matrix_rev[3][0] = 0;
  J1matrix_rev[3][1] = 0;
  J1matrix_rev[3][2] = 0;
  J1matrix_rev[3][3] = 1;

  J2matrix_rev[0][0] = cos(radians(robot[1].PosJEnd + DHparams[1][0]));
  J2matrix_rev[0][1] = -sin(radians(robot[1].PosJEnd + DHparams[1][0])) * cos(radians(DHparams[1][1]));
  J2matrix_rev[0][2] = sin(radians(robot[1].PosJEnd + DHparams[1][0])) * sin(radians(DHparams[1][1]));
  J2matrix_rev[0][3] = DHparams[1][3] * cos(radians(robot[1].PosJEnd + DHparams[1][0]));
  J2matrix_rev[1][0] = sin(radians(robot[1].PosJEnd + DHparams[1][0]));
  J2matrix_rev[1][1] = cos(radians(robot[1].PosJEnd + DHparams[1][0])) * cos(radians(DHparams[1][1]));
  J2matrix_rev[1][2] = -cos(radians(robot[1].PosJEnd + DHparams[1][0])) * sin(radians(DHparams[1][1]));
  J2matrix_rev[1][3] = DHparams[1][3] * sin(radians(robot[1].PosJEnd + DHparams[1][0]));
  J2matrix_rev[2][0] = 0;
  J2matrix_rev[2][1] = sin(radians(DHparams[1][1]));
  J2matrix_rev[2][2] = cos(radians(DHparams[1][1]));
  J2matrix_rev[2][3] = DHparams[1][2];
  J2matrix_rev[3][0] = 0;
  J2matrix_rev[3][1] = 0;
  J2matrix_rev[3][2] = 0;
  J2matrix_rev[3][3] = 1;

  J3matrix_rev[0][0] = cos(radians(robot[2].PosJEnd + DHparams[2][0]));
  J3matrix_rev[0][1] = -sin(radians(robot[2].PosJEnd + DHparams[2][0])) * cos(radians(DHparams[2][1]));
  J3matrix_rev[0][2] = sin(radians(robot[2].PosJEnd + DHparams[2][0])) * sin(radians(DHparams[2][1]));
  J3matrix_rev[0][3] = DHparams[2][3] * cos(radians(robot[2].PosJEnd + DHparams[2][0]));
  J3matrix_rev[1][0] = sin(radians(robot[2].PosJEnd + DHparams[2][0]));
  J3matrix_rev[1][1] = cos(radians(robot[2].PosJEnd + DHparams[2][0])) * cos(radians(DHparams[2][1]));
  J3matrix_rev[1][2] = -cos(radians(robot[2].PosJEnd + DHparams[2][0])) * sin(radians(DHparams[2][1]));
  J3matrix_rev[1][3] = DHparams[2][3] * sin(radians(robot[2].PosJEnd + DHparams[2][0]));
  J3matrix_rev[2][0] = 0;
  J3matrix_rev[2][1] = sin(radians(DHparams[2][1]));
  J3matrix_rev[2][2] = cos(radians(DHparams[2][1]));
  J3matrix_rev[2][3] = DHparams[2][2];
  J3matrix_rev[3][0] = 0;
  J3matrix_rev[3][1] = 0;
  J3matrix_rev[3][2] = 0;
  J3matrix_rev[3][3] = 1;

  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R02matrix_rev[k][i] = R02matrix_rev[k][i] + (J1matrix_rev[k][j] * J2matrix_rev[j][i]);
      }
    }
  }
  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R03matrix_rev[k][i] = R03matrix_rev[k][i] + (R02matrix_rev[k][j] * J3matrix_rev[j][i]);
      }
    }
  }

  InvR03matrix_rev[0][0] = R03matrix_rev[0][0];
  InvR03matrix_rev[0][1] = R03matrix_rev[1][0];
  InvR03matrix_rev[0][2] = R03matrix_rev[2][0];
  InvR03matrix_rev[1][0] = R03matrix_rev[0][1];
  InvR03matrix_rev[1][1] = R03matrix_rev[1][1];
  InvR03matrix_rev[1][2] = R03matrix_rev[2][1];
  InvR03matrix_rev[2][0] = R03matrix_rev[0][2];
  InvR03matrix_rev[2][1] = R03matrix_rev[1][2];
  InvR03matrix_rev[2][2] = R03matrix_rev[2][2];

  for (int k = 0; k < 4; k++) {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        R03_6matrix[k][i] = R03_6matrix[k][i] + (InvR03matrix_rev[k][j] * R06_rev_matrix[j][i]);
      }
    }
  }


  /*for (int k = 0; k < 4; k++) {
    Serial.print("[");
    for (int i = 0; i < 4; i++) {
      Serial.print(R03_6matrix[k][i]);
      Serial.print(", ");
    }
    Serial.println("]");
  }*/


  //calculate J5 angle
  if (WristCon == "F") {
    robot[4].PosJEnd = degrees(atan2(sqrt(1 - pow(R03_6matrix[2][2], 2)), R03_6matrix[2][2]));
  } else {
    robot[4].PosJEnd = -degrees(atan2(-sqrt(1 - pow(R03_6matrix[2][2], 2)), R03_6matrix[2][2]));
  }

  //calculate J4 angle

  if (robot[4].PosJEnd < 0) {
    robot[3].PosJEnd  = degrees(atan2(R03_6matrix[1][2], R03_6matrix[0][2]));
  } 
  else {
    robot[3].PosJEnd  = degrees(atan2(-R03_6matrix[1][2], R03_6matrix[0][2]));
  }

  //calculate J6 angle

  if (robot[4].PosJEnd < 0) {
    robot[5].PosJEnd = degrees(atan2(R03_6matrix[2][1], R03_6matrix[2][0]));
  } 
  else 
  {
    robot[5].PosJEnd = degrees(atan2(-R03_6matrix[2][1], -R03_6matrix[2][0]));
  }




  //error = check_for_error();

  if (error){
    for(int i = 0; i < NUMBER_OF_JOINTS; i++){
      robot[i].PosJEnd = robot[i].PosJStart;
      robot[i].PosEnd = robot[i].PosStart;
    }
  }

}