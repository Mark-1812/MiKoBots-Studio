// block MoveJ
python.pythonGenerator.forBlock['MoveJ_6'] = function(block, generator) 
{
  const number_x = block.getFieldValue('X');
  const number_y = block.getFieldValue('Y');
  const number_z = block.getFieldValue('Z');
  const number_yaw = block.getFieldValue('yaw');
  const number_pitch = block.getFieldValue('pitch');
  const number_roll = block.getFieldValue('roll');
  const number_v = block.getFieldValue('v');
  const number_a = block.getFieldValue('a');

  const code = `robot.MoveJ([${number_x}, ${number_y}, ${number_z}, ${number_yaw}, ${number_pitch}, ${number_roll}], ${number_v}, ${number_a})\n`;
  return code;
}

// block MoveL
python.pythonGenerator.forBlock['MoveL_6'] = function(block, generator) 
{
  const number_x = block.getFieldValue('X');
  const number_y = block.getFieldValue('Y');
  const number_z = block.getFieldValue('Z');
  const number_yaw = block.getFieldValue('yaw');
  const number_pitch = block.getFieldValue('pitch');
  const number_roll = block.getFieldValue('roll');
  const number_v = block.getFieldValue('v');
  const number_a = block.getFieldValue('a');

  const code = `robot.MoveL([${number_x}, ${number_y}, ${number_z}, ${number_yaw}, ${number_pitch}, ${number_roll}], ${number_v}, ${number_a})\n`;
  return code;
}

// block OffsetJ
python.pythonGenerator.forBlock['OffsetJ_6'] = function(block, generator) 
{
  const number_x = block.getFieldValue('X');
  const number_y = block.getFieldValue('Y');
  const number_z = block.getFieldValue('Z');
  const number_yaw = block.getFieldValue('yaw');
  const number_pitch = block.getFieldValue('pitch');
  const number_roll = block.getFieldValue('roll');
  const number_v = block.getFieldValue('v');
  const number_a = block.getFieldValue('a');

  const code = `robot.OffsetJ([${number_x}, ${number_y}, ${number_z}, ${number_yaw}, ${number_pitch}, ${number_roll}], ${number_v}, ${number_a})\n`;
  return code;
}

// OffsetL
python.pythonGenerator.forBlock['OffsetL_6'] = function(block, generator) 
{
  const number_x = block.getFieldValue('X');
  const number_y = block.getFieldValue('Y');
  const number_z = block.getFieldValue('Z');
  const number_yaw = block.getFieldValue('yaw');
  const number_pitch = block.getFieldValue('pitch');
  const number_roll = block.getFieldValue('roll');
  const number_v = block.getFieldValue('v');
  const number_a = block.getFieldValue('a');

  const code = `robot.OffsetL([${number_x}, ${number_y}, ${number_z}, ${number_yaw}, ${number_pitch}, ${number_roll}], ${number_v}, ${number_a})\n`;
  return code;
}