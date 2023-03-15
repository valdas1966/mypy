from f_logging.c_log_writter import LogWritter
from f_utils import u_file


folder_read = 'c:\\log_archive'
folder_write = 'c:\\log_write'
folder_read = 'd:\\temp\\logwritter'
folder_write = 'd:\\temp\\logwritter\\1'
threshold = 4


def run() -> None:
    filepaths = u_file.filepaths(path_dir=folder_read, extensions='log')
    writter = LogWritter(folder=folder_write, threshold=threshold)
    for i, filepath in enumerate(filepaths):
        with open(filepath) as file:
            print(f'[{i}] {filepath} [{len(file.readlines())}]')
        with open(filepath) as file:
            for line in file:
                writter.write(line=line)
    writter.close()


run()
