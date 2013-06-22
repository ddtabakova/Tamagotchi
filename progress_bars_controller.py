from progress_bar import ProgressBar


class ProgressBarController:

    def __init__(self, attr):
        for key, value in attr.items():
            self.__dict__[key] = value
