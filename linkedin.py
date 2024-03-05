from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pypyodbc as odbc
from mail_tester import create_email
import uuid

def login(driver, username, password):
    driver.get("https://www.linkedin.com/home")
    time.sleep(5)
    username_field = driver.find_element(By.NAME, "session_key")
    password_field = driver.find_element(By.NAME, "session_password")

    time.sleep(5)

    username_field  .send_keys(username)
    time.sleep(5)
    
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(10)


def process_page(driver, linkedin_url,url):
    driver.get(linkedin_url + "/people")
    time.sleep(10)

    visited_names = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        
        profile_cards = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'org-people-profile-card')))
        for card in profile_cards:
            name_element = card.find_element(By.CLASS_NAME, 'org-people-profile-card__profile-title')
            name = name_element.text.strip()
            if name not in visited_names and name != "LinkedIn Member":
                name_parts=name.split(' ')
                if len(name_parts) == 2:
                    first_name, last_name = name_parts
                    print("First Name:", first_name)
                    print("Last Name:", last_name)
                    string EmailAddrss = getPersonEmail(first_name, last_name, url)
                else:
                    print("Different name format:", name)

            profile_link_element = card.find_element(By.CLASS_NAME, 'app-aware-link')
            profile_link = profile_link_element.get_attribute('href')

            subtitle_element = card.find_element(By.CLASS_NAME, 'lt-line-clamp--multi-line')
            subtitle_text = subtitle_element.text.strip()

            print("Name:", name)
            print("LinkedIn Profile Link:", profile_link)
            print("Designation:", subtitle_text)
            print("\n")

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def process_website(driver, url):
    print("Processing:", url)
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        base_url = f"https://{url}"
        driver.get(base_url)
        time.sleep(5)
        all_links = driver.find_elements(By.TAG_NAME, 'a')
        website_pages = []
        linkedin_url = None

        for link in all_links:
            href = link.get_attribute('href')
            if href:
                href = href.lower()
                if ('contact' in href or 'about' in href) and href not in website_pages:
                    website_pages.append(href)

        try:
            linkedin_link = driver.find_element(By.CSS_SELECTOR, 'a[href*="linkedin.com"]')
            linkedin_url = linkedin_link.get_attribute('href')
        except NoSuchElementException:
            print("LinkedIn link not found.")

        if linkedin_url is not None:
            print(linkedin_url)
            process_page(driver, linkedin_url,url)
        else:
            for page in website_pages:
                try:
                    driver.get(page)
                    time.sleep(2)
                    linkedin_link = driver.find_element(By.CSS_SELECTOR, 'a[href*="linkedin.com"]')
                    linkedin_url = linkedin_link.get_attribute('href')
                    print(linkedin_url)
                    process_page(driver, linkedin_url,url)
                except NoSuchElementException:
                    print("LinkedIn link not found. Skipping this website page.")

    except Exception as e:
        print(f"Error occurred while processing {url}: {str(e)}")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def run(username, password, websites):
    driver = webdriver.Chrome()
    try:
        login(driver, username, password)

        for url in websites:
            process_website(driver, url)

    finally:
        driver.quit()


DriverName = 'SQL Server'
ServerName = '192.168.0.207\CRM2017'
DatabaseName = 'KGNCRM'
Username = ''
Password = ''

connectionString = f"""
Driver={{{DriverName}}};
Server={ServerName};
Database={DatabaseName};
UID={Username};
PWD={Password};
"""

conn = odbc.connect(connectionString)

cursor = conn.cursor()

query = "SELECT website1 FROM tblcompany WHERE usergroupid = ?"
parameter = "ugp-abcd796a-f83b-4154-ba9d-95f602c93f78"
cursor.execute(query, (parameter,))
result = cursor.fetchall()
websites = [str(row[0]) for row in result]
print(websites)

conn.close()
username = "stuart.jacobs@kgntechnologies.com"
password = ""

run(username, password, websites)
