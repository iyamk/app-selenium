import sys, time, io, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium_stealth import stealth
import threading
import PySimpleGUI as sg

thread = None
event_selenium = None

def runner():
    global event_selenium
    op = webdriver.ChromeOptions()
    op.add_argument('start-maximized')
    op.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(
        service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=op
    )
    stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True,
    )

    driver.get('https://example.com')

    while True:
        time.sleep(1)
        if event_selenium == 'STOP':
            break
        event_selenium = None

    driver.quit()

if __name__ == '__main__':
    window = sg.Window('App', [
        [
            sg.Button('Start', key='start'),
            sg.Button('Stop', key='stop', disabled=True)
        ]
    ])
    while True:
        event, values = window.read()
        if event == 'start':
            window['start'].update(disabled=True)
            window['stop'].update(disabled=False)
            thread = threading.Thread(target=runner)
            thread.start()
        elif event == 'stop':
            window['start'].update(disabled=False)
            window['stop'].update(disabled=True)
            event_selenium = 'STOP'
        elif event == sg.WIN_CLOSED:
            break
    window.close()