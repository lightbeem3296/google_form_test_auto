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
