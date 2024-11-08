# Dự án Kiểm thử Tự động OpenCart

Dự án này chứa các bài kiểm thử tự động cho website OpenCart, sử dụng Selenium WebDriver với Python.

## Cấu trúc thư mục

| Thư mục/Tệp                | Mô tả                                   |
|----------------------------|-----------------------------------------|
| `Custom/`                  | Chứa các tệp tùy chỉnh                   |
| └ `custom_user_agent.py`   | Thiết lập user agent tùy chỉnh cho ChromeDriver |
| `Module/`                  | Chứa các module chức năng               |
| ├ `cart_utiustom.py`       | Các hàm xử lý giỏ hàng, thanh toán                  |
| ├ `login.py`               | Đăng nhập vào OpenCart Demo                  |
| ├ `register.py`            | Đăng ký tài khoản                       |
| └ `search.py`              | Tìm kiếm sản phẩm                       |
| `test/`                    | Chứa các bài kiểm thử                   |
| ├ `test_cart_checkout.py`  | Kiểm thử giỏ hàng và thanh toán          |
| ├ `test_login.py`          | Kiểm thử đăng nhập                       |
| ├ `test_navigation.py`     | Kiểm thử điều hướng                      |
| ├ `test_register.py`       | Kiểm thử đăng ký                         |
| ├ `test_responsive_design.py` | Kiểm thử giao diện responsive            |
| └ `test_search_functionality.py` | Kiểm thử chức năng tìm kiếm           |
| `chrome_profile.py`        | Quản lý profile Chrome                  |
| `main.py`                  | Tệp quản lý chức năng của dự án                     |
| `requirements.txt`         | Liệt kê các thư viện cần thiết          |

## Giải thích Code

### Tệp Chính

- **main.py**: Chạy các chức năng từ Module

### Tùy Chỉnh

- **chrome_profile.py**:
    - `create_chrome_profile()`: Hàm tạo thư mục profile Chrome. Cần chạy hàm này trước tiên để lưu dữ liệu duyệt web, tránh trường hợp Chrome driver không load đủ giao diện.
  
- **/Custom/custom_user_agent.py**:
    - `get_driver_with_custom_profile()`: Thiết lập Custom User Agent cho ChromeDriver để hạn chế việc bị check là robot, ảnh hưởng đến quá trình kiểm thử.

### Modules

- **/Module/cart_utiustom.py**: Chứa các hàm xử lý giỏ hàng:
    - `clear_cart()`: Xóa giỏ hàng.
    - `add_to_cart()`: Thêm sản phẩm vào giỏ hàng.
    - `add_to_cart_multiple_clicks()`: Thêm sản phẩm vào giỏ hàng nhiều lần.
  
- **/Module/login.py**:
    - `login_to_opencart()`: Thực hiện đăng nhập. Kiểm tra đã đăng xuất chưa, nếu chưa thì đăng xuất rồi đăng nhập; nếu rồi thì đăng nhập ngay.
  
- **/Module/register.py**:
    - Đăng ký tài khoản. Kiểm tra đã đăng xuất chưa, nếu chưa thì đăng xuất rồi đăng ký; nếu rồi thì đăng ký ngay.

- **/Module/search.py**:
    - `search_products()`: Thực hiện chức năng tìm kiếm sản phẩm.

### Tests

- **/test/test_cart_checkout.py**: 
    - `class TestOpenCart`: Kiểm thử chức năng giỏ hàng và thanh toán.
        - `test_add_to_cart()`: Kiểm tra thêm sản phẩm vào giỏ hàng bình thường.
        - `test_many_add_product()`: Kiểm tra thêm nhiều sản phẩm vào giỏ hàng.
        - `test_add_multiple_products()`: Kiểm tra thêm một sản phẩm vào giỏ hàng nhiều lần.
        - `test_to_cart_with_options()`: Kiểm tra thêm sản phẩm có tùy chọn vào giỏ hàng.
        - `test_checkout_with_guest_account()`: Kiểm tra thanh toán với tài khoản khách.
  
- **/test/test_login.py**: 
    - `class TestLogin`: Kiểm thử chức năng đăng nhập.
        - `test_login_success()`: Đăng nhập thành công với thông tin hợp lệ.
        - `test_login_failure()`: Đăng nhập thất bại với thông tin không hợp lệ.
        - `test_login_with_blank_fields()`: Đăng nhập với email và mật khẩu trống.
        - `test_login_with_valid_email_and_invalid_password()`: Đăng nhập với email hợp lệ và mật khẩu không hợp lệ.
        - `test_login_with_invalid_email_and_valid_password()`: Đăng nhập với email không hợp lệ và mật khẩu hợp lệ.
        - `test_login_with_invalid_email_format()`: Đăng nhập với định dạng email không hợp lệ.
  
