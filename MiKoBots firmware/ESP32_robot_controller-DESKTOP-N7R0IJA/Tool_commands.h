#ifndef Tool_commands_H
#define Tool_commands_H

void sent_message(String message);


void set_TOOL();
void set_tool_frame();

void tool_state();
void tool_move_to();

// Settings Tool
void set_TOOL(String command){
  /*
    Tool pin
    Relay 0 or 1 
    Servo min
    Servo max
  */

  int pos_1_TOOL = command.indexOf('A');
  int pos_2_TOOL = command.indexOf('B');
  int pos_3_TOOL = command.indexOf('C');
  int pos_4_TOOL = command.indexOf('D');

  tool_pin = command.substring(pos_1_TOOL + 1, pos_2_TOOL).toInt();
  tool_type = command.substring(pos_2_TOOL + 1, pos_3_TOOL).toInt();
  servo_min = command.substring(pos_3_TOOL + 1, pos_4_TOOL).toInt();
  servo_max = command.substring(pos_4_TOOL + 1).toInt();

  if (tool_type == 0) {
    servoTool.attach(tool_pin);
  }

  if (tool_type == 1){
    pinMode(tool_pin, OUTPUT);
    digitalWrite(tool_pin, HIGH);
  }


  sent_message("TOOL is set");
  sent_message("END");
}

void set_tool_frame(String command){
  int pos_setting[12];

  for(int i = 0; i < 6; i++){
    pos_setting[i] = command.indexOf(alphabet[i]);
  }

  for(int i = 0; i < 6; i++){
    if (i < 6 - 1){
      TOOL_FRAME[i] = command.substring(pos_setting[i] + 1, pos_setting[i + 1]).toInt();
    } else{
      TOOL_FRAME[i] = command.substring(pos_setting[i] + 1).toInt();
    }
  }

  String message = "";
  for(int i = 0; i < 6; i++){
    message += TOOL_FRAME[i];
    message += ", ";
  }

  sent_message(message);

  sent_message("Tool frame is updated");
  sent_message("END");
}


// Functions tool
void tool_state(String command){
  int pos_1_TOOL = command.indexOf('(');
  int pos_2_TOOL = command.indexOf(')');
  String state = command.substring(pos_1_TOOL + 1, pos_2_TOOL);

  if (state.equals("LOW")){
    digitalWrite(tool_pin, HIGH);
  }
  else if (state.equals("HIGH")){
    digitalWrite(tool_pin, LOW);
  }

  String message = "Tool state " + state;
  sent_message(message);
  sent_message("END");
}

void tool_move_to(String command){
  int pos_1_TOOL = command.indexOf('(');
  int pos_2_TOOL = command.indexOf(')');
  int New_pos = command.substring(pos_1_TOOL + 1, pos_2_TOOL).toInt();

  float togo_pos = New_pos * ((servo_max - servo_min) / 100.0);

  if ((togo_pos - tool_pos) > 0){
    for (int pos = tool_pos; pos <= New_pos; pos += 1){
      delay(20);
      servoTool.write(pos);
    }
  }
  else{
    for (int pos = tool_pos; pos > New_pos; pos -= 1){
      delay(20);
      servoTool.write(pos);
    }
  }

  tool_pos = togo_pos;

  String message = "POS: G " + tool_pos;
  sent_message(message);
  sent_message("END");
}

#endif 