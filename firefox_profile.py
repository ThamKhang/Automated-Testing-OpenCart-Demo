import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def create_firefox_profile(profile_path):
    """
    Manually create a Firefox profile by opening Firefox and allowing the user
    to configure it, then save the profile for Selenium to use later.
    """
    # Ensure the profile path exists
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    # Start Firefox with the custom profile path
    options = Options()
    options.add_argument(f"-profile")
    options.add_argument(profile_path)  # Use the specified profile path

    # Start Firefox for configuration
    print("Opening Firefox to create profile...")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    # Prompt user to configure profile
    print("Configure the Firefox profile and close the browser when done.")
    driver.get("https://www.google.com")  # Open any URL to verify the browser is launched
    input("Press Enter after closing the browser to finish creating the profile.")

    driver.quit()
    print(f"Profile created at: {profile_path}")


def get_firefox_driver_with_profile(profile_path):
    """
    Function to initialize the WebDriver with the created profile.
    """
    options = Options()
    options.add_argument(f"-profile")
    options.add_argument(profile_path)  # Use the saved profile path

    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)


if __name__ == "__main__":
    # Set up profile directory path
    current_directory = os.path.dirname(os.path.abspath(__file__))
    profile_path = os.path.join(current_directory, "my_firefox_profile")

    # Check if profile exists, otherwise create it
    if not os.path.exists(profile_path) or not os.listdir(profile_path):
        create_firefox_profile(profile_path)
    else:
        print(f"Profile already exists at: {profile_path}")

    # Start WebDriver with the saved profile
    driver = get_firefox_driver_with_profile(profile_path)
    driver.get("https://demo.opencart.com/")

    # Perform actions (e.g., login, verify)
    time.sleep(100)  # Pause to observe the loaded page
    driver.quit()