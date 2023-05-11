import platform
import multiprocessing
import subprocess


def findAllFile(base):
    file_paths = []
    for root, ds, fs in os.walk(base):
        for f in fs:
            file_path = os.path.join(root, f).replace('/', '\\')
            file_paths.append(file_path)
    return file_paths


def getHashCode(file_path):
    str_hashcode = subprocess.getoutput('certutil -hashfile "{}" sha256'.format(file_path)).split('\n')
    hashcode = str_hashcode[1]
    return hashcode


def func(file_path, index):
    print('正在扫描第 {} 个文件'.format(index), end='\r')
    hashcode = getHashCode(file_path)
    return [file_path, hashcode]


if __name__ == '__main__':

    current_platform = platform.system()
    if current_platform == 'Windows':

        import tkinter as tk
        from tkinter import filedialog
        from ctypes import windll
        import os

        windll.shcore.SetProcessDpiAwareness(1)
        root = tk.Tk()
        root.withdraw()
        ddir = filedialog.askdirectory()

        core_num = multiprocessing.cpu_count()
        print('检测到该设备有 {} 个CPU核心'.format(core_num))
        pool = multiprocessing.Pool(processes=core_num)

        files_path = findAllFile(ddir)
        num_files = len(files_path)
        file_and_hash_raw = []
        for i in range(num_files):
            file_and_hash_raw.append(pool.apply_async(func=func, args=(files_path[i], i)))
        pool.close()
        pool.join()
        file_and_hash = []
        for x in file_and_hash_raw:
            file_and_hash.append(x.get())

        sorted_file = {}
        for i in range(num_files):
            if file_and_hash[i][1] in sorted_file:
                sorted_file[file_and_hash[i][1]].append(file_and_hash[i][0])

            else:
                sorted_file[file_and_hash[i][1]] = [file_and_hash[i][0], ]
        for key in sorted_file:
            if len(sorted_file[key]) < 2:
                continue
            else:
                print('以下文件是完全相同的：')
                for x in sorted_file[key]:
                    print('\t{}'.format(x), end='\n')

        os.system('pause')


    else:
        print('Only available in Windows terminal:(')
