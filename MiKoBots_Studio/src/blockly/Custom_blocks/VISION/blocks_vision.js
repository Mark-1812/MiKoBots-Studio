// File: custom_blocks/my_custom_blocks.js

Blockly.defineBlocksWithJsonArray([
  {
    "type": "vision_find_objects",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Find objects %1 color %2 %3",
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
            "red",
            "RED"
          ],
          [
            "green",
            "GREEN"
          ],
          [
            "blue",
            "BLUE"
          ],
          [
            "yellow",
            "YELLOW"
          ],
          [
            "orange",
            "ORANGE"
          ],
          [
            "purple",
            "PURPLE"
          ],
          [
            "white",
            "WHITE"
          ],
          [
            "black",
            "BLACK"
          ]
        ]
      },
      {
        "type": "input_dummy",
        "name": "color"
      }
    ],
    "output": null,
    "colour": 225,
    "inputsInline": true
  },
  {
    "type": "vision_move_to",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Move to object %1 Object list %2",
    "args0": [
      {
        "type": "input_dummy",
        "name": "NAME"
      },
      {
        "type": "input_value",
        "name": "Object_list",
        "check": "Array"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 225,
    "inputsInline": true
  }        
]);
