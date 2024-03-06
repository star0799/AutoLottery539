import os
import shutil
import zipfile
import requests
import winreg
from log import Log
import sys
from ReadFile import ReadFile
from SeleniumChrome import SeleniumChrome
from UpdateAutoLottery539 import UpdateAutoLottery539
import configparser
import tempfile
import subprocess


def update_chrome_driver():
    print("更新ChromeDriver開始")
    Log().write_log("更新ChromeDriver開始")
    chrome_driver_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    chromedriver_version = get_chrome_driver_version(chrome_driver_path)
    chrome_web_version = get_web_chrome_version()

    if chromedriver_version != chrome_web_version:
        try:
            url_to_download = get_url_to_download(chrome_web_version)
            kill_all_chromedriver_processes()
            download_new_version_of_chrome(url_to_download, chrome_driver_path)
            extract_zip(chrome_driver_path)
            move_chrome_driver(chrome_driver_path)
            Log().write_log("下載新版本Url:"+url_to_download+"完成")
        except Exception as ex:
            Log().write_log("更新ChromeDriver失敗，原因:"+str(ex))
    else:
        Log().write_log("無須更新")
    print("更新ChromeDriver結束")
    Log().write_log("更新ChromeDriver結束")


def get_chrome_driver_version(chrome_driver_path):
    chromedriver_path = os.path.join(chrome_driver_path, "chromedriver.exe")
    outstd2 = os.popen(f'"{chromedriver_path}" --version').read()
    if outstd2:
        version_tokens = outstd2.split(' ')
        if len(version_tokens) > 1:
            return version_tokens[1].split('.')[0]
    return outstd2


def get_web_chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Google\Chrome\BLBeacon')
    version_str, types = winreg.QueryValueEx(key, 'version')
    if version_str:
        version = version_str.split('.')[0]
        return version
    return ""


def get_url_to_download(version):
    if not version:
        raise ValueError("Unable to get url because version is empty")
    url_to_path_location = config['Github']['ChromeLatestReleaseUrl']+f"{
        '.'.join(version.split('.')[:3])}"
    response = requests.get(url_to_path_location)
    if not response.ok:
        Log().write_log(f"Unable to get version path from website: {
            response.status_code}")
        raise requests.exceptions.RequestException(
            f"Unable to get version path from website: {response.status_code}")

    config = configparser.ConfigParser()
    config.read('config.ini')
    downloadUrl = config['Settings']['ChromeDownloadUrl']
    downloadFile = config['Settings']['ChromeDownloadFile']
    return downloadUrl+response.text+downloadFile


def kill_all_chromedriver_processes():
    try:
        os.system("taskkill /f /im chromedriver.exe")
    except Exception as ex:
        Log().write_log(str(ex))


def download_new_version_of_chrome(url_to_download, chrome_driver_path):
    if not url_to_download:
        raise ValueError("Unable to get url because url_to_download is empty")

    zip_file_path = os.path.join(chrome_driver_path, "chromedriver.zip")
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)

    with requests.get(url_to_download, stream=True) as response:
        with open(zip_file_path, 'wb') as zip_file:
            shutil.copyfileobj(response.raw, zip_file)

    if os.path.exists(zip_file_path) and os.path.exists(os.path.join(chrome_driver_path, "chromedriver.exe")):
        os.remove(os.path.join(chrome_driver_path, "chromedriver.exe"))


def extract_zip(chrome_driver_path):
    zip_file_name = ""
    # 取得當前執行檔的絕對路徑
    current_file_path = os.path.abspath(sys.argv[0])
    # 使用 os.path.dirname 獲取目錄部分
    directory_path = os.path.dirname(current_file_path)
    # 組合路徑
    zip_file_name = os.path.join(directory_path, "chromedriver.zip")
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(chrome_driver_path)
    os.remove(zip_file_name)


def move_chrome_driver(chrome_driver_path):
    chromedriver_exe_path = os.path.join(
        chrome_driver_path, "chromedriver-win64", "chromedriver.exe")
    shutil.move(chromedriver_exe_path, os.path.join(
        chrome_driver_path, "chromedriver.exe"))
    shutil.rmtree(os.path.join(chrome_driver_path,
                               "chromedriver-win64"), ignore_errors=True)


def schedule_commands(temp_file_path, file_path):
    # 在延迟后执行命令
    subprocess.Popen(
        ["cmd.exe", "/C", "choice /C Y /N /D Y /T 1 & Del", temp_file_path])

    # 启动新版本程序
    subprocess.Popen(["cmd.exe", "/C", "choice /C Y /N /D Y /T 1 &",
                     os.path.join(file_path, "Lottery539.exe")])


if __name__ == "__main__":
    try:
        Log().write_log("更新應用程式")
        filePath = os.getcwd()
        # 要異動的檔案列表
        moveFiles = ["AutoLottery539_version.txt",
                     "AutoLottery539.exe", "config.ini"]
        updater = UpdateAutoLottery539()
        update_available, download_url = updater.is_update()
        if update_available:
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()

            # 将原始目录中的指定檔案移动到临时目录
            for file_to_move in moveFiles:
                if os.path.isfile(file_to_move):
                    temp_file_path = os.path.join(temp_dir, file_to_move)
                    shutil.move(file_to_move, temp_file_path)

            # 下载并更新文件
            updater.download_file(download_url, '.')

            # 移动并替换文件
            updater.move_and_replace_files()

            # 在一段延迟后执行命令
            temp_exe_path = os.path.join(temp_dir, 'AutoLottery539_temp.exe')
            schedule_commands(temp_exe_path, filePath)
            Log().write_log("更新成功")

    except Exception as ex:
        Log().write_log("更新應用程式失敗")
        Log().write_log(str(ex))

    update_chrome_driver()
    SeleniumChrome().load_data()
