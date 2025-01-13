from tessfiles.telefiles import main_bot


class MainProcess:
    @staticmethod
    def __process1__():
        main_bot.DoBotInterface().main_process()


if __name__ == '__main__':
    MainProcess.__process1__()
