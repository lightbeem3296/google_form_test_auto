import base64
import os
import re
import time
import traceback
from pathlib import Path

from pyrogram import filters
from pyrogram.client import Client

from libchrome import Chrome
from liblogger import log_err, log_inf

ACCOUNT_LIST = {
    "alpha0@gmail.com": {
        "name": "alpha0",
    },
    "alpha1@gmail.com": {
        "name": "alpha1",
    },
    "alpha2@gmail.com": {
        "name": "alpha2",
    },
}

API_ID = 20992264
API_HASH = "8506019a33a5f425e40fd9d119c511a8"
TELEGRAM_APP = Client("my_account", API_ID, API_HASH)


CUR_DIR = str(Path(__file__).parent.absolute())
TEMP_DIR = os.path.join(CUR_DIR, "temp")
CHROME_LIST = {}


@TELEGRAM_APP.on_message(filters.text)
async def hello(client, message):
    if message.chat.title == "ALDOMİLYAR VIP":
        if "forms.gle" in message.text:
            urls = re.findall(r"(https?://\S+)", message.text)
            print(message.text, urls)

            for url in urls:
                if not "forms.gle" in url:
                    continue
                submit_all(url=url)
        else:
            log_err(f"{message.from_user.username}: {message.text}")


def init_chrome(profile_name: str) -> Chrome:
    log_inf("open chrome browser")
    chrome = Chrome(user_data_dir=os.path.join(TEMP_DIR, f"profile_{profile_name}"))
    chrome.start()

    # login google account
    chrome.goto(
        url2go="https://accounts.google.com/",
        wait_timeout=300,
        wait_elem_selector="h1.XY0ASe",
    )

    return chrome


def submit_all(url: str):
    for key in CHROME_LIST:
        submit_google_form_test(
            chrome=CHROME_LIST[key],
            url=url,
            shuffle_name=ACCOUNT_LIST[key]["name"],
            telegram_name=ACCOUNT_LIST[key]["name"],
        )


def submit_google_form_test(chrome: Chrome, url: str, shuffle_name: str, telegram_name: str):
    try:
        # go to google form test url and wait until title "Google Form Test" is selecable
        log_inf("open google form test url")
        chrome.goto(url2go=url, wait_elem_selector="div.F9yp7e.ikZYwf.LgNcQe")

        # click check box
        if chrome.run_script("document.querySelector('#i5').getAttribute('aria-checked')") == "false":
            chrome.click(selector="label.docssharedWizToggleLabeledContainer.OLkl6c")

        # input shuffle name
        b64_shuffle_name = base64.b64encode(shuffle_name.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[0].value=atob('{b64_shuffle_name}')")
        chrome.run_script("document.querySelectorAll('div.ndJi5d.snByac')[0].innerText=''")

        # input telegram name
        b64_telegram_name = base64.b64encode(telegram_name.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[1].value=atob('{b64_telegram_name}')")
        chrome.run_script("document.querySelectorAll('div.ndJi5d.snByac')[1].innerText=''")

        # input captcha
        math_eq = chrome.run_script(
            """
elems = document.querySelectorAll('span.M7eMe');
elem = elems[elems.length - 1];
elem.innerText"""
        )
        if math_eq != None:
            log_inf(f"equation: {math_eq}")
            math_eq = math_eq.replace("x", "*")

            eq_res = str(eval(math_eq))
            log_inf(f"result: {eq_res}")

            b64_eq_res = base64.b64encode(eq_res.encode()).decode()
            chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[2].value=atob('{b64_eq_res}')")
            chrome.run_script("document.querySelectorAll('div.ndJi5d.snByac')[2].innerText=''")

        time.sleep(0.5)
        # click submit button
        chrome.run_script("document.querySelectorAll('span.NPEfkd.RveJvd.snByac')[0].click()")
    except:
        traceback.print_exc()


def work():
    global CHROME_LIST
    try:
        # open chrome browsers
        for key in ACCOUNT_LIST:
            chrome = init_chrome(key)
            CHROME_LIST[key] = chrome

        TELEGRAM_APP.run()

        # close chrome browsers
        for key in CHROME_LIST:
            CHROME_LIST[key].quit()
    except:
        traceback.print_exc()


def main():
    work()


def test():
    # open chrome browsers
    for key in ACCOUNT_LIST:
        chrome = init_chrome(key)
        CHROME_LIST[key] = chrome

    submit_all(url="https://forms.gle/4NccFM5EcL12mdnM7")
    submit_all(url="https://forms.gle/4NccFM5EcL12mdnM7")

    input("Press ENTER to close browser.")

    # close chrome browsers
    for key in CHROME_LIST:
        CHROME_LIST[key].quit()


if __name__ == "__main__":
    main()
    # test()

    input("Press ENTER to exit.")
