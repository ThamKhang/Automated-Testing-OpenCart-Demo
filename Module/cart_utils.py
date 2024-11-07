import io
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from Module.search import search_products

def clear_cart(driver):
    driver.get("https://demo.opencart.com/en-gb?route=checkout/cart")
    time.sleep(5)  # Wait for the cart page to load

    empty_cart_message = driver.find_element(By.CSS_SELECTOR, "#content p").text
    if "Your shopping cart is empty!" in empty_cart_message:
        print("The cart is already empty.")
        return

    while True:
        remove_buttons = driver.find_elements(By.CSS_SELECTOR, "button[formaction*='checkout/cart.remove']")
        if not remove_buttons:
            break

        for button in remove_buttons:
            try:
                button.click()
                time.sleep(2)
            except StaleElementReferenceException:
                break

    print("Cart cleared.")

def add_to_cart(driver, product_name):
    # Chuyển hướng đầu ra để ẩn thông báo
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    # Gọi search_products
    product_details = search_products(driver, product_name)

    # Khôi phục lại đầu ra sau khi gọi xong
    sys.stdout = old_stdout

    if not product_details:
        print("No products found.")
        return

    first_product = product_details[0]
    print(f"Adding to cart: {first_product['name']} at price {first_product['price']}")
    driver.get(first_product['link'])

    wait = WebDriverWait(driver, 10)
    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
    add_to_cart_button.click()

    success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
    assert product_name in success_message.text, f"Product name '{product_name}' not found in success message."

def add_to_cart_multiple_clicks(driver, product_name, click_count=3):
    # Chuyển hướng đầu ra để ẩn thông báo
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    # Gọi search_products
    product_details = search_products(driver, product_name)

    # Khôi phục lại đầu ra sau khi gọi xong
    sys.stdout = old_stdout

    if not product_details:
        print("No products found.")
        return

    first_product = product_details[0]
    print(f"Adding to cart: {first_product['name']} at price {first_product['price']}")
    driver.get(first_product['link'])

    wait = WebDriverWait(driver, 10)

    for _ in range(click_count):
        # Chờ nút "Add to Cart" sẵn sàng và nhấn
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
        add_to_cart_button.click()

        # Chờ thông báo thêm sản phẩm thành công xuất hiện
        success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        assert product_name in success_message.text, f"Product name '{product_name}' not found in success message."

        # Refresh trang để chuẩn bị cho lần nhấn tiếp theo
        driver.refresh()
