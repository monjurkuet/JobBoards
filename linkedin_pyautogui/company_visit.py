import webbrowser
import pyautogui
import time
from win32 import win32api
from pywinauto import Application
# Specify the path to your Chrome application
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s &'  # Update this path

# The URL you want to navigate to
url = 'http://linkedin.com/'

# Open the URL in a new Chrome window
app = Application().connect(path='C:/Program Files/Google/Chrome/Application/chrome.exe')
webbrowser.get(chrome_path).open(url)

pyautogui.hotkey('ctrl', 'l')
time.sleep(1)