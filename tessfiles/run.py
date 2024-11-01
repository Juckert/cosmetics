from DoWorkInterface import DoWork
import os

get_time = lambda f: os.stat(f).st_ctime

fn = '1.jpg'
dir = 'pic/'
prev_time = get_time(dir + fn)


main_method = DoWork(fn) # 1 jpg --- current container


if __name__ == '__main__':
    while True:
        t = get_time(dir + fn)
        if t != prev_time:
            print(main_method.its())
            prev_time = t