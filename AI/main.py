from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# LinkedIn login credentials
USERNAME = "Bobsmikkelopmetjekop@gmail.com"
PASSWORD = "Fruitschaal3!"


# Initialize Selenium WebDriver with options
def init_driver():
    print("Initializing the WebDriver...")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    print("WebDriver initialized.")
    return driver


# Login to LinkedIn
def login_to_linkedin(driver):
    print("Navigating to LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    print("Login page loaded.")

    # Enter login credentials
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    print("Entering login credentials...")
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Wait for the LinkedIn homepage to load
    print("Logging in...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Search')]")))
    print("Logged in successfully.")


# Fetch the profile HTML from LinkedIn
def fetch_profile_html(driver, profile_url):
    print(f"Navigating to profile URL: {profile_url}")
    driver.get(profile_url)
    time.sleep(3)  # Allow time for the profile to load
    print("Profile page loaded.")
    return driver.page_source


# Parse profile to extract basic info and "About" section
def parse_profile(html_content):
    print("Parsing profile content...")
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract name
    name_element = soup.find("h1", class_="RIbnCAsTbWzbdDScQkPGXRrQHSaITKZWQhh inline t-24 v-align-middle break-words")
    name = name_element.get_text(strip=True) if name_element else None
    print(f"Name found: {name}")

    # Extract headline
    headline_element = soup.find("div", class_="text-body-medium break-words")
    headline = headline_element.get_text(strip=True) if headline_element else None
    print(f"Headline found: {headline}")

    # Extract location
    location_element = soup.find("span", class_="text-body-small inline t-black--light break-words")
    location = location_element.get_text(strip=True) if location_element else None
    print(f"Location found: {location}")

    # Extract About section
    about_element = soup.find("div", class_="full-width", attrs={"dir": "ltr"})
    about_text = ""
    if about_element:
        # Extract both "aria-hidden" visible text and "visually-hidden" hidden text
        visible_text = about_element.find("span", {"aria-hidden": "true"})
        hidden_text = about_element.find("span", {"class": "visually-hidden"})

        # Combine visible and hidden parts for the complete "About" section
        if visible_text:
            about_text += visible_text.get_text(" ", strip=True)
        if hidden_text:
            about_text += "\n" + hidden_text.get_text(" ", strip=True)

    print(f"About section found: {about_text}")

    # Consolidate all extracted information
    profile_data = {
        "name": name,
        "headline": headline,
        "location": location,
        "about": about_text
    }

    print("Profile parsing complete.")
    return profile_data



# Main function to execute the scraping by profile URL
def scrape_linkedin_by_profile_url(profile_url):
    driver = init_driver()
    try:
        login_to_linkedin(driver)
        profile_html = fetch_profile_html(driver, profile_url)
        profile_data = parse_profile(profile_html)
    finally:
        driver.quit()  # Always close the driver

    print("Scraping process complete.")
    return profile_data


# Run the scraper
if __name__ == "__main__":
    profile_url_to_scrape = "https://www.linkedin.com/in/niels-verheuvel-743364170/"  # Replace with the target profile URL
    profile_data = scrape_linkedin_by_profile_url(profile_url_to_scrape)
    print("Profile data found:")
    print(profile_data)
