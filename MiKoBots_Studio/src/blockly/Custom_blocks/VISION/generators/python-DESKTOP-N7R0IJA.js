
python.pythonGenerator.forBlock['vision_find_objects'] = function(block, generator) {
    const dropdown_name = block.getFieldValue('NAME');
  
    // TODO: Assemble python into the code variable.
    const code = `vision.find_object("${dropdown_name}")\n`;
    // TODO: Change Order.NONE to the correct operator precedence strength
    return [code, python.Order.NONE];
}

python.pythonGenerator.forBlock['vision_move_to'] = function(block, generator) {
  // TODO: change Order.ATOMIC to the correct operator precedence strength
  const value_object_list = generator.valueToCode(block, 'Object_list', python.Order.ATOMIC);

  // TODO: Assemble python into the code variable.
  const code = `vision.find_object(${value_object_list})\n`;
  return code;
}