import os
import tempfile
import time
import unittest
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select

from Module.search import search_products
from Module.login import login_to_opencart
from test.test_login import VALID_EMAIL, VALID_PASSWORD
from Module.cart_utils import clear_cart, add_to_cart, add_to_cart_multiple_clicks


class TestOpenCart:
    @pytest.fixture(scope="class", autouse=True)
    def driver(self):
        """Thiết lập driver cho tất cả các bài kiểm thử"""
        driver = login_to_opencart(VALID_EMAIL, VALID_PASSWORD)
        driver.get("https://demo.opencart.com/")
        yield driver
        driver.quit()

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def test_add_to_cart(self):
        add_to_cart(self.driver, "HTC")

    def test_many_add_product(self):
        # Clear the cart before adding new products
        clear_cart(self.driver)

        # Product to add and the desired click count
        product_name = "HTC Touch HD"
        click_count = 3  # Number of times to add the same product

        # Add the product multiple times
        add_to_cart_multiple_clicks(self.driver, product_name, click_count=click_count)
        time.sleep(4)  # Wait for the add to cart process

        # Navigate to the shopping cart page
        self.driver.get("https://demo.opencart.com/en-gb?route=checkout/cart")

        # Wait for the cart items to be visible
        cart_items = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#shopping-cart tbody tr"))
        )

        # Create dictionary to store quantities of each product
        product_quantities = {}

        for item in cart_items:
            product_name_in_cart = item.find_element(By.CSS_SELECTOR, ".text-start a").text
            quantity = int(item.find_element(By.NAME, "quantity").get_attribute("value"))
            product_quantities[product_name_in_cart] = quantity

        # Check the quantity of the added product
        assert product_name in product_quantities, f"{product_name} not found in the cart."
        assert product_quantities[product_name] == click_count, (
            f"Expected {click_count} of {product_name}, found {product_quantities[product_name]}."
        )

        print("All products were successfully added to the cart and verified.")

    def test_add_multiple_products(self):
        # Clear the cart before adding new products
        clear_cart(self.driver)

        # Dictionary of products to add with desired quantities
        products_to_add = {
            "HTC Touch HD": 1,
            "iPhone": 2,
            "MacBook": 1,
        }

        # Loop through each product and add it to the cart the specified number of times
        for product, quantity in products_to_add.items():
            for _ in range(quantity):
                add_to_cart(self.driver, product)
                time.sleep(3)  # Wait for the add to cart process to complete

        # Navigate to the shopping cart page
        self.driver.get("https://demo.opencart.com/en-gb?route=checkout/cart")

        # Wait for the cart items to be visible
        cart_items = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#shopping-cart tbody tr"))
        )

        # Dictionary to store the quantities of products in the cart
        product_quantities = {}

        for item in cart_items:
            # Get the name and quantity of each product in the cart
            product_name = item.find_element(By.CSS_SELECTOR, ".text-start a").text
            quantity = int(item.find_element(By.NAME, "quantity").get_attribute("value"))
            product_quantities[product_name] = quantity

        # Check if each product in products_to_add has the correct quantity in the cart
        for product, expected_quantity in products_to_add.items():
            assert product in product_quantities, f"{product} not found in the cart."
            assert product_quantities[product] == expected_quantity, \
                f"Expected {expected_quantity} of {product}, found {product_quantities[product]}."

        print("All specified products were successfully added to the cart with the correct quantities.")
    #
    def test_to_cart_with_options(self):
        # Điều hướng đến trang sản phẩm "Apple Cinema 30"
        self.driver.get("https://demo.opencart.com/index.php?route=product/product&product_id=42")

        # Chọn tùy chọn 'Radio' (Large)
        self.driver.find_element(By.ID, "input-option-value-7").click()

        # Chọn tùy chọn 'Checkbox' (Checkbox 3 và Checkbox 4)
        element = self.driver.find_element(By.ID, "input-option-value-10")
        self.driver.execute_script("arguments[0].click();", element)

        element = self.driver.find_element(By.ID, "input-option-value-11")
        self.driver.execute_script("arguments[0].click();", element)

        # Điền giá trị vào trường 'Text'
        self.driver.find_element(By.ID, "input-option-208").send_keys("Custom text for product")

        # Chọn tùy chọn 'Select' (Red)
        select_element = Select(self.driver.find_element(By.ID, "input-option-217"))
        select_element.select_by_value("4")

        # Điền giá trị vào trường 'Textarea'
        self.driver.find_element(By.ID, "input-option-209").send_keys("Textarea content for product")
        wait = WebDriverWait(self.driver, 10)

        # Giả lập mã tải lên tệp vào trường input-option-222 mà không tải tệp thật
        fake_file_code = "25d5eee12d3a1d92399e3d110ffea4f1"  # Mã giả
        upload_input = self.driver.find_element(By.ID, "input-option-222")
        self.driver.execute_script("arguments[0].value = arguments[1];", upload_input, fake_file_code)

        print("File code entered into hidden input successfully.")
        # Chọn giá trị cho 'Date'
        date_field = self.driver.find_element(By.ID, "input-option-219")
        date_field.clear()
        date_field.send_keys("2024-11-06")

        # Chọn giá trị cho 'Date & Time'
        datetime_field = self.driver.find_element(By.ID, "input-option-220")
        datetime_field.clear()
        datetime_field.send_keys("2024-11-06 10:30")

        # Chọn số lượng sản phẩm
        self.driver.find_element(By.ID, "input-quantity").clear()
        self.driver.find_element(By.ID, "input-quantity").send_keys("2")

        # Thêm sản phẩm vào giỏ hàng
        element = self.driver.find_element(By.ID, "button-cart")
        self.driver.execute_script("arguments[0].click();", element)

        # Chờ thông báo xác nhận xuất hiện
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "Success: You have added Apple Cinema 30\" to your shopping cart!" in success_message.text

        print("Product with options added to the cart successfully.")

    def test_checkout_with_guest_account(self):
        # Clear the cart before adding new products
        clear_cart(self.driver)
        # Dictionary of products to add with desired quantities
        products_to_add = {
            "HTC Touch HD": 1,
            "MacBook": 1,
        }

        # Loop through each product and add it to the cart the specified number of times
        for product, quantity in products_to_add.items():
            for _ in range(quantity):
                add_to_cart(self.driver, product)
                time.sleep(3)  # Wait for the add to cart process to complete

        # Navigate to the shopping cart page
        self.driver.get("https://demo.opencart.com/en-gb?route=checkout/cart")

        # Thêm sản phẩm vào giỏ hàng
        checkout_button = self.driver.find_element(By.LINK_TEXT, "Checkout")
        self.driver.execute_script("arguments[0].click();", checkout_button)

        time.sleep(3)
        input_guest = self.driver.find_element(By.ID, "input-shipping-new")
        self.driver.execute_script("arguments[0].click();", input_guest)
        time.sleep(3)

        # Nhập thông tin giao hàng
        first_name = "Trần"
        last_name = "Thẩm Khang"
        company = "Jung Talents"
        address1 = "67/12 Trần Xuân Soạn"
        address2 = "HCM"
        city = "Ho Chi Minh City"
        post_code = "191103"
        country = "Viet Nam"
        region = "Ho Chi Minh City"

        # Hàm điền thông tin vào ô nhập liệu
        def fill_input(input_id, value, driver):
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, input_id))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Cuộn trang tới phần tử
            driver.execute_script("arguments[0].focus();", element)  # Đảm bảo phần tử được lấy tiêu điểm
            element.clear()
            element.send_keys(value)

        # Điền thông tin cá nhân và địa chỉ giao hàng
        fill_input("input-shipping-firstname", first_name, self.driver)
        fill_input("input-shipping-lastname", last_name, self.driver)
        fill_input("input-shipping-company", company, self.driver)
        fill_input("input-shipping-address-1", address1, self.driver)
        fill_input("input-shipping-address-2", address2, self.driver)
        fill_input("input-shipping-city", city, self.driver)
        fill_input("input-shipping-postcode", post_code, self.driver)

        # Chọn quốc gia và vùng
        select_country = Select(WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#input-shipping-country"))
        ))
        select_country.select_by_visible_text(country)
        time.sleep(3)

        select_region = Select(WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "input-shipping-zone"))
        ))
        time.sleep(3)
        select_region.select_by_visible_text(region)
        time.sleep(3)

        # Bấm vào nút "Tiếp tục" để xác nhận thông tin
        continue_btn = self.driver.find_element(By.ID, "button-shipping-address")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
        continue_btn.click()
        time.sleep(3)

        # Lướt tới đầu trang
        shipping_method = self.driver.find_element(By.ID, "button-shipping-methods")
        time.sleep(4)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", shipping_method)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "button-shipping-methods")))
        shipping_method.click()
        time.sleep(2)


        method_flat = self.driver.find_element(By.ID, "input-shipping-method-flat-flat")
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", method_flat)
        method_flat.click()

        continue_1 = self.driver.find_element(By.ID, "button-shipping-method")
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_1)
        continue_1.click()

        # Chọn phương thức thanh toán và xác nhận đơn hàng
        payment_method = self.driver.find_element(By.ID, "button-payment-methods")
        time.sleep(4)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", payment_method)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "button-payment-methods")))
        time.sleep(2)
        payment_method.click()
        time.sleep(2)

        cash_method = self.driver.find_element(By.ID, "input-payment-method-cod-cod")
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", cash_method)
        cash_method.click()

        continue_2 = self.driver.find_element(By.ID, "button-payment-method")
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_2)
        continue_2.click()
        time.sleep(2)


        # Button "Confirm" để xác nhận thanh toán
        confirm_order = self.driver.find_element(By.ID, "button-confirm")
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_order)
        confirm_order.click()

        notification = self.driver.find_element(By.CSS_SELECTOR, "#content > h1")  # Chuyển qua trang mới và hiện thong báo
        notification_actual = notification.text

        notification_expected = "Your order has been placed!"

        assert notification_expected == notification_actual, "Đơn hàng không được đặt thành công"  # Check thông báo ở trang mới
