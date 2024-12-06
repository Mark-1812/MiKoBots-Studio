
// block digital write
python.pythonGenerator.forBlock['io_digital_write'] = function(block, generator) 
{
  const value_pin_number = generator.valueToCode(block, 'pin_number', python.Order.ATOMIC);
  const dropdown_state = block.getFieldValue('state');

  const code = `IO.digitalWrite(${value_pin_number}, "${dropdown_state}")\n`;
  return code;
}

// block digital read
python.pythonGenerator.forBlock['io_digital_read'] = function(block, generator) 
{
  const value_name = generator.valueToCode(block, 'NAME', python.Order.ATOMIC);

  const code = `IO.digitalRead(${value_name})\n`;
  return [code, python.Order.NONE];
}

// block io pin
python.pythonGenerator.forBlock['io_pin'] = function(block, generator) 
{
  const number_pin_number = block.getFieldValue('pin_number');
  const text_name_io = block.getFieldValue('name_io');

  const code = `${number_pin_number}\n`;
  return [number_pin_number, python.Order.NONE];
}

// block set io pin
python.pythonGenerator.forBlock['set_io_pin'] = function(block, generator) 
{
  const io_number = generator.valueToCode(block, 'NAME', python.Order.ATOMIC);
  const dropdown_io_type = block.getFieldValue('io_type');

  const code = `IO.SetIO(${io_number}, "${dropdown_io_type}")\n`;
  return code;
}