- **/test/test_navigation.py**: 
    - `class TestNavigation`: Kiểm thử điều hướng website.
        - `test_click_desktops_and_mac()`: Kiểm tra điều hướng đến danh mục "Desktops" và chọn "Mac".
        - `test_show_all_desktops()`: Kiểm tra điều hướng đến danh mục "Desktops" và chọn "Show All Desktops".
        - `test_menu_navigation()`: Kiểm tra điều hướng qua các mục menu có menu con.
        - `test_simple_menu_items()`: Kiểm tra điều hướng qua các mục menu không có menu con.
  
- **/test/test_register.py**: 
    - `class TestRegister`: Kiểm thử chức năng đăng ký.
        - `test_invalid_firstname()`: Đăng ký với tên không hợp lệ.
        - `test_invalid_lastname()`: Đăng ký với họ không hợp lệ.
        - `test_invalid_email()`: Đăng ký với email không hợp lệ.
        - `test_email_already_registered()`: Đăng ký với email đã tồn tại.
        - `test_weak_password()`: Đăng ký với mật khẩu yếu.
        - `test_successful_registration()`: Đăng ký thành công.
  
- **/test/test_responsive_design.py**: Kiểm thử giao diện responsive trên các thiết bị khác nhau (desktop, laptop, tablet, mobile).
    - `test_responsive_design(driver, device, size)`: Kiểm tra hiển thị của hộp tìm kiếm, dropdown 'My Account', nội dung chính, giỏ hàng, ... trên các kích thước màn hình khác nhau.
  
- **/test/test_search_functionality.py**:
    - `class TestSearchFunctionality`: Kiểm thử chức năng tìm kiếm.
        - `test_correct_search_products()`: Tìm kiếm với từ khóa hợp lệ.
        - `test_search_with_no_exist_products()`: Tìm kiếm với từ khóa không tồn tại.
        - `test_search_with_uppercase_all_text()`: Tìm kiếm với từ khóa viết hoa.
        - `test_search_with_lowercase_all_text()`: Tìm kiếm với từ khóa viết thường.
        - `test_search_special_characters()`: Tìm kiếm với ký tự đặc biệt.
        - `test_search_with_whitespace_surrounded()`: Tìm kiếm với từ khóa có khoảng trắng thừa.
        - `test_search_empty_characters()`: Tìm kiếm với chuỗi rỗng.
        - `test_search_with_special_character_in_text()`: Tìm kiếm với ký tự đặc biệt trong tên sản phẩm.
        - `test_search_with_long_character_in_text()`: Tìm kiếm với từ khóa dài bất thường.

## Yêu cầu

### Phần mềm:

- **Python**: Phiên bản 3.7 hoặc cao hơn.
- **Trình duyệt**: Google Chrome.
- **Chrome WebDriver**: Tự động tải với Selenium (không cần cài đặt ChromeDriver thủ công).

### Thư viện Python:

- **Selenium**: Tự động hóa trình duyệt (Selenium 4 tự động tải WebDriver).
- **Pytest**: Chạy và quản lý các trường hợp kiểm thử.
- **pytest-html**: Tạo báo cáo kiểm thử HTML.

## Hướng dẫn Thiết lập

### Cài đặt Python:

1. Tải xuống và cài đặt Python, đảm bảo chọn tùy chọn "Thêm Python vào PATH".
2. Xác nhận cài đặt bằng cách chạy `python --version`.

### Cài đặt Các Gói Python Cần Thiết:

1. Mở terminal trong VS Code: `Terminal > New Terminal`.
2. Tạo môi trường ảo: `python -m venv venv`.
3. Kích hoạt môi trường ảo:
    - **Windows**: `venv\Scripts\activate`.
    - **macOS/Linux**: `source venv/bin/activate`.
4. Cài đặt các thư viện: `pip install selenium pytest pytest-html`.

### Cấu hình Môi trường Kiểm thử:

- Kết nối internet ổn định.
- Trang web http://demo.opencart.com/ hoạt động ổn định.

## Chạy Các Bài Kiểm Thử

### Thực thi từ Dòng lệnh:

- Tạo profile Chrome (nếu sử dụng custom user agent): `python Custom/custom_user_agent.py`.
- Chạy tất cả bài kiểm thử: `pytest`.
- Chạy một tệp kiểm thử cụ thể: `pytest <tên_tệp_kiểm_thử>.py` (ví dụ: `pytest test/test_login.py`).
- Chạy một test cụ thể: `pytest -k <tên_test>` (ví dụ: `pytest -k test_login_success`).

### Tạo Báo cáo Kiểm thử HTML:

- `pytest --html=report.html`
