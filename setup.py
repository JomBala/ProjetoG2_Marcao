import cx_Freeze
import sys
import aifc  

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="recursos/assets/icone.ico",
        target_name="PaperRun.exe"
    )
]

cx_Freeze.setup(
    name="Paper Run: Konan Edition",
    version="1.0",
    options={
        "build_exe": {
            "packages": ["pygame", "tkinter", "pyttsx3", "speech_recognition"],
            "includes": ["aifc"],
            "include_files": [("recursos", "recursos"), "log.dat"]
        }
    },
    executables=executaveis
)
