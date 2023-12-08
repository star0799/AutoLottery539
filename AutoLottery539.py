import os
import shutil
import zipfile
import requests
import winreg
from log import Log
import sys
from ReadFile import ReadFile
from SeleniumChrome import SeleniumChrome


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
    url_to_path_location = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{
        '.'.join(version.split('.')[:3])}"
    response = requests.get(url_to_path_location)
    if not response.ok:
        Log().write_log(f"Unable to get version path from website: {
            response.status_code}")
        raise requests.exceptions.RequestException(
            f"Unable to get version path from website: {response.status_code}")

    return f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{response.text}/win64/chromedriver-win64.zip"


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


if __name__ == "__main__":
    update_chrome_driver()
    SeleniumChrome().load_data()
