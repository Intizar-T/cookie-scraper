import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["POST"])
def scraper():
    return scrape()


def driver_settings(headless: bool = True):
    opts = webdriver.ChromeOptions()

    if headless:
        opts.add_argument("--headless=new")

    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--disable-blink-features=AutomationControlled")

    return opts


def print_text(elems, type):
    if type == "text":
        for elem in elems:
            print(elem.text)
        return
    for elem in elems:
        print(elem.get_attribute(type))


def scrape():
    options = driver_settings(headless=False)
    driver = webdriver.Chrome(
        options=options,
    )
    driver.get("https://test.deepblock.net/")
    time.sleep(10)

    try:
        # find signin button and click -> redirects to the login page
        buttons = driver.find_elements(By.TAG_NAME, "button")
        signin_button = [button for button in buttons if button.text == "SIGN UP / IN"][
            0
        ]
        signin_button.click()
        time.sleep(10)

        # find Google login button and click -> redirects to a new page
        a_tags = driver.find_elements(By.TAG_NAME, "a")
        for a_tag in a_tags:
            if (
                a_tag.get_attribute("href")
                == "https://test.deepblock.net/api/login/google?referer=https://test.deepblock.net"
            ):
                google_tag = a_tag
                break
        google_tag.click()
        time.sleep(10)

        # fill in the email
        email = "intizartashow99@gmail.com"
        email_input_div = driver.find_element(By.CLASS_NAME, "Xb9hP")
        email_inputs = email_input_div.find_elements(By.TAG_NAME, "input")
        email_input = email_inputs[0]
        email_input.send_keys(email)
        time.sleep(3)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        next_button = [button for button in buttons if button.text == "Next"][0]
        next_button.click()
        time.sleep(10)

        # fill in the password
        password = "Insignia@123"
        password_input_div = driver.find_element(By.CLASS_NAME, "Xb9hP")
        password_inputs = password_input_div.find_elements(By.TAG_NAME, "input")
        password_input = password_inputs[0]
        password_input.send_keys(password)
        time.sleep(3)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        next_button = [button for button in buttons if button.text == "Next"][0]
        next_button.click()
        time.sleep(10)

        # get cookies
        cookie_obj = driver.get_cookie("connect.sid")
        cookie_name = cookie_obj.get("name", "Couldn't find the cookie")
        if cookie_name == "connect.sid":
            return cookie_obj["value"]
        else:
            return cookie_name
    except Exception as error:
        return error


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
