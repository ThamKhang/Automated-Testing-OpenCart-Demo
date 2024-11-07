import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def create_chrome_profile(profile_path):
    """
    Mở Chrome với đường dẫn profile để tạo và cấu hình profile mới.
    Người dùng có thể đăng nhập và thay đổi các cài đặt của Chrome trong cửa sổ này.
    """
    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument("start-maximized")  # Mở Chrome toàn màn hình

    # Khởi động Chrome để người dùng cấu hình profile
    print("Đang mở Chrome để tạo profile...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Đợi người dùng tùy chỉnh profile
    print("Cấu hình profile của bạn trong Chrome. Đóng trình duyệt khi hoàn tất.")
    driver.get("https://www.google.com")  # Mở trang Google để kiểm tra
    input("Nhấn Enter sau khi bạn đóng trình duyệt để hoàn tất.")

    driver.quit()
    print(f"Profile đã được tạo tại: {profile_path}")

def get_chrome_driver_with_profile(profile_path):
    """
    Hàm khởi tạo WebDriver với profile đã tạo.
    """
    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Lấy thư mục chứa file hiện tại
    profile_path = os.path.join(current_directory, "my_chrome_profile")  # Đường dẫn tới profile trong thư mục hiện tại

    # Kiểm tra nếu profile chưa tồn tại thì tạo profile mới
    if not os.path.exists(profile_path):
        create_chrome_profile(profile_path)
    else:
        print(f"Profile đã tồn tại tại: {profile_path}")

    # Khởi động WebDriver với profile vừa tạo
    driver = get_chrome_driver_with_profile(profile_path)
    driver.get("https://demo.opencart.com/")

    # Thực hiện các thao tác cần thiết trên trang (ví dụ: đăng nhập, kiểm tra, v.v.)
    time.sleep(120)  # Tạm dừng để xem trang
    driver.quit()