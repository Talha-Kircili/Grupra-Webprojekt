from multiprocessing import cpu_count


pythonpath = 'Grundlagenpraktikum'
bind = '127.0.0.1:8000'
workers = cpu_count() * 2 + 1
timeout = 90
loglevel = 'error'
errorlog = 'error.log'
daemon = True
