import platform

if __name__ == '__main__':
    current_platform = platform.system()
    if current_platform == 'Windows':

        import subprocess
        import tkinter as tk
        from tkinter import filedialog
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
        root = tk.Tk()
        root.withdraw()
        file_path = tk.filedialog.askopenfilename()
        if len(file_path) == 0:
            exit(0)
        str_hashcode = subprocess.getoutput('certutil -hashfile {} sha256'.format(file_path)).split('\n')
        hashcode = str_hashcode[1]
        print(hashcode)
    else:
        print('Only available in Windows')
