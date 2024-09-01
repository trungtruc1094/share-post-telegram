import time
import logging
import psutil
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def kill_process_by_name(process_name):
    """Kill all processes by name."""
    for proc in psutil.process_iter():
        try:
            if process_name in proc.name():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def get_telegram_urls():
    response = requests.get('https://script.google.com/macros/s/AKfycbyZupp7HuurRdNt0JkIbu8kRlpQdeWgt6PZ3EWsLbw5f-lb8NcOWesSyVsPAxtpUTkzIg/exec')
    
    if response.status_code == 200:
        data = response.json()
        urls = data.get('urls', [])
        logging.info(f"Telegram URLs: '{urls}'")
        return urls
    else:
        logging.error(f"Failed to retrieve data: {response.status_code}")
        return []

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Define your Telegram group URLs in a list
group_urls = []

# Step 2: Initialize the WebDriver with a specific Chrome profile in headless mode
def initialize_webdriver():
    # Kill any residual Chrome or ChromeDriver processes
    kill_process_by_name("Google Chrome")
    kill_process_by_name("chromedriver")

    options = webdriver.ChromeOptions()
    
    # Set the path to your Chrome profile
    chrome_user_data_dir = "/Users/mac/Library/Application Support/Google/Chrome"  # Update with your actual username
    chrome_profile = "Profile 6"  # Replace with your actual profile folder name (e.g., "Profile 1", "Default", etc.)
    
    options.add_argument(f"user-data-dir={chrome_user_data_dir}")
    options.add_argument(f"profile-directory={chrome_profile}")
    
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (useful for headless)
    options.add_argument("--start-maximized")  # Open the browser in maximized mode

    # This option is useful to allow WebDriver to find elements in headless mode
    options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(options=options)
    return driver

def simulate_typing(element, text):
    """Simulate typing each character with a random delay."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Random delay between each keystroke

def human_like_delay(min_seconds=1, max_seconds=3):
    """Introduce a random delay to simulate human-like actions."""
    time.sleep(random.uniform(min_seconds, max_seconds))

# Step 3: Send the URL to each group
def send_url_to_groups(driver, sharing_url):
    group_urls = get_telegram_urls()
    for i, group_url in enumerate(group_urls):
        try:
            logging.info(f"Opening group URL: {group_url}")
            
            # Open the group URL in a new tab
            if i == 0:
                driver.get(group_url)  # Open the first URL in the current tab
            else:
                driver.execute_script("window.open('');")  # Open a new tab
                driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
                driver.get(group_url)  # Open the group URL in the new tab
            
            human_like_delay(4, 6)  # Wait for the group chat to load
            
            # Step 4: Detect the input message element and send the URL
            input_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="editable-message-text"]'))
            )
            input_box.click()
            logging.info("Input box found and clicked.")
            human_like_delay(1, 2)  # Simulate human delay
            
            simulate_typing(input_box, sharing_url)  # Simulate typing the URL
            logging.info(f"URL '{sharing_url}' entered into the input box.")
            human_like_delay(2, 3)  # Simulate human delay
            
            # Send the message by pressing Enter
            input_box.send_keys(u'\ue007')  # Unicode for Enter key
            logging.info("Message sent.")
            human_like_delay(3, 5)  # Wait a bit after sending before moving to the next group

        except Exception as e:
            logging.error(f"Error processing group URL '{group_url}': {e}")
            screenshot_path = f"screenshot_error_{i}.png"
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot taken and saved as {screenshot_path}")

        finally:
            # Close the previous tab if not the first one
            if i > 0:
                driver.close()  # Close the previous tab
                driver.switch_to.window(driver.window_handles[0])  # Switch back to the first tab

# Main function
def main():
    # Step 1: Retrieve the latest URL directly within the main function
    logging.info("Retrieving the latest URL...")
    config = {
        'google_sheets': {
            'script_url': 'https://script.google.com/macros/s/AKfycbwqjk9UtKGEoxUhym12-XTsXPXN3VgigRGVOuBhwQd7bHFpV6dncJzHEsROVrsUAGxdKw/exec'  # Replace with your actual Google Apps Script URL
        }
    }
    
    script_url = config['google_sheets']['script_url']
    params = {
        'action': 'getLatestShareURL'  # Specify the action to retrieve the latest URL
    }
    
    try:
        response = requests.get(script_url, params=params)
        latest_url = response.text.strip()

        if not latest_url or latest_url == "Sheet not found" or latest_url == "No data found in column E":
            logging.error("No latest URL found or an error occurred.")
            return  # Exit if no valid URL is retrieved

        logging.info(f"Retrieved latest URL: {latest_url}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while retrieving the latest URL: {e}")
        return  # Exit if there's an error with the request

    # Step 2: Initialize WebDriver
    logging.info("Initializing WebDriver...")
    driver = initialize_webdriver()
    
    try:
        # Step 3: Send the URL to each group
        send_url_to_groups(driver, latest_url)
    finally:
        # Step 6: Close the browser
        logging.info("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
