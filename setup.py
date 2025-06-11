# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="feito.py", icon="assets/icone.ico") ]
cx_Freeze.setup(
    name = "Paper Run: Konan Edition",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["assets"]
        }
    }, executables = executaveis
)


