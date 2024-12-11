from TessProcess import DoWorkInterface
from images import IToken


im = IToken.FileChecker
prev_time = im.get_time()

if __name__ == '__main__':
    while True:
        if im.get_time() != prev_time:
            DoWorkInterface('../OutputMessage/output_composition.txt', path=fc.get_path()).main_process()
            prev_time = im.get_time()