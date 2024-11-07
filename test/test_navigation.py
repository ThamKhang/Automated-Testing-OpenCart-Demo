import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path

@pytest.fixture(scope="class")
def driver():
    driver = get_driver_with_custom_profile(profile_path)
    driver.get('https://demo.opencart.com/')
    yield driver
    driver.quit()

class TestNavigation:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def test_click_desktops_and_mac(self):
        # Click vào "Desktops" trong navbar
        desktops_menu = self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle[href*="catalog/desktops"]')
        desktops_menu.click()

        # Click vào "Mac" trong mục con của "Desktops"
        mac_subcategory = self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href*="catalog/desktops/mac"]')
        mac_subcategory.click()

        # Xác nhận tiêu đề trang bao gồm "Mac"
        assert 'Mac' in self.driver.title

    def test_show_all_desktops(self):
        # Click vào "Desktops" và sau đó "Show All Desktops"
        self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle[href*="catalog/desktops"]').click()
        show_all_link = self.driver.find_element(By.CSS_SELECTOR, 'a.see-all[href*="catalog/desktops"]')
        show_all_link.click()

        # Kiểm tra tiêu đề trang bao gồm "Desktops"
        assert 'Desktops' in self.driver.title

    def test_menu_navigation(self):
        # Danh sách các mục menu để kiểm thử
        menu_items = [
            {"name": "Desktops", "sub_items": ["PC (0)", "Mac (1)"]},
            {"name": "Laptops & Notebooks", "sub_items": ["Macs (0)", "Windows (0)"]},
            {"name": "Components", "sub_items": ["Mice and Trackballs (0)", "Monitors (2)", "Printers (0)", "Scanners (0)", "Web Cameras (0)"]},
            {"name": "MP3 Players", "sub_items": ["test 11 (0)", "test 12 (0)", "test 15 (0)"]}
        ]

        for item in menu_items:
            # Tìm và di chuột qua mục menu
            menu = self.wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, item["name"]))
            )
            ActionChains(self.driver).move_to_element(menu).perform()

            # Kiểm tra từng mục con trong menu thả xuống
            for sub_item in item["sub_items"]:
                # Tìm và click vào mục con
                sub_menu = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, sub_item))
                )
                sub_menu.click()

                # Xác nhận đã vào trang chính xác
                assert sub_item.split()[0] in self.driver.title, f"Không vào được trang {sub_item}"
                print(f"Đã vào trang {sub_item} thành công")

                time.sleep(1)

                # Quay lại trang chủ để tiếp tục với mục menu khác
                self.driver.back()
                menu = self.wait.until(
                    EC.presence_of_element_located((By.LINK_TEXT, item["name"]))
                )
                ActionChains(self.driver).move_to_element(menu).perform()

    def test_simple_menu_items(self):
        # Danh sách các mục không có menu con cần kiểm thử
        simple_menu_items = [
            {"name": "Tablets", "expected_title": "Tablets"},
            {"name": "Software", "expected_title": "Software"},
            {"name": "Phones & PDAs", "expected_title": "Phones & PDAs"},
            {"name": "Cameras", "expected_title": "Cameras"}
        ]

        for item in simple_menu_items:
            # Tìm và nhấp vào mục menu
            menu_item = self.wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, item["name"]))
            )
            menu_item.click()

            # Xác nhận tiêu đề hoặc URL của trang là chính xác
            assert item["expected_title"] in self.driver.title, f"Không vào được trang {item['name']}"
            print(f"Đã vào trang {item['name']} thành công")

            # Quay lại trang chủ để tiếp tục kiểm tra mục tiếp theo
            self.driver.back()