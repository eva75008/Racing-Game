import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

def main():
    python_exe = sys.executable
    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(initialdir=sys.path[0], title="Select a Pyxel resource file", filetypes=[("Pyxel Resource Files", "*.pyxres")])
        if not file_path:
            print("No .pyxres file selected.")
            sys.exit(1)

        subprocess.run([python_exe, "-m", "pyxel", "edit", file_path], check=True)

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
