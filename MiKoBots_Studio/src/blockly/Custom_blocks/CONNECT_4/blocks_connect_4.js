Blockly.defineBlocksWithJsonArray([
  // block connect4 find board
  {
    "type": "connect4_find_board",
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
    "colour": 330,
    "inputsInline": true
  },

  // block connect4 find human move
  {
    "type": "connect4_find_human_move",
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
    "colour": 330,
    "inputsInline": true
  },

  // block connect4 generate move ai
  {
    "type": "connect4_generate_move_ai",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Genetate move ai %1 board %2",
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
    "colour": 330,
    "inputsInline": true
  },

  // block connect4 check winning move
  {
    "type": "connect4_check_winning_move",
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
    "colour": 330
  }
                                                               
]);

