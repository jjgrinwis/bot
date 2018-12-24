# credential stuffing tebot
# A test using selenium module using the automation API of the browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import credentials

# Create a new instance of the selenium Chrome driver
# let's feed some commandline parameters to Chrome
# --headless as we don't need user-interface
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--proxy-server=127.0.0.1:8080')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36')

i = 1
while i < 15:
    i += 1

    # now start a headless chrome instance and retrieve page
    driver = webdriver.Chrome(options=chrome_options)

    # we need to wait a couple of seconds
    driver.implicitly_wait(10)

    # no need to delete the cookies.
    print("number of cookies: {}".format(len(driver.get_cookies())))

    driver.get("http://bmp.grinwis.com/wp-login.php")
    driver.get_screenshot_as_file('pre-login.png')

    # now get elements needed to login
    # we found these elements using Katalon Recorder Chrome plugin
    # after an upgrade, we need to select the field using click() method
    user_login = driver.find_element_by_id('user_login')
    user_login.click()
    user_pass = driver.find_element_by_id('user_pass')
    user_pass.click()
    loginform = driver.find_element_by_id('loginform')

    # now enter our credentials and submit
    user_login.send_keys(credentials.username)
    user_pass.send_keys(credentials.password)
    loginform.submit()

    try:
        # now let's wait for the result. If title contains Dashboard we're in
        WebDriverWait(driver, 2).until(EC.title_contains('Dashboard'))
        print("login granted")
        driver.get_screenshot_as_file("output.png")

        # check the cookies we've received
        cookies = driver.get_cookies()
        for cookie in cookies:
            if 'w' not in cookie['name']:
                print("botman cookie: {}".format(cookie['name']))

    except TimeoutException:
        # we didn't get the result with x seconds, permission denied.
        print("login denied")
        # print(driver.page_source)
    finally:
        driver.quit()
