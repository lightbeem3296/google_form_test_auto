import base64
import os
import traceback
from pathlib import Path

from libchrome import Chrome
from liblogger import log_inf

CUR_DIR = str(Path(__file__).parent.absolute())
PROFILE_DIR = os.path.join(CUR_DIR, "profile")


def submit_google_form_test(chrome: Chrome, url: str, shuffle_name: str, telegram_name: str):
    try:
        # go to google form test url and wait until title "Google Form Test" is selecable
        log_inf("open google form test url")
        chrome.goto(url2go=url, wait_elem_selector="div.F9yp7e.ikZYwf.LgNcQe")

        # input shuffle name
        b64_shuffle_name = base64.b64encode(shuffle_name.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[0].value=atob('{b64_shuffle_name}')")

        # input telegram name
        b64_telegram_name = base64.b64encode(telegram_name.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[1].value=atob('{b64_telegram_name}')")

        # input captcha
        captcha = "kk"
        b64_captcha = base64.b64encode(captcha.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[2].value=atob('{b64_captcha}')")

        # click submit button
        chrome.run_script("document.querySelectorAll('span.NPEfkd.RveJvd.snByac')[0].click()")
    except:
        traceback.print_exc()


def work():
    try:
        log_inf("open browser")
        chrome = Chrome(user_data_dir=PROFILE_DIR)
        chrome.start()

        submit_google_form_test(
            chrome=chrome,
            url="https://forms.gle/4NccFM5EcL12mdnM7",
            shuffle_name="ekudahl",
            telegram_name="ekudahl",
        )

        log_inf("quit browser")
        chrome.quit()
    except:
        traceback.print_exc()


def main():
    work()
    input("Press ENTER to exit.")


if __name__ == "__main__":
    main()
