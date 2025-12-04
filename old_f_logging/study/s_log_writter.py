from old_f_logging.c_log_writter import LogWritter


folder = 'd:\\temp\\logwritter'
logw = LogWritter(folder=folder, threshold=2)
for i in range(10):
    logw.write(line=str(i))
logw.close()
