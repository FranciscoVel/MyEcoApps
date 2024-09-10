from cx_Freeze import setup, Executable

# Información sobre tu aplicación
build_exe_options = {
    "packages": ["os", "tkinter", "psutil", "zipfile", "shutil", "subprocess"],
    "excludes": [],
    
}

# Configuración del script
setup(
    name="main",
    version="1.0",
    description="Descripción de mi aplicación",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)],
)
