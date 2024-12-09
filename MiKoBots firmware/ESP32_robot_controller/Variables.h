#ifndef VARIABLES_H
#define VARIABLES_H

//DECLARE TOOL FRAME
extern float toolFrame[4][4];
extern float toolFrameRev[4][4];


extern float R06_neg_matrix[4][4];


//DECLARE JOINT MATRICES
extern double JointMatrix[6][4][4];

extern float J1matrix_rev[4][4];
extern float J2matrix_rev[4][4];
extern float J3matrix_rev[4][4];

extern double R02matrix[4][4];
extern double R03matrix[4][4];
extern double R04matrix[4][4];
extern double R05matrix[4][4];
extern double R06matrix[4][4];
extern double R0Tmatrix[4][4];

extern float R02matrix_rev[4][4];
extern float R03matrix_rev[4][4];

extern float R0T_rev_matrix[4][4];
extern float InvtoolFrame[4][4];
extern float R06_rev_matrix[4][4];
extern float R05_rev_matrix[4][4];
extern float InvR03matrix_rev[4][4];
extern float R03_6matrix[4][4];


extern float blank[4][4];

#endif