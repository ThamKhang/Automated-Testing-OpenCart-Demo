# login.py
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path


def login_to_opencart(email_address, password):
    driver = get_driver_with_custom_profile(profile_path)
    driver.get("http://localhost/opencart/upload/")

    try:
        # Kiểm tra và đăng xuất nếu người dùng đã đăng nhập
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))).click()

        # Nếu "Logout" tồn tại, thực hiện đăng xuất
        logout_option = driver.find_elements(By.LINK_TEXT, "Logout")
        if logout_option:
            logout_option[0].click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))).click()

        # Bắt đầu quá trình đăng nhập
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()

        email = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-email")))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-password")))

        email.send_keys(email_address)
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].btn.btn-primary"))
        )
        login_button.click()

        # Kiểm tra nếu có cảnh báo đăng nhập thất bại
        try:
            warning_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert .alert-danger"))
            )
            if "Warning: No match for E-Mail Address and/or Password." in warning_message.text:
                print("Login failed: Invalid email or password.")
                driver.quit()
                return None  # Trả về None nếu đăng nhập thất bại
        except TimeoutException:
            # Không tìm thấy cảnh báo, tiếp tục kiểm tra đăng nhập thành công
            pass

        # Kiểm tra đăng nhập thành công
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
        print("Login successful!")

        return driver  # Return the driver for further use or inspection

    except Exception as e:
        print(f"Error during login process: {e}")
        driver.quit()
        return None