import os, stat, time

def chmod_x(path):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

def calc_time(cluster):
    start_time = cluster['start_time'] / 1000
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(start_time))
