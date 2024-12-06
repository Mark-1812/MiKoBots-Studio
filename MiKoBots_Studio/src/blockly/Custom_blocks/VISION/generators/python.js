// block vision find object
python.pythonGenerator.forBlock['vision_find_objects'] = function(block, generator) 
{
    const dropdown_name = block.getFieldValue('NAME');
  
    const code = `vision.FindObject("${dropdown_name}")\n`;
    return [code, python.Order.NONE];
}

// block vision move to 
python.pythonGenerator.forBlock['vision_move_to'] = function(block, generator) 
{
  const value_objectlist = generator.valueToCode(block, 'ObjectList', python.Order.ATOMIC);
  const number_posz = block.getFieldValue('PosZ');
  const number_vel = block.getFieldValue('vel');
  const number_accel = block.getFieldValue('accel');

  // Change TRUE or FALSE to True or False
  const checkbox_check = block.getFieldValue('check') === "TRUE" ? "True" : "False";

  const code = `vision.MoveToObject(${value_objectlist}, ${number_posz}, ${number_vel}, ${number_accel}, ${checkbox_check})\n`;
  return code;
}

