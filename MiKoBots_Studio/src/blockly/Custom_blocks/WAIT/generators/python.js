// Block wait 
python.pythonGenerator.forBlock['wait'] = function(block, generator) {
  const number_name = block.getFieldValue('time');

  const code = `time.sleep(${number_name})\n`;
  return code;
}