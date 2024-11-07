from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path

def register_to_opencart(first_name, last_name, email, password):
    driver = get_driver_with_custom_profile(profile_path)
    driver.get("https://demo.opencart.com/")

    try:
        # Kiểm tra và đăng xuất nếu người dùng đã đăng nhập
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))).click()

        # Nếu "Logout" tồn tại, thực hiện đăng xuất
        logout_option = driver.find_elements(By.LINK_TEXT, "Logout")
        if logout_option:
            logout_option[0].click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account"))).click()

        # Chuyển đến trang đăng ký
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Register"))).click()

        # Điền thông tin đăng ký
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys(
            first_name)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-lastname"))).send_keys(
            last_name)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(email)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "input-password"))).send_keys(password)

        # Đồng ý với điều khoản
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='agree']"))).click()

        # Gửi biểu mẫu đăng ký
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].btn.btn-primary"))
        ).click()

        # Kiểm tra cảnh báo dưới ô nhập
        try:
            if first_name == "":
                error_message = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "error-firstname"))
                ).text
                print(f"First Name Error: {error_message}")  # In thông báo lỗi cho tên
                return f"Error: {error_message}"

            if last_name == "":
                error_message = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "error-lastname"))
                ).text
                print(f"Last Name Error: {error_message}")  # In thông báo lỗi cho họ
                return f"Error: {error_message}"

            if "@" not in email or "." not in email.split("@")[-1]:  # Đơn giản kiểm tra email
                error_message = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "error-email"))
                ).text
                print(f"Email Error: {error_message}")  # In thông báo lỗi cho email
                return f"Error: {error_message}"
        except TimeoutException:
            print("No input field errors found.")  # Không có cảnh báo dưới ô nhập

        # Kiểm tra cảnh báo trên thông báo
        try:
            warning_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger"))
            ).text
            print(f"Warning Message: {warning_message}")  # In thông báo cảnh báo
            return f"Warning: {warning_message}"
        except TimeoutException:
            print("No warning messages found.")  # Không có cảnh báo

        # Kiểm tra xem đăng ký thành công
        WebDriverWait(driver, 10).until(
            EC.title_contains("Your Account Has Been Created!")
        )
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#content h1"))
        ).text

        if "Your Account Has Been Created!" in success_message:
            print("Registration successful!")
            return driver  # Return driver for further actions if needed
        else:
            print("Registration failed!")
            driver.quit()
            return None

    except Exception as e:
        print(f"Error during registration process: {e}")
        driver.quit()
        return None
