from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def search_products(driver, search_query):  # Hàm bổ trợ có chức năng tìm kiếm
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "search"))  # Tìm kiếm vị trí của Search
        )

        search_box.clear()  # Xóa các kí tự có sẵn trong đó
        search_box.send_keys(search_query + Keys.RETURN)  # Nhập vào các kí tự mới được thêm vào

        WebDriverWait(driver, 10).until(  # Tìm kiếm vị trí contnt
            EC.presence_of_element_located((By.ID, "content"))
        )

        products = driver.find_elements(By.XPATH,
                                        "//div[@id='content']//div[@class='product-thumb']")  # Tìm phần tử chứ content là sản phẩm

        product_details = []

        # check sản phẩm có được thểm vào giỏ hàng hay không
        if not products:
            print("No products found for the search query.")
            return product_details

        for product in products:  # Kiểm tra sản phẩm trong giỏ hàng
            product_name = product.find_element(By.XPATH, ".//h4/a").text
            product_price = product.find_element(By.XPATH, ".//span[@class='price-new']").text
            product_link = product.find_element(By.XPATH, ".//h4/a").get_attribute('href')

            product_details.append({
                "name": product_name,
                "price": product_price,
                "link": product_link
            })

            print(f"Product Name: {product_name}")
            print(f"Price: {product_price}")
            print(f"Link: {product_link}")
            print("=" * 40)

        return product_details

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
