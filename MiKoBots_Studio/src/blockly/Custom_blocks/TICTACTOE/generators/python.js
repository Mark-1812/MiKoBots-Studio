// block find board tic tac toe
python.pythonGenerator.forBlock['ttt_find_board'] = function(block, generator) 
{
  const dropdown_color = block.getFieldValue('color');

  const code = `tictactoe.DetectBoard("${dropdown_color}")\n`;
  return [code, python.Order.NONE];
}


// block find human move
python.pythonGenerator.forBlock['ttt_find_human_move'] = function(block, generator) 
{
  const dropdown_name = block.getFieldValue('NAME');
  const value_board = generator.valueToCode(block, 'board', python.Order.ATOMIC);

  const code = `tictactoe.FindHumanMove("${dropdown_name}", ${value_board})\n`;
  return code;
}

// block generate move ai
python.pythonGenerator.forBlock['ttt_generate_move_ai'] = function(block, generator) 
{
  const value_board = generator.valueToCode(block, 'board', python.Order.ATOMIC);

  const code = `tictactoe.GenerateMoveAi(${value_board})\n`;
  return [code, python.Order.NONE];
}

// block check winning move
python.pythonGenerator.forBlock['ttt_check_winning_move'] = function(block, generator) 
{
  const code = 'tictactoe.CheckWinningMove()';
  return [code, python.Order.NONE];
}