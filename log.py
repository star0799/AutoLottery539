import os
import datetime
import sys


class Log:
    def write_log(self, message):
        log_directory = os.path.join(os.path.abspath(
            os.path.dirname(sys.argv[0])), "pylog")
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        log_file_path = os.path.join(
            log_directory, datetime.datetime.now().strftime("%Y%m%d") + ".txt")
        with open(log_file_path, "a") as log_file:
            log_file.write(
                f"{datetime.datetime.now().strftime('%H:%M:%S')}   {message}\n")
