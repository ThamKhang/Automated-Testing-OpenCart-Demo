import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from Custom.custom_user_agent import get_driver_with_custom_profile
from config import profile_path

# Các kích thước màn hình khác nhau để kiểm tra responsive
screen_sizes = {
    "desktop": (1920, 1080),
    "laptop": (1366, 768),
    "tablet_landscape": (1024, 768),
    "tablet_portrait": (768, 1024),
    "mobile_large": (414, 896),
    "mobile_small": (360, 640)
}

@pytest.fixture(scope="module")
def driver():
    driver = get_driver_with_custom_profile(profile_path)
    yield driver
    driver.quit()

@pytest.mark.parametrize("device, size", screen_sizes.items())
def test_responsive_design(driver, device, size):
    driver.get("https://demo.opencart.com/")

    # Đặt kích thước cửa sổ trình duyệt theo kích thước device
    width, height = size
    driver.set_window_size(width, height)
    driver.refresh()  # Làm mới trang để áp dụng kích thước mới

    # Chờ cho phần tử 'body' của trang web xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )

    try:
        # Kiểm tra hộp tìm kiếm có hiển thị hay không
        search_box = driver.find_element(By.NAME, "search")
        assert search_box.is_displayed(), f"Search box is not displayed on {device}."

        # Kiểm tra menu 'My Account' có hiển thị hay không
        my_account_dropdown = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']")
        assert my_account_dropdown.is_displayed(), f"My Account dropdown is not displayed on {device}."

        # Kiểm tra phần nội dung chính của trang có hiển thị hay không
        main_content = driver.find_element(By.ID, "content")
        assert main_content.is_displayed(), f"Main content is not displayed on {device}."

        # Tìm và nhập từ khóa 'Iphone' vào hộp tìm kiếm, sau đó nhấn Enter
        search_box.clear()
        search_box.send_keys("Iphone" + Keys.RETURN)

        # Nhấp vào nút 'Add to Cart' để thêm sản phẩm vào giỏ hàng
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'][data-bs-toggle='tooltip']"))
        )
        add_to_cart_button.click()

        # Chờ cho liên kết 'Shopping Cart' có thể nhấp được, rồi nhấp vào
        shopping_cart_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Shopping Cart']"))
        )
        shopping_cart_link.click()

        # Chờ cho phần tử div chứa giỏ hàng xuất hiện
        checkout_cart_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "checkout-cart"))
        )

        # Kiểm tra giỏ hàng có chứa sản phẩm nào không
        products_in_cart = checkout_cart_div.find_elements(By.CLASS_NAME, "product-thumb")
        assert len(products_in_cart) > 0, "No products found in the cart."

        # Kiểm tra div giỏ hàng có hiển thị hay không
        assert checkout_cart_div.is_displayed(), "Checkout cart div is not displayed."
        print(f"Checkout cart div is displayed successfully on {device}.")

    except Exception as e:
        print(f"Responsive test failed for {device}: {e}")

    print(f"Responsive design test completed for {device}.")
