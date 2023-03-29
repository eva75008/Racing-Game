import tkinter.filedialog as fd
import subprocess
import sys

# Open a file dialog to select a .pyxres file
file_path = fd.askopenfilename(
    initialdir=sys.path[0],
    title="Select a Pyxel resource file",
    filetypes=[("Pyxel Resource Files", "*.pyxres")],
)

# If a file was selected, open it in the Pyxel Editor
if file_path:
    subprocess.run(["python", "-m", "pyxel", "edit", file_path], check=True)
else:
    print("No .pyxres file selected.")
    sys.exit(1)