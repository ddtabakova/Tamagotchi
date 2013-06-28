class ParallelDate:

    def __init__(self, seconds_representation):
        self.seconds_representation = seconds_representation
        self.__seconds = 0.0
        self.__minutes = 0.0
        self.__hours = 0.0
        self.__days = 0.0

    def update_date(self, seconds):
        self.__seconds = seconds*self.seconds_representation
        self.__minutes, self.__seconds = divmod(self.__seconds, 60)
        self.__hours, self.__minutes = divmod(self.__minutes, 60)
        self.__days, self.__hours = divmod(self.__hours, 24)

    def get_seconds(self):
        return str(int(self.__seconds))

    def get_minutes(self):
        return str(int(self.__minutes))

    def get_hours(self):
        return str(int(self.__hours))

    def get_days(self):
        return str(int(self.__days))
