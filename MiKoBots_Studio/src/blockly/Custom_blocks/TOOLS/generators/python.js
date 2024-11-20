
python.pythonGenerator.forBlock['set_tool'] = function(block, generator) {
    const text_tool_name = block.getFieldValue('Tool_name');
  
    // TODO: Assemble python into the code variable.
    const code = `tool.SetTool("${text_tool_name}")\n`;
    // TODO: Change Order.NONE to the correct operator precedence strength
    return code;
}

python.pythonGenerator.forBlock['tool_move_to'] = function(block, generator) {
  // TODO: change Order.ATOMIC to the correct operator precedence strength
  const number_pos = block.getFieldValue('pos');

  // TODO: Assemble python into the code variable.
  const code = `tool.MoveTo(${number_pos})\n`;
  return code;
}

python.pythonGenerator.forBlock['tool_state'] = function(block, generator) {
  // TODO: change Order.ATOMIC to the correct operator precedence strength
  const dropdown_state = block.getFieldValue('state');

  // TODO: Assemble python into the code variable.
  const code = `tool.State("${dropdown_state}")\n`;
  return code;
}

