from backend.run_program.run_program import RunProgram

run_program = RunProgram()

###########################
#   RunProgram
###########################

def run_script(sim):
    run_program.RunScript(sim)
    
def stop_script():
    run_program.StopScript()



def run_blockly_code(code):
    run_program.RunBlocklyCode(code)
    
def run_single_line(code):
    run_program.RunSingleLine(code)
