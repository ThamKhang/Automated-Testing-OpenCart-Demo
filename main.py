# main.py
import uuid

from Custom.custom_user_agent import get_driver_with_custom_profile
from Module.add_to_wishlist import add_all_to_wishlist, add_single_product_to_wishlist
from Module.login import login_to_opencart
from Module.logout import logout_from_opencart
from Module.register import register_to_opencart
from config import profile_path


# Main function to execute the login and then send an email
def main():
    # Define registration details
    first_name = 'Tran'
    last_name = 'Khang'
    email = f"{uuid.uuid4().hex}@gmail.com"  # Generates a unique email
    email_address = "thamkhang2003@gmail.com"
    password = "PUEb5@7Lard"

    # Login
    # login_driver = login_to_opencart(email_address, password)
    # Register
    driver = register_to_opencart(first_name, last_name, email, password)
    # logout_from_opencart(driver)
    # login_driver = login_to_opencart(email_address, password)
    # add_all_to_wishlist()



if __name__ == "__main__":
    main()
