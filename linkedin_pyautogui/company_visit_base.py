import webbrowser
import pyautogui
import time
import subprocess
import os
import signal
import re

# Specify the path to your Chrome application
chrome_path = '/usr/bin/chromium-browser %s &'  # Update this path

# The URL you want to navigate to
url = 'http://linkedin.com/'


webbrowser.get(chrome_path).open(url)


subprocess.run(['wmctrl','-xa','chromium-browser'])

pyautogui.hotkey('alt', 'd')

time.sleep(1)

pyautogui.hotkey('ctrl', 'l')

pyautogui.press('backspace') 

def enter_navbar_text(textvalue):
    subprocess.run(['wmctrl','-xa','chromium-browser'])
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


mitmprocess_command = f"mitmdump -s mitmSave.py -p 2191"

mitmprocess = subprocess.Popen(mitmprocess_command, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid, stderr=subprocess.PIPE)

browserprocess_command = f"chromium-browser --proxy-server=127.0.0.1:2191 &>/dev/null &"

browserprocess = subprocess.Popen(browserprocess_command, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid, stderr=subprocess.PIPE)

os.killpg(os.getpgid(mitmprocess.pid), signal.SIGTERM)  

os.killpg(os.getpgid(browserprocess.pid), signal.SIGTERM) 

with open('companyhtmldata.html','r') as f:
    htmldata=f.read()

os.remove('companyhtmldata.html')

# Define the regular expression pattern
pattern_website = r'websiteUrl&quot;:&quot;(http://.*?)&quot;'

# Search for the pattern in the input string
match = re.search(pattern_website, htmldata)
# Check if a match is found
if match:
    # Extract the URL from the match
    url = match.group(1)
    print(url)
else:
    url=None