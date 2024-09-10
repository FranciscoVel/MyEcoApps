import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psutil
import zipfile
import shutil
import subprocess

# Crear una instancia de la ventana de Tkinter
win = Tk()
win.geometry("450x200")
string = ""

def display_text():
    global entry
    global string
    string = entry.get()

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def set_license_file(option):
    if option == "1":
        run("[Environment]::SetEnvironmentVariable('SLBSLS_LICENSE_FILE', $env:SLBSLS_LICENSE_FILE + '27000@10.11.45.107;27000@10.11.45.104;27000@10.11.45.93;27000@10.11.45.94;27001@10.11.45.93;27001@10.11.45.94', 'User')")
    elif option == "2":
        run("[Environment]::SetEnvironmentVariable('SLBSLS_LICENSE_FILE', $env:SLBSLS_LICENSE_FILE + '27000@10.11.45.110;27000@10.11.45.104;27000@10.11.45.93;27000@10.11.45.94;27001@10.11.45.93;27001@10.11.45.94', 'User')")
    elif option == "3":
        run("[Environment]::SetEnvironmentVariable('SLBSLS_LICENSE_FILE', $env:SLBSLS_LICENSE_FILE + '27002@10.11.45.108;27000@10.11.45.93;27000@10.11.45.94;27001@10.11.45.93;27001@10.11.45.94', 'User')")
    elif option == "4":
        run("[Environment]::SetEnvironmentVariable('SLBSLS_LICENSE_FILE', $env:SLBSLS_LICENSE_FILE + '27000@10.11.45.104;27000@10.11.45.93;27000@10.11.45.94;27001@10.11.45.93;27001@10.11.45.94', 'User')")
    elif option == "0":
        run("[Environment]::SetEnvironmentVariable('SLBSLS_LICENSE_FILE', $env:SLBSLS_LICENSE_FILE + '27000@10.11.45.104;27000@10.11.45.93;27000@10.11.45.94;27001@10.11.45.93;27001@10.11.45.94', 'User')")
    else:
        return False
    return True

def menu():
    global entry
    global label

    label1 = Label(win,
                   text="Digite el número de su dependencia:\n1 = VDE.\n2 = VEX.\n3 = GNC/VDP.\n4 = ICP.\n0 = Ninguna de las anteriores\n\nOpciones de Licenciamiento:",
                   font=("Arial", 10))
    label1.pack()

    entry = Entry(win, width=40)
    entry.focus_set()
    entry.pack()

    ttk.Button(win, text="Okay", width=20, command=combine_funcs(display_text, win.destroy)).pack(pady=5)

    win.mainloop()

def to_gb(bytes):
    return bytes / 1024**3

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    if completed.returncode != 0:
        print("Error al ejecutar el comando:", completed.stderr)

disk_usage = psutil.disk_usage("C:\\")
total_C_space = to_gb(disk_usage.free)

# Usa rutas con barras inclinadas o barras invertidas escapadas
copy_origin = r"C:/Users/Mjaramillo6/OneDrive - Schlumberger/Proyecto Petrel/OneDrive_2024-07-03.zip"
copy_destination = r"C:/Windows/Temp"
filename = r'C:/Windows/Temp/OneDrive_2024-07-03.zip'
extract_dir = r'C:/Windows/Temp/Petrel20194_64bit'

if total_C_space > 8.0:
    while True:
        menu()
        if set_license_file(string):
            shutil.copy(copy_origin, copy_destination)
            shutil.unpack_archive(filename, extract_dir)
            run("$AESKeyFilePath = 'C:/Users/Mjaramillo6/AES_MJ_key.txt' `n $SecurePwdFilePath = 'C:/Users/Mjaramillo6/credpassword.txt' `n $userUPN = 'dir\\mjaramillo6' `n $AESKey = Get-Content -Path $AESKeyFilePath `n $pwdTxt = Get-Content -Path $SecurePwdFilePath `n $securePass = $pwdTxt | ConvertTo-SecureString -Key $AESKey `n $adminCreds = New-Object System.Management.Automation.PSCredential($userUPN, $securePass) `n Start-Process 'powershell.exe' -Credential $adminCreds -args '& ping 8.8.8.8'")
            messagebox.showinfo("Info", "AOSM SCHLUMBERGER le informa que ha terminado la instalación de PETREL")
        else:
            messagebox.showerror("Error", "Seleccione una opción del menú")
            break
else:
    messagebox.showerror("Error", f"No cuenta con espacio en la unidad C: {total_C_space:.2f} GB.")
