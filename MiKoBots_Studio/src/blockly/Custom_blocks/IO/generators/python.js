
python.pythonGenerator.forBlock['io_digital_write'] = function(block, generator) {
    const value_pin_number = generator.valueToCode(block, 'pin_number', python.Order.ATOMIC);

    const dropdown_state = block.getFieldValue('state');
  
    // TODO: Assemble python into the code variable.

    const code = `IO.digitalWrite(${value_pin_number}, "${dropdown_state}")\n`;
    // TODO: Change Order.NONE to the correct operator precedence strength
    return code;
}


python.pythonGenerator.forBlock['io_digital_read'] = function(block, generator) {
    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const value_name = generator.valueToCode(block, 'NAME', python.Order.ATOMIC);
  
    // TODO: Assemble python into the code variable.
    const code = `IO.digitalWrite("${value_name}")\n`;
    // TODO: Change Order.NONE to the correct operator precedence strength
    return [code, python.Order.NONE];
  }


python.pythonGenerator.forBlock['io_pin'] = function(block, generator) {
const number_pin_number = block.getFieldValue('pin_number');
const text_name_io = block.getFieldValue('name_io');

// TODO: Assemble python into the code variable.
const code = `${number_pin_number}\n`;
// TODO: Change Order.NONE to the correct operator precedence strength
return [number_pin_number, python.Order.NONE];
}

python.pythonGenerator.forBlock['set_io_pin'] = function(block, generator) {
    // TODO: change Order.ATOMIC to the correct operator precedence strength
    const io_number = generator.valueToCode(block, 'NAME', python.Order.ATOMIC);
  
    const dropdown_io_type = block.getFieldValue('io_type');
  
    // TODO: Assemble python into the code variable.
    const code = `IO.SetIO(${io_number}, "${dropdown_io_type}")\n`;
    return code;
  }