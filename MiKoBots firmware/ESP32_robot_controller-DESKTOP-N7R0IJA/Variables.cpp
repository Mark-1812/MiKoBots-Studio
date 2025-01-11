#include "variables.h"

//DECLARE TOOL FRAME
float toolFrame[4][4];
float toolFrameRev[4][4];


float R06_neg_matrix[4][4]{};


//DECLARE JOINT MATRICES
double JointMatrix[6][4][4];

float J1matrix_rev[4][4];
float J2matrix_rev[4][4];
float J3matrix_rev[4][4];

double R02matrix[4][4];
double R03matrix[4][4];
double R04matrix[4][4];
double R05matrix[4][4];
double R06matrix[4][4];
double R0Tmatrix[4][4];

float R02matrix_rev[4][4];
float R03matrix_rev[4][4];

float R0T_rev_matrix[4][4];
float InvtoolFrame[4][4];
float R06_rev_matrix[4][4];
float R05_rev_matrix[4][4];
float InvR03matrix_rev[4][4];
float R03_6matrix[4][4];


float blank[4][4];