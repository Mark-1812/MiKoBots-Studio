void SetupEsp32(){

  BLEDevice::init("Robot_MiKoBots");  // Custom BLE name here

  // Create BLE server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  if (pServer == NULL) {
    Serial.println("Failed to create BLE server");
    while (1); // Halt the program
  }

  // Create a BLE service
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_WRITE |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );
  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();

  mutex = xSemaphoreCreateMutex();
  if (mutex == NULL) {
    // Mutex creation failed, handle the error
    Serial.println("Mutex creation failed!");
    while (1); // Halts the program
  }

  stopSemaphore = xSemaphoreCreateBinary();
  if (stopSemaphore == NULL) {
    // Semaphore creation failed, handle the error
    Serial.println("Semaphore creation failed!");
    while (1); // Halts the program
  }

  

  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("BLE Device is Ready to Pair");

  Serial.print("Free heap: ");
  Serial.println(ESP.getFreeHeap());

  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
                    Task1code,   /* Task function. */
                    "Task1",     /* name of task. */
                    8192,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task1,      /* Task handle to keep track of created task */
                    0);          /* pin task to core 0 */                  
  delay(300); 

  //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  xTaskCreatePinnedToCore(
                    Task2code,   /* Task function. */
                    "Task2",     /* name of task. */
                    15000,       /* Stack size of task */
                    NULL,        /* parameter of the task */
                    1,           /* priority of the task */
                    &Task2,      /* Task handle to keep track of created task */
                    1);          /* pin task to core 1 */
  delay(300);

}


void Task1code(void * pvParameters) {
  while (true) {
    // Process Serial Input
    while (Serial.available() > 0) {
      deviceDisconnected = false;
        char c = Serial.read();
        if (c == '\n') {
            String str(buffer);
            processCommand(str);  // Process command in a separate function
            memset(buffer, 0, sizeof(buffer));  // Clear buffer
        } else {
            if (strlen(buffer) < (sizeof(buffer) - 1)) {
                strncat(buffer, &c, 1);
            }
        }
    }

    // Process Bluetooth Input
    if (deviceConnected && pCharacteristic->getValue() != "") {
        String recievedData = pCharacteristic->getValue().c_str();
        pCharacteristic->setValue("");  // Clear after reading
        processCommand(recievedData);  // Process command in a separate function
        recievedData = "";
    }


    checkInputs();  // Separate function for input checks
    vTaskDelay(100 / portTICK_PERIOD_MS);  // Use vTaskDelay instead of delay
  }
}


void storeInBuffer(const String& data) {
  if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE) {
    if (lineIndex < BUFFER_SIZE) {
      lines[lineIndex] = data;
      lineIndex++;
    } else {
      sent_message_task("Error: Buffer overflow");
    }
    if (lineIndex > BUFFER_SIZE - 2) {
      sent_message_task("wait");
    }
    xSemaphoreGive(mutex);
  }
}


String coordinates;
void Task2code(void * pvParameters) {
  String command;
  while (true) {
    while (stop == false){
      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE){
        if (lines[0] == ""){
          xSemaphoreGive(mutex);
          break;
        }
        command = lines[0];
        xSemaphoreGive(mutex);
      }

      int spaceIndex = command.indexOf(' ');
      String typeOfCommand = command.substring(0, spaceIndex);
      coordinates = command.substring(spaceIndex + 1);

      typeOfCommand.trim();

      // Commands
      if (type_device  == "ROBOT" and typeOfCommand.equals("MoveL")) MoveL(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("MoveJ")) MoveJ(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("MoveJoint")) MoveJoint(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("jogL")) jogL(command);
      else if (type_device  == "ROBOT" and typeOfCommand.equals("jogJ")) jogJ(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("OffsetJ")) offsetJ(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("OffsetL")) offsetL(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Home")) home_Joints(command);

      // commands tool
      else if (typeOfCommand.equals("Tool_move_to")) tool_move_to(command);
      else if (typeOfCommand.equals("Tool_state")) tool_state(command);  

      // commands IO
      else if (typeOfCommand.equals("IO_digitalWrite")) IO_digitalWrite(command);

      // Settings robot
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_number_of_joints")) set_number_of_joints(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_motor_pin")) set_motor_pin(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_switch_pin")) set_switch_pin(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_max_pos")) set_max_pos(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_lim_pos")) set_lim_pos(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_step_deg")) set_step_deg(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_dir_joints")) set_direction_joint(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_dh_par")) set_dh_par(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_speed")) set_speed(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_home_settings")) set_homing(command);
      else if (type_device == "ROBOT" and typeOfCommand.equals("Set_extra_joint")) set_extra_joint(command);
      

      // Settings Tool
      else if (typeOfCommand.equals("Set_tools")) set_TOOL(command);
      else if (typeOfCommand.equals("Set_tool_frame")) set_tool_frame(command);

      // Settings IO
      else if (typeOfCommand.equals("Set_io_pin")) set_IO_pin(command);

      //If the command does not match send END
      // else{
      //   String message = "Error: do not regonize this command: " + typeOfCommand;
      //   sent_message(message);
      //   sent_message("END");
      // }
    

      if ((xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE) and (command != "")){
        for (int i = 0; i < BUFFER_SIZE - 1; i++) {
          lines[i] = lines[i+1];
        }      

        lines[BUFFER_SIZE - 1] = ""; // Clear the last line'
        lineIndex--;

        if(lineIndex < BUFFER_SIZE - 1){
          sent_message("go");
        } 
        xSemaphoreGive(mutex);
      }

    }
    if (stop){

      if (xSemaphoreTake(mutex, portMAX_DELAY) == pdTRUE){
        for (int i = 0; i < BUFFER_SIZE; i++) {
          lines[i] = "";
        } 

        lineIndex = 0; // Wrap around if the buffer is full
        xSemaphoreGive(mutex);
      }
    }
    vTaskDelay(5 / portTICK_PERIOD_MS);  
  }
  vTaskDelay(10 / portTICK_PERIOD_MS);
}