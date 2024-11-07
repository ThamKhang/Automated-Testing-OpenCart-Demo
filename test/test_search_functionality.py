import pytest
from selenium.webdriver.common.by import By

from Custom.custom_user_agent import get_driver_with_custom_profile
from Module.login import login_to_opencart
from Module.search import search_products
from config import profile_path
from test.test_login import VALID_EMAIL, VALID_PASSWORD


class TestSearchFunctionality:
    @pytest.fixture(scope="class", autouse=True)
    def driver(self):
        """Thiết lập driver cho tất cả các bài kiểm thử"""
        driver = login_to_opencart(VALID_EMAIL, VALID_PASSWORD)
        driver.get("https://demo.opencart.com/")
        yield driver
        driver.quit()

    def test_correct_search_products(self, driver):
        """Kiểm tra tìm kiếm với từ khóa hợp lệ"""
        existent_keyword = "Iphone"
        results = search_products(driver, existent_keyword)
        assert len(results) > 0, "Không tìm thấy sản phẩm cho 'Iphone'"
        print(f"Kiểm tra tìm kiếm hợp lệ thành công. Sản phẩm tìm thấy: {len(results)}.")

    def test_search_with_no_exist_products(self, driver):
        """Kiểm tra tìm kiếm với sản phẩm không tồn tại"""
        nonexistent_keyword = "dep tong lao"
        results = search_products(driver, nonexistent_keyword)
        assert len(results) == 0, f"Đã tìm thấy sản phẩm cho '{nonexistent_keyword}', nhưng không mong muốn."
        print(f"Kiểm tra sản phẩm không tồn tại thành công. Không tìm thấy sản phẩm.")

    def test_search_with_uppercase_all_text(self, driver):
        """Kiểm tra tìm kiếm với ký tự hoa"""
        uppercase_keyword = "IPHONE"
        results = search_products(driver, uppercase_keyword)
        assert len(results) > 0, f"Đã tìm thấy sản phẩm cho '{uppercase_keyword}', nhưng không có sản phẩm nào."
        print(f"Kiểm tra từ khóa viết hoa '{uppercase_keyword}' thành công. Sản phẩm tìm thấy: {len(results)}.")

    def test_search_with_lowercase_all_text(self, driver):
        """Kiểm tra tìm kiếm với ký tự thường"""
        lowercase_keyword = "iphone"
        results = search_products(driver, lowercase_keyword)
        assert len(results) > 0, f"Đã tìm thấy sản phẩm cho '{lowercase_keyword}', nhưng không có sản phẩm nào."
        print(f"Kiểm tra từ khóa viết thường '{lowercase_keyword}' thành công. Sản phẩm tìm thấy: {len(results)}.")

    def test_search_special_characters(self, driver):
        """Kiểm tra tìm kiếm với ký tự đặc biệt"""
        special_character_search_query = "!@#$%^&*()_+"
        results = search_products(driver, special_character_search_query)
        assert len(results) == 0, f"Đã tìm thấy sản phẩm cho tìm kiếm ký tự đặc biệt, nhưng không mong muốn."
        print("Kiểm tra tìm kiếm ký tự đặc biệt thành công. Không tìm thấy sản phẩm.")

    def test_search_with_whitespace_surrounded(self, driver):
        """Kiểm tra tìm kiếm với từ khóa có khoảng trắng xung quanh"""
        keyword_with_whitespace = "  Iphone  "
        results = search_products(driver, keyword_with_whitespace)
        assert len(
            results) > 0, f"Hy vọng tìm thấy sản phẩm cho '{keyword_with_whitespace}', nhưng không có sản phẩm nào."
        print(f"Kiểm tra từ khóa có khoảng trắng '{keyword_with_whitespace}' thành công. Sản phẩm tìm thấy.")

    def test_search_empty_characters(self, driver):
        """Kiểm tra tìm kiếm với chuỗi rỗng"""
        empty_search_query = ""
        results = search_products(driver, empty_search_query)
        assert len(results) == 0, f"Đã tìm thấy sản phẩm cho tìm kiếm rỗng, nhưng không mong muốn."
        print("Kiểm tra tìm kiếm với ký tự trống thành công. Không tìm thấy sản phẩm.")

    def test_search_with_special_character_in_text(self, driver):
        """Kiểm tra tìm kiếm với ký tự đặc biệt trong tên sản phẩm"""
        special_characters_keyword = "!Iphone"
        results = search_products(driver, special_characters_keyword)
        assert len(results) == 0, f"Đã tìm thấy sản phẩm cho '{special_characters_keyword}', nhưng không mong muốn."
        print(f"Kiểm tra từ khóa có ký tự đặc biệt '{special_characters_keyword}' thành công. Không tìm thấy sản phẩm.")

    def test_search_with_long_character_in_text(self, driver):
        """Kiểm tra tìm kiếm với chuỗi ký tự dài"""
        long_keyword = "z" * 100  # Tạo một từ khóa dài
        results = search_products(driver, long_keyword)

        # Xác nhận không tìm thấy sản phẩm với từ khóa dài
        assert len(results) == 0, f"Hy vọng không tìm thấy sản phẩm cho từ khóa dài, nhưng đã tìm thấy {len(results)}."
        print(f"Kiểm tra từ khóa dài '{long_keyword}' thành công. Không tìm thấy sản phẩm.")

        # Kiểm tra bố cục bằng cách so sánh chiều rộng trang với chiều rộng viewport
        page_width = driver.execute_script("return document.body.scrollWidth;")
        viewport_width = driver.execute_script("return window.innerWidth;")
        assert page_width <= viewport_width, "Bố cục trang bị hỏng và có cuộn ngang."
        print("Kiểm tra bố cục thành công. Không có cuộn ngang.")
