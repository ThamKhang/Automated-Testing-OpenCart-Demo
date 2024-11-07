import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path


def add_single_product_to_wishlist():
    driver = get_driver_with_custom_profile(profile_path)
    driver.get("https://demo.opencart.com/en-gb/catalog/desktops")
    try:
        # Tìm nút "Add to Wish List" cho sản phẩm "Apple Cinema 30" trên trang
        wishlist_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='content']//h4/a[text()='Canon EOS 5D']/../../..//button[@data-bs-toggle='tooltip' and @title='Add to Wish List']"))
        )

        print("Found the wishlist button for Apple Cinema 30.")

        # Kiểm tra nếu nút có thể nhấp được
        if wishlist_button.is_enabled():
            # Cuộn đến nút và nhấp vào nó
            driver.execute_script("arguments[0].scrollIntoView(true);", wishlist_button)
            ActionChains(driver).move_to_element(wishlist_button).click().perform()
            print("Apple Cinema 30 added to Wish List!")
            time.sleep(20)
        else:
            print("Button is disabled, skipping...")
    except Exception as e:
        print(f"Error adding Apple Cinema 30 to Wish List: {e}")


def add_all_to_wishlist():
    driver = get_driver_with_custom_profile(profile_path)
    driver.get("https://demo.opencart.com/en-gb/catalog/desktops")
    try:
        # Tìm tất cả các nút "Add to Wish List" trên trang
        wishlist_buttons = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[title='Add to Wish List']"))
        )

        print(f"Found {len(wishlist_buttons)} wishlist buttons.")

        # Nhấp vào từng nút "Add to Wish List"
        for index, button in enumerate(wishlist_buttons):
            # Cuộn từ từ đến nút "Add to Wish List"
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)  # Thời gian chờ cho việc cuộn mượt

            try:
                # Dùng JavaScript click để tránh bị chặn
                driver.execute_script("arguments[0].click();", button)
                print(f"Product {index + 1} added to Wish List!")
            except Exception as click_exception:
                print(f"Could not click on button {index + 1}: {click_exception}")
            time.sleep(2)

    except Exception as e:
        print(f"Error adding products to Wish List: {e}")
    finally:
        driver.quit()