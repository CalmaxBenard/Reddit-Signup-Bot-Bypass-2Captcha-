from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions
from time import sleep
import random
import os
from captcha import solve_recaptcha

URL = 'https://www.reddit.com/'

emails = ["calmax12@gmail.com", "cynthiaadhiambo9@gmail.com", "calmaxbenard6@gmail.com", "calmax.bn@gmail.com",
          "qwriters1@gmail.com", "calmaxbenad@gmail.com", "emmyvoenter@gmail.com", "bensonmuta195@gmail.com",
          "terrymungai213@gmail.com"]

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
           'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


site_key = os.environ.get("SITE_KEY")
site_url = os.environ.get("SITE_URL")


# Generate a secure password
def generate_password():
    new_password = ""

    for letter in range(random.randint(5, 7)):
        new_password += random.choice(letters)

    for symbol in range(random.randint(4, 5)):
        new_password += random.choice(symbols)

    for num in range(random.randint(3, 4)):
        new_password += random.choice(numbers)

    password_shuffled = ''.join(random.sample(new_password, len(new_password)))
    return password_shuffled


run = 1
while True:
    print(f"That was run {run}")

    # Chrome setup
    driver = webdriver.Chrome()

    # go to reddit homepage
    driver.get(URL)

    # Ignored exceptions
    ignore = (NoSuchElementException, StaleElementReferenceException)

    # wait for 5 seconds
    sleep(5)

    # Get the login button and click it
    login = WebDriverWait(driver, 1000, ignored_exceptions=ignore) \
        .until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Log In")))
    login.click()

    # wait for 2 seconds
    sleep(10)

    # get the register page

    try:
        driver.get("https://www.reddit.com/register")
        # Get the email input
        email = WebDriverWait(driver, 100, ignored_exceptions=ignore) \
            .until(expected_conditions.presence_of_element_located((By.ID, "regEmail")))

    except TimeoutException:
        print("We go again!")
        driver.quit()
        # Chrome setup
        driver = webdriver.Chrome()

        # go to reddit homepage
        driver.get(URL)

        sleep(5)
        login = WebDriverWait(driver, 1000, ignored_exceptions=ignore) \
            .until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Log In")))
        login.click()

        sleep(2)
        driver.get("https://www.reddit.com/register")
        email = WebDriverWait(driver, 100, ignored_exceptions=ignore) \
            .until(expected_conditions.presence_of_element_located((By.ID, "regEmail")))

    # randomly choose an email from the list provided
    chosen_email = random.choice(emails)

    # enter the email
    for ch in chosen_email:
        email.send_keys(ch)

    sleep(5)
    # press enter to proceed
    email.send_keys(Keys.ENTER)

    sleep(5)
    names = []
    # Hold the suggested names and append them to the names list
    suggested_usernames = WebDriverWait(driver, 1000, ignored_exceptions=ignore) \
        .until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "Onboarding__usernameSuggestion")))

    for name in suggested_usernames:
        names.append(name.text)

    # choose a random name and password
    name = random.choice(names)
    password = generate_password()

    # Append the chosen name and password to the data file
    with open("data.txt", "a") as data_file:
        if name != "" and password != "":
            data_file.write(f"\n{name},{password}")

    # Get the registration name input field and enter the chosen name
    reg_username = WebDriverWait(driver, 1000, ignored_exceptions=ignore) \
        .until(expected_conditions.presence_of_element_located((By.ID, "regUsername")))

    for ch in name:
        reg_username.send_keys(ch)

    # Get the registration password field and enter the chosen password
    reg_password = WebDriverWait(driver, 1000, ignored_exceptions=ignore) \
        .until(expected_conditions.presence_of_element_located((By.ID, "regPassword")))

    for ch in password:
        reg_password.send_keys(ch)

    # Bypass Recaptcha
    result = solve_recaptcha(
        site_key=site_key,
        url=site_url
    )

    code = result['code']
    print(code)
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'g-recaptcha-response'))
        )
    except TimeoutException:
        print("Code broke before signup!")

    driver.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")

    sign_up = WebDriverWait(driver, 10, ignored_exceptions=ignore) \
        .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "SignupButton")))
    sign_up.click()
    sleep(10)
    driver.quit()
    sleep(660)
    run += 1
