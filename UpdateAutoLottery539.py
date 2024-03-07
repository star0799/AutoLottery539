import configparser
import os
import requests
import shutil
import zipfile
from log import Log
import sys


class UpdateAutoLottery539:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.path = os.getcwd()

    def is_update(self):
        local_version = self.read_version()

        release = self.get_latest_release()
        Log().write_log("當前版本:"+local_version)
        Log().write_log("新版本:"+release['tag_name'])
        if release is not None and self.is_new_version(release['tag_name'].strip(), local_version.strip()):
            url = release['assets'][0]['browser_download_url']
            print("Current version:", local_version,
                  ", New version:", release['tag_name'])
            Log().write_log("版本更新至:"+release['tag_name'])
            return True, url
        else:
            return False, ''

    def read_version(self):
        file_name = os.path.join(self.path, "AutoLottery539_version.txt")
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return file.read().strip()
        return ""

    def get_latest_release(self):
        owner = self.config.get('Github', 'GithubUser')
        repo = self.config.get('Github', 'GithubRepo')
        api_url = f"https://api.github.com/repos/{
            owner}/{repo}/releases/latest"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def download_file(self, url, file_path):
        file_path = os.path.join(file_path, "Lottery539.zip")
        with requests.get(url, stream=True) as r:
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        extract_path = os.path.dirname(file_path)
        publish_path = os.path.join(extract_path, "publish")
        if os.path.exists(publish_path):
            shutil.rmtree(publish_path)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        os.remove(file_path)

    def move_and_replace_files(self):
        Log().write_log(os.path.dirname(os.path.abspath(sys.argv[0])))
        source_directory = os.path.join(os.path.dirname(__file__), "publish")
        destination_directory = os.path.dirname(__file__)
        Log().write_log("__file__"+__file__)
        Log().write_log(source_directory)
        Log().write_log(destination_directory)
        if os.path.exists(source_directory):
            for file_name in os.listdir(source_directory):
                source_path = os.path.join(source_directory, file_name)
                destination_path = os.path.join(
                    destination_directory, file_name)
                shutil.copyfile(source_path, destination_path)

            shutil.rmtree(source_directory)

    def is_new_version(self, latest_version, current_version):
        return latest_version > current_version
