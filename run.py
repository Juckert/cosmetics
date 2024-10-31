from DoWorkInterface import DoWork
import os

get_time = lambda f: os.stat(f).st_ctime

fn = 'file.name'
prev_time = get_time(fn)


main_method = DoWork('1.jpg') # 1 jpg --- current container


if __name__ == '__main__':
    while True:
        t = get_time(fn)
        if t != prev_time:
            main_method.its()
            prev_time = t