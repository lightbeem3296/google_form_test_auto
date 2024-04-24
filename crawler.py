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

API_ID = 20992264
API_HASH = "8506019a33a5f425e40fd9d119c511a8"
TELEGRAM_APP = Client("my_account", API_ID, API_HASH)


CUR_DIR = str(Path(__file__).parent.absolute())
TEMP_DIR = os.path.join(CUR_DIR, "temp")
CHROME: Chrome


@TELEGRAM_APP.on_message(filters.text)
async def hello(client, message):
    if message.chat.title == "ALDOMİLYAR VIP":
        if "forms.gle" in message.text:
            urls = re.findall(r"(https?://\S+)", message.text)
            print(message.text, urls)

            for url in urls:
                if not "forms.gle" in url:
                    continue

                submit_google_form_test(
                    url=url,
                    shuffle_name=message.from_user.username,
                    telegram_name=message.from_user.username,
                )
        else:
            log_err(f"{message.from_user.username}: {message.text}")


def init_chrome() -> Chrome:
    log_inf("open chrome browser")
    chrome = Chrome(user_data_dir=os.path.join(TEMP_DIR, "profile"))
    chrome.start()

    # login google account
    chrome.goto(
        url2go="https://accounts.google.com/",
        wait_timeout=300,
        wait_elem_selector="h1.XY0ASe",
    )

    return chrome


def submit_google_form_test(url: str, shuffle_name: str, telegram_name: str):
    try:
        # go to google form test url and wait until title "Google Form Test" is selecable
        log_inf("open google form test url")
        CHROME.goto(url2go=url, wait_elem_selector="div.F9yp7e.ikZYwf.LgNcQe")

        # click check box
        if CHROME.run_script("document.querySelector('#i5').getAttribute('aria-checked')") == "false":
            CHROME.click(selector="label.docssharedWizToggleLabeledContainer.OLkl6c")

        # input shuffle name
        b64_shuffle_name = base64.b64encode(shuffle_name.encode()).decode()
        CHROME.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[0].value=atob('{b64_shuffle_name}')")
        CHROME.run_script("document.querySelectorAll('div.ndJi5d.snByac')[0].innerText=''")

        # input telegram name
        b64_telegram_name = base64.b64encode(telegram_name.encode()).decode()
        CHROME.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[1].value=atob('{b64_telegram_name}')")
        CHROME.run_script("document.querySelectorAll('div.ndJi5d.snByac')[1].innerText=''")

        # input captcha
        math_eq = CHROME.run_script(
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

            b64_captcha = base64.b64encode(eq_res.encode()).decode()
            CHROME.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[2].value=atob('{b64_captcha}')")
            CHROME.run_script("document.querySelectorAll('div.ndJi5d.snByac')[2].innerText=''")

        time.sleep(0.5)
        # click submit button
        CHROME.run_script("document.querySelectorAll('span.NPEfkd.RveJvd.snByac')[0].click()")
    except:
        traceback.print_exc()


def work():
    global CHROME
    try:
        # open chrome browser
        CHROME = init_chrome()

        TELEGRAM_APP.run()

        CHROME.quit()
    except:
        traceback.print_exc()


def main():
    work()


def test():
    global CHROME
    CHROME = init_chrome()
    submit_google_form_test(
        url="https://forms.gle/4NccFM5EcL12mdnM7",
        shuffle_name="ekudahl",
        telegram_name="ekudahl",
    )
    input("Press ENTER to close browser.")
    CHROME.quit()


if __name__ == "__main__":
    main()
    # test()

    input("Press ENTER to exit.")
