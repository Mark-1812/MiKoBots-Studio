Blockly.defineBlocksWithJsonArray([
  // block find board tic tac toe
  {
    "type": "ttt_find_board",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Find board %1 %2 %3",
    "args0": [
      {
        "type": "input_dummy",
        "name": "NAME"
      },
      {
        "type": "field_dropdown",
        "name": "color",
        "options": [
          [
            "RED",
            "RED"
          ], 
          [
            "BLUE",
            "BLUE"
          ],
          [
            "GREEN",
            "GREEN"
          ]
        ]
      },
      {
        "type": "input_dummy",
        "name": "color"
      }
    ],
    "output": null,
    "colour": 180,
    "inputsInline": true
  },

  // block find human move
  {
    "type": "ttt_find_human_move",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Find human move %1 color %2 %3",
    "args0": [
      {
        "type": "input_dummy",
        "name": "NAME"
      },
      {
        "type": "field_dropdown",
        "name": "NAME",
        "options": [
          [
            "RED",
            "RED"
          ],
          [
            "GREEN",
            "GREEN"
          ],
          [
            "BLUE",
            "BLUE"
          ]
        ]
      },
      {
        "type": "input_dummy",
        "name": "color"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 180,
    "inputsInline": true
  },

  // block generate move ai
  {
    "type": "ttt_generate_move_ai",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Generate move ai %1 board %2",
    "args0": [
      {
        "type": "input_dummy",
        "name": "NAME"
      },
      {
        "type": "input_value",
        "name": "board",
        "check": "Array"
      }
    ],
    "output": null,
    "colour": 180,
    "inputsInline": true
  },

  // block check winning move
  {
    "type": "ttt_check_winning_move",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Check winning move %1",
    "args0": [
      {
        "type": "input_dummy",
        "name": "NAME"
      }
    ],
    "output": null,
    "colour": 180
  }                                                     
]);

