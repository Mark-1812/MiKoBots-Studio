// File: custom_blocks/my_custom_blocks.js

Blockly.defineBlocksWithJsonArray([
    {
        "type": "MoveJ_6",
        "tooltip": "",
        "helpUrl": "",
        "message0": "MoveJ %1 X %2 %3 Y %4 %5 Z %6 %7 y %8 %9 p %10 %11 r %12 %13 v %14 %15 a %16 %17",
        "args0": [
          {
            "type": "input_dummy",
            "name": "name"
          },
          {
            "type": "field_number",
            "name": "X",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "X"
          },
          {
            "type": "field_number",
            "name": "Y",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "Y"
          },
          {
            "type": "field_number",
            "name": "Z",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "Z"
          },
          {
            "type": "field_number",
            "name": "yaw",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "yaw"
          },
          {
            "type": "field_number",
            "name": "pitch",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "pitch"
          },
          {
            "type": "field_number",
            "name": "roll",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "roll"
          },
          {
            "type": "field_number",
            "name": "v",
            "value": 50,
            "min": 1,
            "max": 100
          },
          {
            "type": "input_dummy",
            "name": "v"
          },
          {
            "type": "field_number",
            "name": "a",
            "value": 50,
            "min": 1,
            "max": 100
          },
          {
            "type": "input_dummy",
            "name": "a"
          }
        ],
        "previousStatement": "Number",
        "nextStatement": null,
        "colour": 0,
        "inputsInline": true
      },
      {
        "type": "MoveL_6",
        "tooltip": "",
        "helpUrl": "",
        "message0": "MoveL %1 X %2 %3 Y %4 %5 Z %6 %7 y %8 %9 p %10 %11 r %12 %13 v %14 %15 a %16 %17",
        "args0": [
          {
            "type": "input_dummy",
            "name": "name"
          },
          {
            "type": "field_number",
            "name": "X",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "X"
          },
          {
            "type": "field_number",
            "name": "Y",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "Y"
          },
          {
            "type": "field_number",
            "name": "Z",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "Z"
          },
          {
            "type": "field_number",
            "name": "yaw",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "yaw"
          },
          {
            "type": "field_number",
            "name": "pitch",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "pitch"
          },
          {
            "type": "field_number",
            "name": "roll",
            "value": 0
          },
          {
            "type": "input_dummy",
            "name": "roll"
          },
          {
            "type": "field_number",
            "name": "v",
            "value": 50,
            "min": 1,
            "max": 100
          },
          {
            "type": "input_dummy",
            "name": "v"
          },
          {
            "type": "field_number",
            "name": "a",
            "value": 50,
            "min": 1,
            "max": 100
          },
          {
            "type": "input_dummy",
            "name": "a"
          }
        ],
        "previousStatement": "Number",
        "nextStatement": null,
        "colour": 0,
        "inputsInline": true
      },
      {
        "type": "robot_init",
        "message0": "create robot %1",
        "args0": [
            {
                "type": "field_input",
                "name": "ROBOT_NAME",
                "text": "robot"
            }
        ],
        "nextStatement": null,
        "colour": 210,
        "tooltip": "Creates a new robot instance.",
        "helpUrl": ""
    },
    {
      "type": "OffsetJ_6",
      "tooltip": "",
      "helpUrl": "",
      "message0": "OffsetJ %1 X %2 %3 Y %4 %5 Z %6 %7 y %8 %9 p %10 %11 r %12 %13 v %14 %15 a %16 %17",
      "args0": [
        {
          "type": "input_dummy",
          "name": "name"
        },
        {
          "type": "field_number",
          "name": "X",
          "value": 0
        },
        {
          "type": "input_dummy",
          "name": "X"
        },
        {
          "type": "field_number",
          "name": "Y",
          "value": 0
        },
        {
          "type": "input_dummy",
          "name": "Y"
        },
        {
          "type": "field_number",
          "name": "Z",
          "value": 0
        },
        {
          "type": "input_dummy",
          "name": "Z"
        },
        {
          "type": "field_number",
          "name": "yaw",
          "value": 0
        },
        {
          "type": "input_dummy",
          "name": "yaw"
        },
        {
          "type": "field_number",
          "name": "pitch",
          "value": 0
        },
        {
          "type": "input_dummy",
          "name": "pitch"
        },
        {
          "type": "field_number",
          "name": "roll",
          "value": 0
        },
        {
          "type": "input_dummy",
          "name": "roll"
        },
        {
          "type": "field_number",
          "name": "v",
          "value": 50,
          "min": 1,
          "max": 100
        },
        {
          "type": "input_dummy",
          "name": "v"
        },
        {
          "type": "field_number",
          "name": "a",
          "value": 50,
          "min": 1,
          "max": 100
        },
        {
          "type": "input_dummy",
          "name": "a"
        }
      ],
      "previousStatement": "Number",
      "nextStatement": null,
      "colour": 0,
      "inputsInline": true
    },
    {
      "type": "robot_init",
      "message0": "create robot %1",
      "args0": [
          {
              "type": "field_input",
              "name": "ROBOT_NAME",
              "text": "robot"
          }
      ],
      "nextStatement": null,
      "colour": 210,
      "tooltip": "Creates a new robot instance.",
      "helpUrl": ""
  },
  {
    "type": "OffsetL_6",
    "tooltip": "",
    "helpUrl": "",
    "message0": "OffsetL %1 X %2 %3 Y %4 %5 Z %6 %7 y %8 %9 p %10 %11 r %12 %13 v %14 %15 a %16 %17",
    "args0": [
      {
        "type": "input_dummy",
        "name": "name"
      },
      {
        "type": "field_number",
        "name": "X",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "X"
      },
      {
        "type": "field_number",
        "name": "Y",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "Y"
      },
      {
        "type": "field_number",
        "name": "Z",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "Z"
      },
      {
        "type": "field_number",
        "name": "yaw",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "yaw"
      },
      {
        "type": "field_number",
        "name": "pitch",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "pitch"
      },
      {
        "type": "field_number",
        "name": "roll",
        "value": 0
      },
      {
        "type": "input_dummy",
        "name": "roll"
      },
      {
        "type": "field_number",
        "name": "v",
        "value": 50,
        "min": 1,
        "max": 100
      },
      {
        "type": "input_dummy",
        "name": "v"
      },
      {
        "type": "field_number",
        "name": "a",
        "value": 50,
        "min": 1,
        "max": 100
      },
      {
        "type": "input_dummy",
        "name": "a"
      }
    ],
    "previousStatement": "Number",
    "nextStatement": null,
    "colour": 0,
    "inputsInline": true
  }                       
    
]);