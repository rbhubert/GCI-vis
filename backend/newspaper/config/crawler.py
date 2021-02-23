import psutil
from selenium.webdriver import FirefoxOptions

MACOS_ = "geckodriver_macos"
WINDOWS_ = "geckodriver_windows.exe"
LINUX_ = "geckodriver_linux.exe"
GECKODRIVER_PATH_BASE = "./geckodriver/"
GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + WINDOWS_

# Identification of the SO to select and use the appropiate geckodriver to scrap the newspapers.
if psutil.MACOS:
    GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + MACOS_
elif psutil.LINUX:
    GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + LINUX_

firefox_options = FirefoxOptions()
firefox_options.add_argument('--headless')
