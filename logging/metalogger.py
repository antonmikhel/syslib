import os
import time
import datetime

from sysdefines.meta import Singleton


class MetaLogger:
    __metaclass__ = Singleton

    def __init__(self, log_dir="", app_name="Logger", start_time = time.time(), max_log_size_mb=5):
        self.__log_dir = log_dir if log_dir else os.devnull
        self.__app_name = app_name
        self.__start_time = start_time
        self.__max_log_size = max_log_size_mb
        self.__logfile = None
        self.__create_log()

    def __create_log(self):
        log_path = os.path.join(self.__log_dir, self.__app_name + "_log_1.log")
        if os.path.exists(log_path):
            if (os.path.getsize(log_path) / 1024 / 1024) > self.__max_log_size:
                # Always remove older log
                os.unlink(log_path)
            self.__logfile = open(os.path.join(log_path, "a"))

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self):
        if self.__logfile:
            self.__logfile.close()

    @staticmethod
    def current_date():
        return str(datetime.datetime.now().date().isoformat())

    @staticmethod
    def current_time():
        return str(datetime.datetime.now().time().isoformat())

    def __msg_format(self, msg, verb):
        msg_time = time.time()
        return "|{0}>>{1}|{2:.2f}s|{3:s}>>>{4:s}".format(self.current_date(), self.current_time(),
                                                         msg_time - self.__start_time, verb, msg)

    def __write_to_disk(self, msg):
        if self.__logfile:
            self.__logfile.write(msg + "\n")

    def __print_msg(self, msg, verb):
        print self.__msg_format(msg, verb)

    def __handle_msg(self, msg, verb):
        self.__print_msg(msg, verb)
        self.__write_to_disk(self.__msg_format(msg + "\n", verb))

    def info(self, msg, verb="INFO"):
        self.__handle_msg(msg, verb)

    def warn(self, msg, verb="WARN"):
        self.__handle_msg(msg, verb)

    def err(self, msg, verb="ERROR"):
        self.__handle_msg(msg, verb)
