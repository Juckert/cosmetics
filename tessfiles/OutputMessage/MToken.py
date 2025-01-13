import os
__NAME__ = os.path.dirname(os.path.abspath(__file__)) + '/output_bad_ingredients.txt'


class FileChecker:
    @staticmethod
    def get_time():
        return os.stat(__NAME__).st_ctime

    @staticmethod
    def get_short_path():
        return 'OutputMessage/output_bad_ingredients.txt'

    @staticmethod
    def get_path():
        return os.path.abspath(__NAME__)


if __name__ == '__main__':
    print('It is not a lib!')