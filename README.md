


MiKoBots 0_1/
|
|- MiKoBots_studio.py
|
|- backend/
|	|
|	|- calculations/
|   |   |- calculations_vision.py
|	|	|- kinematics_6_axis.py
|	|	
|	|- core/
|	|	|- api.py
|	|	|- event_manager.py
|	|	|- run_program.py
|	|	|- variables.py
|	|
|	|- file_management/
|	|	|- get_users_path.py
|	|	|- save_open.py
|	|
|	|- g_code/
|	|	|- functions.py
|	|
|	|- xbox/
|	|	|- xbox.py
|	|	
|	|- robot_management/
|	|	|- robot_3d_model.py
|	|	|- robot_commands.py
|	|	|- robot_communication.py
|	|	|- robot_loader.py
|	|	|- tool_management.py
|	|
|	|- simulation/
|	|	|- __init__.py
|	|	|- simulation_management.py
|	|	|- simulation_object_window.py
|	|	|- simulation_origin_window.py
|	|
|	|- vision/
|	|	|- connect4/
|	|	|	|- __init__.py
|	|	|	|- functions.py
|	|	|	|- solve_connect4.py
|	|	|
|	|	|- tic_tac_toe/
|	|	|	|- __init__.py
|	|	|	|- functions.py
|	|	|	|- solve_tic_tac_toe.py
|	|	|
|	|	|- __init__.py
|	|	|- vision_functions.py
|	|	|- vision_management.py
|	|	|- vision_var.py
|	
|- gui/
|	|- main_window.py
|	|
|	|- fields/
|	|	|- field_control.py
|	|	|- field_log.py
|	|	|- field_menu.py
|	|	|- field_program.py
|	|	|- field_settings.py
|	|
|	|- tabs_field/
|	|	|- show_hide_tab.py
|	|	|
|	|	|- gcode/
|	|	|	|- gcode_frame.py
|	|	|	|- gcode_info.py
|	|	|	|- gcode_program_field.py
|	|	|
|	|	|- robot_tab/
|	|	|	|- robot_3d_model.py
|	|	|	|- robot_frame.py
|	|	|	|- robot_info.py
|	|	|	|- robot_overview.py
|	|	|	|- robot_settings.py
|	|	|	|- robot_tools.py
|	|	|
|	|	|- simulation/
|	|	|	|- simulation_frame.py
|	|	|
|	|	|- vision/
|	|	|	|- vision_connect4.py
|	|	|	|- vision_frame.py
|	|	|	|- vision_info.py
|	|	|	|- vision_setup.py
|	|	|	|- vision_tictactoe.py