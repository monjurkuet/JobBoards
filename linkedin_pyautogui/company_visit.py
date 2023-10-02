import webbrowser
import pyautogui
import time
import subprocess
import os
import signal

# Specify the path to your Chrome application
firefox_path = '/usr/bin/firefox'  # Update this path

# The URL you want to navigate to
url = 'http://linkedin.com/'


webbrowser.get(firefox_path).open(url)

subprocess.run(['wmctrl','-xa','firefox'])

pyautogui.hotkey('alt', 'd')

time.sleep(1)

pyautogui.hotkey('ctrl', 'l')

pyautogui.press('backspace') 

def enter_navbar_text(textvalue):
    subprocess.run(['wmctrl','-xa','brave-browser'])
    time.sleep(.5)
    pyautogui.hotkey('alt', 'd')
    time.sleep(.5)
    pyautogui.press('backspace') 
    time.sleep(.5)
    pyautogui.write(textvalue, interval=0.05)
    time.sleep(.5)
    pyautogui.press('backspace') 
    time.sleep(.5)
    pyautogui.press('enter')


mitmprocess_command = f"mitmdump -s mitmSave.py --mode upstream:http://{PROXY}:3199 -p 2191"

mitmprocess = subprocess.Popen(mitmprocess_command, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid, stderr=subprocess.PIPE)

browserprocess_command = f"brave-browser --proxy-server=127.0.0.1:2191 --user-data-dir={PROFILE_DIRECTORY}/{PROXY} &>/dev/null &"

browserprocess = subprocess.Popen(browserprocess_command, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid, stderr=subprocess.PIPE)

os.killpg(os.getpgid(mitmprocess.pid), signal.SIGTERM)  

os.killpg(os.getpgid(browserprocess.pid), signal.SIGTERM) 