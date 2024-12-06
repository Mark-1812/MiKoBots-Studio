// block connect4 find board
python.pythonGenerator.forBlock['connect4_find_board'] = function(block, generator) 
{
  const dropdown_color = block.getFieldValue('color');

  const code = `connect4.DetectBoard("${dropdown_color}")\n`;
  return [code, python.Order.NONE];
}

// block connect4 find human move
python.pythonGenerator.forBlock['connect4_find_human_move'] = function(block, generator) 
{
  const dropdown_name = block.getFieldValue('NAME');

  const code = `connect4.FindHumanMove("${dropdown_name}")\n`;
  return code;
}

// block connect4 generate move ai
python.pythonGenerator.forBlock['connect4_generate_move_ai'] = function(block, generator) 
{
  const value_board = generator.valueToCode(block, 'board', python.Order.ATOMIC);

  const code = `connect4.GenerateMoveAi("${value_board}")\n`;
  return [code, python.Order.NONE];
}

// block connect4 check winning move
python.pythonGenerator.forBlock['connect4_check_winning_move'] = function(block, generator) 
{
  const code = 'connect4.CheckWinningMove()';
  return [code, python.Order.NONE];
}