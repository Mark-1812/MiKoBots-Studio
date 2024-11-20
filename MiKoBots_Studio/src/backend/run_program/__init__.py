from backend.run_program.run_program import RunProgram

run_program = RunProgram()

###########################
#   RunProgram
###########################

def run_script(sim):
    run_program.RunScript(sim)
    
def stop_script():
    run_program.StopScript()

def check_program_run():
    if run_program.program_running:
        return True
    else:
        return False

def run_blockly_code(code):
    run_program.RunBlocklyCode(code)
    
def run_single_line(code):
    run_program.RunSingleLine(code)
