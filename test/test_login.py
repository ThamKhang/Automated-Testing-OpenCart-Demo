# test_login.py
import pytest
from Module.login import login_to_opencart

# Thông tin đăng nhập mẫu
VALID_EMAIL = "thamkhang2003@gmail.com"
VALID_PASSWORD = "PUEb5@7Lard"
INVALID_EMAIL = "invalid@example.com"
INVALID_PASSWORD = "invalid_password"

class TestLogin:
    def test_login_success(self):
        """Kiểm tra đăng nhập thành công với thông tin hợp lệ."""
        driver = login_to_opencart(VALID_EMAIL, VALID_PASSWORD)
        assert driver is not None, "Đăng nhập thành công nhưng driver không được trả về."
        driver.quit()  # Đóng trình duyệt sau khi kiểm thử

    def test_login_failure(self):
        """Kiểm tra đăng nhập thất bại với thông tin không hợp lệ."""
        driver = login_to_opencart(INVALID_EMAIL, INVALID_PASSWORD)
        assert driver is None, "Đăng nhập thất bại nhưng driver vẫn được trả về."

    def test_login_with_blank_fields(self):
        """Kiểm tra đăng nhập với email và mật khẩu trống."""
        driver = login_to_opencart("", "")
        assert driver is None, "Đăng nhập với thông tin trống nhưng driver vẫn được trả về."

    def test_login_with_valid_email_and_invalid_password(self):
        """Kiểm tra đăng nhập thất bại với email hợp lệ và mật khẩu không hợp lệ."""
        driver = login_to_opencart(VALID_EMAIL, INVALID_PASSWORD)
        assert driver is None, "Đăng nhập thất bại nhưng driver vẫn được trả về khi dùng email hợp lệ và mật khẩu sai."

    def test_login_with_invalid_email_and_valid_password(self):
        """Kiểm tra đăng nhập thất bại với email không hợp lệ và mật khẩu hợp lệ."""
        driver = login_to_opencart(INVALID_EMAIL, VALID_PASSWORD)
        assert driver is None, "Đăng nhập thất bại nhưng driver vẫn được trả về khi dùng email sai và mật khẩu hợp lệ."

    def test_login_with_invalid_email_format(self):
        """Kiểm tra đăng nhập thất bại với định dạng email không hợp lệ."""
        invalid_email_format = "invalid-email-format"
        driver = login_to_opencart(invalid_email_format, VALID_PASSWORD)
        assert driver is None, "Đăng nhập thất bại nhưng driver vẫn được trả về khi dùng định dạng email không hợp lệ."