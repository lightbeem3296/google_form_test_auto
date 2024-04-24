# crawler.py --shuffle_name=ekudahl --telegram_name=ekudahl

import argparse
import base64
import os
import traceback
from hashlib import md5
from pathlib import Path

from libchrome import Chrome
from liblogger import log_inf

CUR_DIR = str(Path(__file__).parent.absolute())
TEMP_DIR = os.path.join(CUR_DIR, "temp")


def submit_google_form_test(chrome: Chrome, url: str, shuffle_name: str, telegram_name: str):
    try:
        # go to google form test url and wait until title "Google Form Test" is selecable
        log_inf("open google form test url")
        chrome.goto(url2go=url, wait_elem_selector="div.F9yp7e.ikZYwf.LgNcQe")

        # click check box
        chrome.click(selector="label.docssharedWizToggleLabeledContainer.OLkl6c")

        # input shuffle name
        b64_shuffle_name = base64.b64encode(shuffle_name.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[0].value=atob('{b64_shuffle_name}')")

        # input telegram name
        b64_telegram_name = base64.b64encode(telegram_name.encode()).decode()
        chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[1].value=atob('{b64_telegram_name}')")

        # input captcha
        math_eq = chrome.run_script(
            """
elems = document.querySelectorAll('span.M7eMe');
elem = elems[elems.length - 1];
elem.innerText"""
        )
        if math_eq != None:
            math_eq = math_eq.replace("x", "*")
            eq_res = str(eval(math_eq))
            b64_captcha = base64.b64encode(eq_res.encode()).decode()
            chrome.run_script(f"document.querySelectorAll('input.whsOnd.zHQkBf')[2].value=atob('{b64_captcha}')")

        # click submit button
        chrome.run_script("document.querySelectorAll('span.NPEfkd.RveJvd.snByac')[0].click()")
    except:
        traceback.print_exc()


def work(shuffle_name: str, telegram_name: str):
    try:
        log_inf("open browser")
        profile_dir_name = (
            f"profile_{md5(shuffle_name.encode()).hexdigest()[:8]}_{md5(telegram_name.encode()).hexdigest()[:8]}"
        )
        chrome = Chrome(user_data_dir=os.path.join(TEMP_DIR, profile_dir_name))
        chrome.start()

        # login google account
        chrome.goto(
            url2go="https://myaccount.google.com/",
            wait_elem_selector="h1.XY0ASe",
        )

        # submit google form test
        submit_google_form_test(
            chrome=chrome,
            url="https://forms.gle/4NccFM5EcL12mdnM7",
            shuffle_name=shuffle_name,
            telegram_name=telegram_name,
        )

        input("Press ENTER to close browser.")
        log_inf("quit browser")
        chrome.quit()
    except:
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--shuffle_name",
        dest="shuffle_name",
        type=str,
        required=True,
        help="Shuffle name to input in Google Form Test.",
    )
    parser.add_argument(
        "--telegram_name",
        dest="telegram_name",
        type=str,
        required=True,
        help="Shuffle name to input in Google Form Test.",
    )
    args = parser.parse_args()
    work(
        shuffle_name=args.shuffle_name,
        telegram_name=args.telegram_name,
    )


def test():
    work(
        shuffle_name="ekudahl",
        telegram_name="ekudahl",
    )


if __name__ == "__main__":
    main()
    # test()

    input("Press ENTER to exit.")
