import psutil
import platform

GB = 1024 ** 3
MB = 1024 ** 2
KB = 1024


def get_info():
    info = dict()
    info['system'] = platform.system()
    info['node'] = platform.node()
    info['platform'] = platform.platform()
    return info


def get_disk_info():
    info = dict()
    m = psutil.disk_partitions()
    for i, item in enumerate(m):
        disk = dict()
        try:
            aux = psutil.disk_usage(m[i][0])
        except FileNotFoundError:
            continue
        disk["partition"] = m[i][0]
        disk["total"] = aux[0] / GB
        disk["used"] = aux[1] / GB
        disk["free"] = aux[2] / GB
        disk["usage"] = aux[3]
        info[i] = disk
    return info


def get_virtual_memory_info():
    info = dict()
    m = psutil.virtual_memory()
    info["total"] = m[0] / GB
    info["used"] = m[3] / GB
    info["free"] = m[4] / GB
    info["usage"] = m[2]
    return info


def get_pid_info(p):
    info = dict()
    try:
        info["name"] = p.name()
    except psutil.AccessDenied:
        return 0
    try:
        info["username"] = p.username()
    except psutil.AccessDenied:
        return 0
    info["pid"] = p.pid
    info["cpu_usage"] = p.cpu_percent()
    info["memory_usage"] = p.memory_percent()
    info["threads"] = p.num_threads()
    return info


def get_process_info():
    p = dict()
    i = 0
    for process in psutil.process_iter():
        pid = get_pid_info(process)
        if pid == 0:
            continue
        p[i] = pid
        i += 1
    return p