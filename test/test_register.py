import time
import unittest
import uuid

from Module.register import register_to_opencart


class TestRegister(unittest.TestCase):

    def test_invalid_firstname(self):
        """Test đăng ký với tên rỗng"""
        result = register_to_opencart("", "Doe", f"{uuid.uuid4().hex}@gmail.com", "ComplexPass123")
        self.assertEqual(result, "Error: First Name must be between 1 and 32 characters!")

    def test_invalid_lastname(self):
        """Test đăng ký với họ rỗng"""
        result = register_to_opencart("John", "", f"{uuid.uuid4().hex}@gmail.com", "ComplexPass123")
        self.assertEqual(result, "Error: Last Name must be between 1 and 32 characters!")

    def test_invalid_email(self):
        """Test đăng ký với email rỗng"""
        result = register_to_opencart("John", "Doe", "", "ComplexPass123")
        self.assertEqual(result, "Error: E-Mail Address does not appear to be valid!")

    def test_email_already_registered(self):
        """Test đăng ký với email đã có trên hệ thống"""
        result = register_to_opencart("John", "Doe", "thamkhang2003@gmail.com", "ComplexPass123")
        self.assertTrue(isinstance(result, str))  # Kiểm tra xem kết quả có phải là chuỗi không
        self.assertIn("Warning: E-Mail Address is already registered!",
                      result)  # Kiểm tra xem có thông báo cảnh báo nào không

    def test_weak_password(self):
        """Test đăng ký với mật khẩu yếu"""
        result = register_to_opencart("John", "Doe", "newemail@example.com", "1234")  # Sử dụng email mới
        self.assertTrue(isinstance(result, str))  # Kiểm tra xem kết quả có phải là chuỗi không
        self.assertNotIn("Warning:", result)  # Không có thông báo cảnh báo

    def test_successful_registration(self):
        """Test đăng ký thành công với thông tin hợp lệ"""
        result = register_to_opencart("Jane", "Doe", f"{uuid.uuid4().hex}@gmail.com", "ComplexPass123!")
        self.assertIsNotNone(result)  # Kết quả không được là None
        # Có thể kiểm tra thêm điều kiện khác tùy thuộc vào yêu cầu của bạn
