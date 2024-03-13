import os
import sys
from LotteryData import LotteryData
from log import Log


class ReadFile:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])))
        self.log = Log()
        self.file_name = "Lottery"

    # 從txt讀檔轉成list
    def read_txt_file(self):
        list_lottery_data = []
        txt_path = os.path.join(self.path, self.file_name + '.txt')

        try:
            if os.path.exists(txt_path):
                with open(txt_path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        data = line.strip().split(':')
                        list_lottery_data.append(
                            {"Issue": data[0], "LotteryDate": data[1], "Numbers": data[2]})
        except Exception as ex:
            Log().write_log("read_txt_file 錯誤:"+str(ex))

        return list_lottery_data
