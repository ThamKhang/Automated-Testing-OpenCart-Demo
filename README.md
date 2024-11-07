
# Kiểm thử Tự động với Selenium và Pytest

Dự án này chứa các trường hợp kiểm thử tự động sử dụng **Selenium WebDriver** và **Pytest** để xác minh chức năng sắp xếp trên trang web [Open Cart](http://localhost/webopencart/index.php?route=common/home&language=en-gb).

## Mục lục
- [Yêu cầu](#yêu-cầu)
- [Hướng dẫn Thiết lập](#hướng-dẫn-thiết-lập)
- [Chạy Các Bài Kiểm Thử](#chạy-các-bài-kiểm-thử)
- [Ghi chú](#ghi-chú)

---

## Yêu cầu

### 1. Phần mềm
- **Python**: Phiên bản 3.7 hoặc cao hơn
- **Trình duyệt**: Microsoft Edge (hoặc có thể thay đổi cho Chrome, Firefox, v.v.)
- **Edge WebDriver**: Phải phù hợp với phiên bản trình duyệt Edge của bạn (có hướng dẫn bên dưới).

### 2. Thư viện Python
- **Selenium**: Để tự động hóa trình duyệt
- **Pytest**: Để chạy và quản lý các trường hợp kiểm thử

---

## Hướng dẫn Thiết lập

### 1. Cài đặt Python
1. [Tải xuống Python](https://www.python.org/downloads/) và tiến hành cài đặt, đảm bảo chọn tùy chọn "Thêm Python vào PATH" trong quá trình cài đặt (Path environment).
2. Xác nhận việc cài đặt bằng cách chạy:
   ```bash
   python --version
   ```

### 2. Cài đặt Các Gói Python Cần Thiết
1. Mở terminal trong VS Code: Terminal > New Terminal
2. Tạo một môi trường ảo bằng lệnh:
   ```bash
   python -m venv venv
   ```
3. Kích hoạt môi trường ảo:
   ```bash
   venv\Scripts\activate
   ```
4. Sử dụng `pip` để cài đặt Selenium và Pytest:
   ```bash
   pip install selenium pytest
   ```

### 3. Thiết lập Edge WebDriver
Để tự động hóa các bài kiểm thử với Microsoft Edge:
1. Xác định phiên bản **Microsoft Edge** của bạn bằng cách truy cập `edge://settings/help`.
2. Tải xuống phiên bản **Edge WebDriver** phù hợp từ [trang WebDriver chính thức của Microsoft](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
3. Giải nén tệp thực thi WebDriver (ví dụ: `msedgedriver.exe`) và đặt nó vào một thư mục có trong **system PATH**, hoặc cập nhật fixture `driver` để trỏ đến đường dẫn chính xác của tệp driver.

Nếu bạn đang sử dụng **Chrome**:
- Thay thế `webdriver.Edge()` bằng `webdriver.Chrome()` trong mã, và tải xuống **ChromeDriver** thay thế.

### 4. Cấu hình Môi trường Kiểm thử
1. Đảm bảo rằng kết nối internet ổn định, vì các bài kiểm thử sẽ tương tác với trang web trực tuyến [Open Cart](http://localhost/webopencart/index.php?route=common/home&language=en-gb).
2. Xác nhận rằng thông tin đăng nhập được sử dụng (`nttn1234@gmail.com` và `1234`) có thể truy cập được trên trang thử nghiệm.

---

## Chạy Các Bài Kiểm Thử

### Thực thi từ Dòng lệnh
Để chạy tất cả các bài kiểm thử, hãy điều hướng đến thư mục dự án và chạy:
   ```bash
   pytest <tên_tệp_script_của_bạn>.py
   ```

### Tạo Báo cáo Kiểm thử HTML trong Python
Để tạo báo cáo HTML cho một bài kiểm thử Selenium, bạn cần cài đặt một plugin bằng lệnh: 
```bash
pip install pytest-html
```
Để tạo báo cáo, hãy di chuyển từ thư mục hiện tại đến thư mục chứa tệp Pytest mà bạn muốn thực thi. Sau đó, chạy lệnh: 
```bash
pytest --html=report.html
```

Sau khi lệnh này được thực thi thành công, một tệp mới có tên `report.html` sẽ được tạo trong thư mục dự án.
