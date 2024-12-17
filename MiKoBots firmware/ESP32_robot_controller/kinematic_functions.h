void tool_matrix() {
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

float T_i[4][4] = {
  {1, 0, 0, 1},
  {0, 1, 0, 2},
  {0, 0, 1, 3},
  {0, 0, 0, 1}
};

float T[4][4] = {
  {1, 0, 0, 0},
  {0, 1, 0, 0},
  {0, 0, 1, 0},
  {0, 0, 0, 1}
  };

float result[4][4];

void matrixMultiply(float A[4][4], float B[4][4], float C[4][4]) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            C[i][j] = 0;
            for (int k = 0; k < 4; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void resetMatrix(float T[4][4]) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            T[i][j] = (i == j) ? 1 : 0;  // Set diagonal elements to 1, others to 0
        }
    }
}