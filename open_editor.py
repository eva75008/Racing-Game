from tkinter.filedialog import askopenfilename
from subprocess import run
from sys import path

# Open a file dialog to select a .pyxres file
file_path = askopenfilename(
    initialdir=path[0],
    title="Select a Pyxel Resource File",
    filetypes=[("Pyxel Resource Files", "*.pyxres")],
)

# If a file was selected, open it in the Pyxel Editor
if file_path:
    run(["python", "-m", "pyxel", "edit", file_path], check=True)
else:
    exit("No .pyxres file selected.")