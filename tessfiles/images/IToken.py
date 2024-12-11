import os
__NAME__ = os.path.dirname(os.path.abspath(__file__)) + '/input.jpg'


class FileChecker:
    @staticmethod
    def get_time():
        return os.stat(__NAME__).st_ctime

    @staticmethod
    def get_path():
        return os.path.abspath(__NAME__)
