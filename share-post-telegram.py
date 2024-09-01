import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Define your Telegram group URLs in a list
group_urls = [
    "https://web.telegram.org/#/im?p=g1234567890",  # Replace with actual group URLs
    "https://web.telegram.org/#/im?p=g0987654321",  # Add more as needed
]

# Step 2: Initialize the WebDriver with a specific Chrome profile
def initialize_webdriver():
    options = webdriver.ChromeOptions()
    
    # Set the path to your Chrome profile
    chrome_user_data_dir = "/Users/yourusername/Library/Application Support/Google/Chrome"  # Update with your actual username
    chrome_profile = "Profile 1"  # Replace with your actual profile folder name (e.g., "Profile 1", "Default", etc.)
    
    options.add_argument(f"user-data-dir={chrome_user_data_dir}")
    options.add_argument(f"profile-directory={chrome_profile}")
    
    options.add_argument("--start-maximized")  # Open the browser in maximized mode
    driver = webdriver.Chrome(options=options)
    return driver

# Step 3: Send the URL to each group
def send_url_to_groups(driver, sharing_url):
    for group_url in group_urls:
        logging.info(f"Opening group URL: {group_url}")
        driver.get(group_url)
        time.sleep(5)  # Wait for the group chat to load
        
        try:
            # Step 4: Detect the input message element and send the URL
            input_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
            )
            input_box.click()
            logging.info("Input box found and clicked.")
            time.sleep(1)  # Simulate human delay
            
            input_box.send_keys(sharing_url)
            logging.info(f"URL '{sharing_url}' entered into the input box.")
            time.sleep(2)  # Simulate human delay
            
            # Send the message by pressing Enter
            input_box.send_keys(u'\ue007')  # Unicode for Enter key
            logging.info("Message sent.")
            time.sleep(3)  # Wait a bit after sending before moving to the next group

        except Exception as e:
            logging.error(f"Error sending URL to group: {group_url}, Error: {e}")

# Main function
def main():
    # Step 1: Ask for input URL
    sharing_url = input("Please enter the URL to share: ")
    
    # Step 2: Initialize WebDriver
    logging.info("Initializing WebDriver...")
    driver = initialize_webdriver()
    
    try:
        # Step 3: Send the URL to each group
        send_url_to_groups(driver, sharing_url)
    finally:
        # Step 6: Close the browser
        logging.info("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()
