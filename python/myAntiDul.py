import platform
import sys


def findAllFile(base):
    file_paths = []
    for root, ds, fs in os.walk(base):
        for f in fs:
            file_path = os.path.join(root, f).replace('/', '\\')
            file_paths.append(file_path)
    return file_paths


def mainFunc(file_paths):
    files_num = len(file_paths)
    print('在该文件夹中检测到 {} 个文件\n'.format(files_num))
    hashs = []
    duplicate_files = []
    cnt = 1
    for file_path in file_paths:
        # sys.stdout.write('\r正在扫描第{}个文件 {}'.format(cnt,file_path))
        # sys.stdout.flush()
        # print('\x1B[1A\x1B[K正在扫描第{}个文件 {}'.format(cnt, file_path), end='\r', flush=True)
        print('\r正在扫描第{}个文件'.format(cnt), end='', flush=True)
        hashcode = getHashCode(file_path)
        if hashcode in hashs:
            print('\rDuplicate file detected! {}'.format(file_path), end='\n')
            duplicate_files.append(file_path)
        else:
            hashs.append(hashcode)
        cnt += 1


def getHashCode(file_path):
    # str_hashcode = subprocess.getoutput('certutil -hashfile "{}" sha256'.format(file_path)).split('\n')
    # SHA-256太慢所以换成MD5
    str_hashcode = subprocess.getoutput('certutil -hashfile "{}" md5'.format(file_path)).split('\n')
    hashcode = str_hashcode[1]
    return hashcode


if __name__ == '__main__':

    current_platform = platform.system()
    if current_platform == 'Windows':

        import subprocess
        import tkinter as tk
        from tkinter import filedialog
        from ctypes import windll
        import os

        windll.shcore.SetProcessDpiAwareness(1)
        root = tk.Tk()
        root.withdraw()
        ddir = filedialog.askdirectory()
        mainFunc(findAllFile(ddir))
    else:
        print('Only available in Windows :(')
