from TessProcess import DoWorkInterface
from images import IToken


fc = IToken.FileChecker
prev_time = fc.get_time()

if __name__ == '__main__':
    while True:
        if fc.get_time() != prev_time:
            DoWorkInterface('../OutputMessage/output_composition.txt', path=fc.get_path()).main_process()
            prev_time = fc.get_time()