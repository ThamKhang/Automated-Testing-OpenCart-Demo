# logout.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path


def initialize_driver():
    return get_driver_with_custom_profile(profile_path)


def logout_from_opencart(driver=None):
    if driver is None:
        print("Driver is not initialized. Attempting to initialize driver.")
        driver = initialize_driver()

    try:
        # Navigate to the account page if not already there
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()
        print("Logged out successfully!")
    except Exception as e:
        print(f"Error during logout process: {e}")
    finally:
        if driver is not None:
            driver.quit()  # Close the driver if it was initialized here
