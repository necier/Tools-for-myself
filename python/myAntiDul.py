import multiprocessing
import subprocess
import sys


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
    # print(hashcode)
    return [file_path, hashcode]


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # Module multiprocessing is organized differently in Python 3.4+
    try:
        # Python 3.4+
        if sys.platform.startswith('win'):
            import multiprocessing.popen_spawn_win32 as forking
        else:
            import multiprocessing.popen_fork as forking
    except ImportError:
        import multiprocessing.forking as forking
    if sys.platform.startswith('win'):
        class _Popen(forking.Popen):
            def __init__(self, *args, **kw):
                if hasattr(sys, 'frozen'):
                    # We have to set original _MEIPASS2 value from sys._MEIPASS
                    # to get --onefile mode working.
                    os.putenv('_MEIPASS2', sys._MEIPASS)
                try:
                    super(_Popen, self).__init__(*args, **kw)
                finally:
                    if hasattr(sys, 'frozen'):
                        if hasattr(os, 'unsetenv'):
                            os.unsetenv('_MEIPASS2')
                        else:
                            os.putenv('_MEIPASS2', '')
        forking.Popen = _Popen

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
        print('该文件夹内共有 {} 个文件'.format(num_files))
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
        dul_exists = False
        for key in sorted_file:
            if len(sorted_file[key]) < 2:
                continue
            else:
                dul_exists = True
                print('以下文件是完全相同的：')
                for x in sorted_file[key]:
                    print('\t{}'.format(x), end='\n')
        pool.terminate()
        if not dul_exists:
            print('此文件夹中没有完全相同的文件')
        os.system('pause')
    else:
        print('Only available in Windows:(')
