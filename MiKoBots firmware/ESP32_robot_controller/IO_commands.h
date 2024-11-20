#ifndef IO_commands_H
#define IO_commands_H

void set_IO_pin();
void IO_digitalWrite();

// Settings IO
void set_IO_pin(String command){
  int pos_IO_1_PIN = command.indexOf('A');
  int pos_IO_2_PIN = command.indexOf('B');
  int pos_IO_3_PIN = command.indexOf('C');

  int io_number = command.substring(pos_IO_1_PIN + 1, pos_IO_2_PIN).toInt();
  io_pin[io_number] = command.substring(pos_IO_2_PIN + 1, pos_IO_3_PIN).toInt();
  String type = command.substring(pos_IO_3_PIN + 1);


  type.trim();
  if (type.equals("INPUT")){
    pinMode(io_pin[io_number], INPUT_PULLUP);
    io_type[io_number] = 1;
  } else if (type == "OUTPUT"){
    pinMode(io_pin[io_number], OUTPUT);
    digitalWrite(io_pin[io_number], HIGH);
    io_type[io_number] = 0;
  } 

  sent_message("IO pin is set");
  sent_message("END");
}


// Functions IO
void IO_digitalWrite(String command){
  int pos_1_IO = command.indexOf('P');
  int pos_2_IO = command.indexOf('S');

  int io_number = command.substring(pos_1_IO + 1, pos_2_IO).toInt();
  int state = command.substring(pos_2_IO + 1).toInt();

  if (state == 1) digitalWrite(io_pin[io_number], LOW);
  else if (state == 0) digitalWrite(io_pin[io_number], HIGH);

  String message = "State " + String(io_pin[io_number]) + " " + String(state);
  
  sent_message(message);
  sent_message("END");
}

#endif 