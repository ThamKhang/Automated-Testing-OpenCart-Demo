from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService, Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions, Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver_with_custom_profile(profile_path):
    if 'firefox' in profile_path.lower():
        options = Options()
        options.add_argument(f"--user-data-dir={profile_path}")  # Setting user data dir for Firefox
        options.set_preference("general.useragent.override",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
        options = Options()
        options.add_argument(f"-profile")
        options.add_argument(profile_path)

        return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    elif 'chrome' in profile_path.lower():
        options = ChromeOptions()
        options.add_argument(f"user-data-dir={profile_path}")
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
        # Add typical options
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-web-security")
        options.add_argument("--ignore-certificate-errors")

        # Add custom headers for mimicking real user behavior
        options.add_argument("accept-language=en-US,en;q=0.9")
        options.add_argument("accept-encoding=gzip, deflate, br")
        options.add_argument("referer=https://www.google.com/")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    else:
        raise ValueError("Unsupported profile path! Please provide a valid Chrome or Firefox profile path.")