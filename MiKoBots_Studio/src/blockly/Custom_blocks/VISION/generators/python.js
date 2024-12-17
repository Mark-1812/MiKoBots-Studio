// block vision find object
python.pythonGenerator.forBlock['vision_find_objects'] = function(block, generator) 
{
    const dropdown_name = block.getFieldValue('NAME');
  
    const code = `vision.FindObject("${dropdown_name}")\n`;
    return [code, python.Order.NONE];
}

python.pythonGenerator.forBlock['vision_find_objects_area'] = function(block, generator) 
{
  const dropdown_name = block.getFieldValue('NAME');

  const number_area_x = block.getFieldValue('area_x');
  const number_area_y = block.getFieldValue('area_y');
  const number_area_w = block.getFieldValue('area_w');
  const number_area_h = block.getFieldValue('area_h');

  // TODO: Assemble python into the code variable.
  const code = `vision.FindObject("${dropdown_name}", [${number_area_x},${number_area_y},${number_area_w},${number_area_h}])\n`;
  // TODO: Change Order.NONE to the correct operator precedence strength
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

