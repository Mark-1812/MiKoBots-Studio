Blockly.defineBlocksWithJsonArray([
  // block vision find object
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
    "colour": 0,
    "inputsInline": true
  },

  // block vision move to 
  {
    "type": "vision_move_to",
    "tooltip": "",
    "helpUrl": "https://mikobots.com/mikobots-studio/help/program-field/functions-vision/",
    "message0": "Object List %1 Position Z %2 %3 v %4 %5 a %6 %7 Extra check %8 %9",
    "args0": [
      {
        "type": "input_value",
        "name": "ObjectList",
        "check": "Array"
      },
      {
        "type": "field_number",
        "name": "PosZ",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "ZPos"
      },
      {
        "type": "field_number",
        "name": "vel",
        "value": 50
      },
      {
        "type": "input_dummy",
        "name": "vel"
      },
      {
        "type": "field_number",
        "name": "accel",
        "value": 50
      },
      {
        "type": "input_dummy",
        "name": "accel"
      },
      {
        "type": "field_checkbox",
        "name": "check",
        "checked": "FALSE"
      },
      {
        "type": "input_dummy",
        "name": "Check"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 0,
    "inputsInline": true
  }
                      
]);

