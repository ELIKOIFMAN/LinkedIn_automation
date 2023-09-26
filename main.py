from selenium import webdriver
import time
import back
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


# ------------dont change---------------
def wait_id(element, max_attempts=3):
    for i in range(max_attempts):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element)))
            return  # Element found, no need to continue waiting
        except Exception as e:
            print(f"Failed to locate element with ID '{element}': {str(e)}")
            driver.refresh()
    print("Exiting due to failure.")
    driver.quit()


def wait_xpath(element, max_attempts=3):
    for i in range(max_attempts):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
            return  # Element found, no need to continue waiting
        except Exception as e:
            print(f"Failed to locate {element}: {str(e)}")
            driver.refresh()
    print("Exiting due to failure.")
    driver.quit()


def wait_css_selector(element, max_attempts=3):
    for i in range(max_attempts):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
            return  # Element found, no need to continue waiting
        except Exception as e:
            print(f"Failed to locate element with CSS selector '{element}': {str(e)}")
            driver.refresh()
    print("Exiting due to failure.")
    driver.quit()


# --------------------------------------


# get into Linkedin homepage
driver.get('https://www.linkedin.com/?trk=seo-authwall-base_nav-header-logo')
wait_id("session_key")

# login section (dont forget to enter your username & password in the back file)
driver.find_element(by=By.ID, value="session_key").send_keys(back.user_name)
driver.find_element(by=By.ID, value="session_password").send_keys(back.password)

# enter linkedin
enter_linkedin = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
enter_linkedin.click()
wait_css_selector('.search-global-typeahead__input')

# search for one of the roles inside -> "role_list"
search_bar = driver.find_element(By.CSS_SELECTOR, '.search-global-typeahead__input')
search_bar.click()
search_bar.send_keys(back.random_role)
search_bar.send_keys(Keys.ENTER)

# find searchFilter_network option in people section
wait_xpath("//ul[@class='reusable-search__entity-cluster--quick-filter-action-container']/li")
herf_list = driver.find_elements(By.XPATH,
                                 "//ul[@class='reusable-search__entity-cluster--quick-filter-action-container']/li")

# Iterate through the searchFilter_network list
for item in herf_list:
    # Check if the item's text contains "2nd"
    if "2nd" in item.text:
        # Find the link element within the list item and get it
        link_element = item.find_element(By.XPATH, "./a")
        href = link_element.get_attribute("href")
        driver.get(href)
        time.sleep(5)
        break

while True:
    # Find all button element that exist on the current page
    all_buttons = driver.find_elements(By.TAG_NAME, "button")
    print("wait 3 seconds until the page will load")
    time.sleep(3)

    connect_count = 0  # Counter for the number of "Connect" buttons found

    for button in all_buttons:
        try:
            if "Connect" in button.text:  # Click the "Connect" buttons and send invitations
                button.click()
                wait_xpath("//button[@aria-label='Send now']")
                driver.find_element(By.XPATH, "//button[@aria-label='Send now']").click()
                time.sleep(1.5)
                connect_count += 1  # Increment the "Connect" button counter
            elif "Connect" not in button.text:
                connect_count += 1
                continue
        except Exception as e:
            # in case of a popup the exception will print what happened and refresh the page to handle it
            print(f"{e} was the issue")
            time.sleep(1)
            driver.refresh()
            time.sleep(2)
            continue

    # Check if all buttons have been checked and move to the next page
    if connect_count == len(all_buttons):
        try:
            print(f"All {connect_count} buttons on this page have been checked.")
            wait_xpath("//button[@aria-label='Next']")
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
            if not next_button.is_enabled():
                break  # Exit the loop if the "Next" button is disabled (no more pages)
            next_button.click()
            time.sleep(2.5)
        except Exception as e:
            # in case of a popup the exception will print what happened and refresh the page to handle it
            print(f"{e} was the issue")
            time.sleep(1)
            driver.refresh()
            time.sleep(2)
            continue
