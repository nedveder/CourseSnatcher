from time import sleep
from selenium import webdriver
from random import randint

FINAL_CONFIRMATION_TEXT = "המערכת אושרה"

USERNAME = ""
PASSWORD = ""

LOGIN_URL = "https://rishum-net.huji.ac.il/site/student/login.asp"
CONFIRMATION_TEXT = 'אישור המערכת'
CONTINUE_TEXT = "המשך"


def login():
    driver.get(LOGIN_URL)
    # if login button is found on page we loop
    while LOGIN_URL in driver.current_url:
        # Find the username and password fields
        username = driver.find_element(by="id", value="login")
        password = driver.find_element(by="id", value="password")
        # Enter your username and password
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        # Click the login button
        click_btn(value=CONTINUE_TEXT)
        # wait random time to trick system
        sleep(randint(1, 3))


def refresh_occupancy():
    try:
        driver.get(
            'https://rishum-net.huji.ac.il/site/student/accept_time_table_ctl.asp')
        sleep(1)
        # if the button is found on the page we continue
        if CONFIRMATION_TEXT in driver.page_source:
            confirm_schedule()
            if FINAL_CONFIRMATION_TEXT in driver.page_source:
                print("Success!")
                return True
    except Exception as e:
        print("Occupancy not found", end=" ")
    finally:
        driver.get('https://rishum-net.huji.ac.il/site/student/student_main.asp')
        # click on the button to go to the previous page
        click_btn(value="btn_back2")
        # refresh the occupancy page
        click_btn(value="RaanenTfusot")
        click_btn(value="RaanenTfusot")
        click_btn(value="btn_next3")


def confirm_schedule():
    # call save() function to submit the form
    driver.execute_script("save();")
    sleep(1)
    driver.execute_script("save();")
    # mark the checkbox
    click_btn(value="accept")
    # call check_submit() function to submit the form
    sleep(1)
    driver.execute_script("check_submit();")
    sleep(1)


def click_btn(value):
    sleep(1.5)
    driver.find_element(by="id", value=value).click()


if __name__ == '__main__':
    # Create a selenium driver to sign into the website
    driver = webdriver.Firefox()
    login()
    # call SubmitForm() function to submit the form
    driver.execute_script("SubmitForm();")
    # click on the button to go to the next page
    click_btn(value="btn_next2")
    click_btn(value="btn_next3")
    # If text is found on the page, then we do A else B
    i = 1
    while not refresh_occupancy():
        print("Refreshing occupancy for the {} time".format(i))
        i += 1
