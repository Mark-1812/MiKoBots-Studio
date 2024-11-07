// File: custom_blocks/my_custom_blocks.js

Blockly.defineBlocksWithJsonArray([
  {
    "type": "set_tool",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Set tool %1 %2",
    "args0": [
      {
        "type": "field_input",
        "name": "Tool_name",
        "text": "default"
      },
      {
        "type": "input_dummy",
        "name": "NAME"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 225
  },
  {
    "type": "tool_move_to",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Tool MoveTo %1 %2",
    "args0": [
      {
        "type": "field_number",
        "name": "pos",
        "value": 0,
        "min": 0,
        "max": 100
      },
      {
        "type": "input_dummy",
        "name": "NAME"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 225
  },
  {
    "type": "tool_state",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Tool state %1 %2",
    "args0": [
      {
        "type": "field_dropdown",
        "name": "state",
        "options": [
          [
            "HIGH",
            "HIGH"
          ],
          [
            "LOW",
            "LOW"
          ]
        ]
      },
      {
        "type": "input_dummy",
        "name": "NAME"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 225,
    "inputsInline": true
  }
                      
]);
