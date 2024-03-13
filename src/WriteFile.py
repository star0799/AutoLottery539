import os
from datetime import datetime
from typing import List
from LotteryData import LotteryData
import sys


class WriteFile:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])))
        self.file_name = "Lottery"

    def write_data(self, data: List[LotteryData]):
        file_path = os.path.join(self.path, f"{self.file_name}.txt")

        existing_lines = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_lines = file.readlines()

        new_data_lines = self.format_data_file(data)
        existing_lines = new_data_lines + existing_lines

        with open(file_path, 'w') as file:
            file.writelines(existing_lines)

    def format_data_file(self, data: List[LotteryData]) -> List[str]:
        result = []
        for d in data:
            result.append(f"{d.Issue}:{d.LotteryDate}:{
                          self.split_empty(d.Numbers)}\n")
        return result

    def split_empty(self, numbers: str) -> str:
        split_list = [s.strip() for s in numbers.split(',')]
        result = ",".join(split_list)
        return result

    def insert_lottery(self, data: LotteryData):
        file_path = os.path.join(self.path, f"{self.file_name}.txt")

        existing_lines = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_lines = file.readlines()

        new_data_lines = self.format_data_file([data])

        # 解析新數據的日期
        new_date = datetime.strptime(data.LotteryDate, "%Y-%m-%d")

        # 查找要插入的位置
        insert_index = 0
        for i in range(len(existing_lines)):
            # 解析現有行的日期
            existing_date = datetime.strptime(
                existing_lines[i].split(':')[1], "%Y-%m-%d")

            # 如果新數據日期早於或等於現有行的日期，則找到插入位置
            if new_date > existing_date:
                insert_index = i
                break
            if insert_index == 0 and i == len(existing_lines) - 1:
                insert_index = len(existing_lines)

        # 插入新數據
        existing_lines.insert(insert_index, new_data_lines[0])

        # 保存按日期排序的數據
        with open(file_path, 'w') as file:
            file.writelines(existing_lines)
