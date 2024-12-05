
/**
 * A dictionary of the block definitions provided by this module.
 */
Blockly.defineBlocksWithJsonArray([
    // Block for repeat n times (external number).
    {
        'type': 'controls_repeat_ext1',
        'message0': '%{BKY_CONTROLS_REPEAT_TITLE}',
        'args0': [
            {
                'type': 'input_value',
                'name': 'TIMES',
                'check': 'Number',
            },
        ],
        'message1': '%{BKY_CONTROLS_REPEAT_INPUT_DO} %1',
        'args1': [
            {
                'type': 'input_statement',
                'name': 'DO',
            },
        ],
        'previousStatement': null,
        'nextStatement': null,
        'style': 'loop_blocks',
        'tooltip': '%{BKY_CONTROLS_REPEAT_TOOLTIP}',
        'helpUrl': '%{BKY_CONTROLS_REPEAT_HELPURL}',
    },
    // Block for repeat n times (internal number).
    // The 'controls_repeat_ext' block is preferred as it is more flexible.
    {
        'type': 'controls_repeat1',
        'message0': '%{BKY_CONTROLS_REPEAT_TITLE}',
        'args0': [
            {
                'type': 'field_number',
                'name': 'TIMES',
                'value': 10,
                'min': 0,
                'precision': 1,
            },
        ],
        'message1': '%{BKY_CONTROLS_REPEAT_INPUT_DO} %1',
        'args1': [
            {
                'type': 'input_statement',
                'name': 'DO',
            },
        ],
        'previousStatement': null,
        'nextStatement': null,
        'style': 'loop_blocks',
        'tooltip': '%{BKY_CONTROLS_REPEAT_TOOLTIP}',
        'helpUrl': '%{BKY_CONTROLS_REPEAT_HELPURL}',
    },
    // Block for 'do while/until' loop.
    {
        'type': 'controls_whileUntil1',
        'message0': '%1 %2',
        'args0': [
            {
                'type': 'field_dropdown',
                'name': 'MODE',
                'options': [
                    ['%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}', 'WHILE'],
                    ['%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_UNTIL}', 'UNTIL'],
                ],
            },
            {
                'type': 'input_value',
                'name': 'BOOL',
                'check': 'Boolean',
            },
        ],
        'message1': '%{BKY_CONTROLS_REPEAT_INPUT_DO} %1',
        'args1': [
            {
                'type': 'input_statement',
                'name': 'DO',
            },
        ],
        'previousStatement': null,
        'nextStatement': null,
        'style': 'loop_blocks',
        'helpUrl': '%{BKY_CONTROLS_WHILEUNTIL_HELPURL}',
        'extensions': [],
    },
    // Block for 'for' loop.
    {
        'type': 'controls_for1',
        'message0': '%{BKY_CONTROLS_FOR_TITLE}',
        'args0': [
            {
                'type': 'field_variable',
                'name': 'VAR',
                'variable': null,
            },
            {
                'type': 'input_value',
                'name': 'FROM',
                'check': 'Number',
                'align': 'RIGHT',
            },
            {
                'type': 'input_value',
                'name': 'TO',
                'check': 'Number',
                'align': 'RIGHT',
            },
            {
                'type': 'input_value',
                'name': 'BY',
                'check': 'Number',
                'align': 'RIGHT',
            },
        ],
        'message1': '%{BKY_CONTROLS_REPEAT_INPUT_DO} %1',
        'args1': [
            {
                'type': 'input_statement',
                'name': 'DO',
            },
        ],
        'inputsInline': true,
        'previousStatement': null,
        'nextStatement': null,
        'style': 'loop_blocks',
        'helpUrl': '%{BKY_CONTROLS_FOR_HELPURL}',
        'extensions': ['contextMenu_newGetVariableBlock', 'controls_for_tooltip'],
    },
    // Block for 'for each' loop.
    {
        'type': 'controls_forEach1',
        'message0': '%{BKY_CONTROLS_FOREACH_TITLE}',
        'args0': [
            {
                'type': 'field_variable',
                'name': 'VAR',
                'variable': null,
            },
            {
                'type': 'input_value',
                'name': 'LIST',
                'check': 'Array',
            },
        ],
        'message1': '%{BKY_CONTROLS_REPEAT_INPUT_DO} %1',
        'args1': [
            {
                'type': 'input_statement',
                'name': 'DO',
            },
        ],
        'previousStatement': null,
        'nextStatement': null,
        'style': 'loop_blocks',
        'helpUrl': '%{BKY_CONTROLS_FOREACH_HELPURL}',
        'extensions': [
            'contextMenu_newGetVariableBlock',
            'controls_forEach_tooltip',
        ],
    },
    // Block for flow statements: continue, break.
    {
        'type': 'controls_flow_statements1',
        'message0': '%1',
        'args0': [
            {
                'type': 'field_dropdown',
                'name': 'FLOW',
                'options': [
                    ['%{BKY_CONTROLS_FLOW_STATEMENTS_OPERATOR_BREAK}', 'BREAK'],
                    ['%{BKY_CONTROLS_FLOW_STATEMENTS_OPERATOR_CONTINUE}', 'CONTINUE'],
                ],
            },
        ],
        'previousStatement': null,
        'style': 'loop_blocks',
        'helpUrl': '%{BKY_CONTROLS_FLOW_STATEMENTS_HELPURL}',
        'suppressPrefixSuffix': true,
        'extensions': ['controls_flow_in_loop_check1'],
    },
]);


Blockly.Extensions.register('controls_flow_in_loop_check1', function() {
    this.setOnChange(function(changeEvent) {
      if (!this.isInFlyout) {
        let legal = false;
        let block = this.getParent();

        const loopBlockTypes = ['controls_repeat_ext1', 'controls_repeat1', 'controls_forEach1', 'controls_whileUntil1', 'controls_for1'];

        while (block) {
            if (loopBlockTypes.includes(block.type)) {
                legal = true;
                break;
            }
            block = block.getParent();
        }

        if (!legal) {

            this.setWarningText(`This block must be used within a loop.`);
        } else {
            this.setWarningText(null);
        }
      }
    });
  });
  