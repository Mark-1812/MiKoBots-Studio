// File: custom_blocks/my_custom_blocks.js

Blockly.defineBlocksWithJsonArray([
  {
    "type": "io_pin",
    "tooltip": "",
    "helpUrl": "",
    "message0": "pin number %1 io name %2 %3",
    "args0": [
      {
        "type": "field_number",
        "name": "pin_number",
        "value": 0
      },
      {
        "type": "field_input",
        "name": "name_io",
        "text": "name"
      },
      {
        "type": "input_dummy",
        "name": "NAME"
      }
    ],
    "output": null,
    "colour": 225
  },

  {
    "type": "set_io_pin",
    "tooltip": "",
    "helpUrl": "",
    "message0": "Set IO %1 %2 %3",
    "args0": [
      {
        "type": "input_value",
        "name": "NAME",
        "check": "Number"
      },
      {
        "type": "field_dropdown",
        "name": "io_type",
        "options": [
          [
            "INPUT",
            "INPUT"
          ],
          [
            "OUTPUT",
            "OUTPUT"
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
  },
                      
                      
  {
    "type": "io_digital_write",
    "tooltip": "",
    "helpUrl": "",
    "message0": "DigitalWrite %1 state %2 %3",
    "args0": [
      {
        "type": "input_value",
        "name": "pin_number",
        "check": "Number"
      },
      {
        "type": "field_dropdown",
        "name": "state",
        "options": [
          [
            "High",
            "HIGH"
          ],
          [
            "Low",
            "LOW"
          ]
        ]
      },
      {
        "type": "input_dummy",
        "name": "state"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "colour": 225,
    "inputsInline": true
  },
  {
    "type": "io_digital_read",
    "tooltip": "",
    "helpUrl": "",
    "message0": "IO digitalRead %1",
    "args0": [
      {
        "type": "input_value",
        "name": "NAME",
        "check": "Number"
      }
    ],
    "output": null,
    "colour": 225
  }
                      
]);
