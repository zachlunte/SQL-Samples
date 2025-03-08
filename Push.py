#! /usr/bin/env python3

# Import dependencies
import sys, os, sqlite3, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Get the identifier from the first argument
identifier = int(sys.argv[1])

# Define the Lunte Books account credentials
email = "luntebooks@gmail.com"
password = "%%^fGh@2a13"

# Print status message
print("\nLoading item data...")

# Get the absolute path of the SQL database file
current_directory = os.path.dirname(__file__)
database_path = os.path.join(current_directory, '../../Database/Inventory.db')

# Create a connection to the SQL database
connection = sqlite3.connect(database_path)

# Create a cursor from the connection to the database
cursor = connection.cursor()

# Get author field from the database
query = "select author from books where id = {}".format(identifier)
cursor.execute(query)
author = cursor.fetchall()
author = str(author)[3:-4]

# Get title field from the database
query = "select title from books where id = {}".format(identifier)
cursor.execute(query)
title = cursor.fetchall()
title = str(title)[3:-4]

# Get year field from the database
query = "select year from books where id = {}".format(identifier)
cursor.execute(query)
year = cursor.fetchall()
year = str(year)[2:-3]

# Get type field from the database
query = "select type from books where id = {}".format(identifier)
cursor.execute(query)
type = cursor.fetchall()
type = str(type)[3:-4]

# Get publisher field from the database
query = "select publisher from books where id = {}".format(identifier)
cursor.execute(query)
publisher = cursor.fetchall()
publisher = str(publisher)[3:-4]

# Get edition field from the database
query = "select edition from books where id = {}".format(identifier)
cursor.execute(query)
edition = cursor.fetchall()
edition = str(edition)[3:-4]

# Get condition field from the database
query = "select condition from books where id = {}".format(identifier)
cursor.execute(query)
condition = cursor.fetchall()
condition = str(condition)[3:-4]

# Get description field from the database
query = "select description from books where id = {}".format(identifier)
cursor.execute(query)
description = cursor.fetchall()
description = str(description)[3:-4]

# Get price field from the database
query = "select price from books where id = {}".format(identifier)
cursor.execute(query)
price = cursor.fetchall()
price = str(price)[2:-3]

# TO DO: Get the absolute path names of the associated images

# Print status message
print("Item data successfully loaded!")

# Print status message
print("Attempting to sign into AbeBooks account...".format(identifier))

# Set signed in state
signed_in = False

# Define the homepage URL
homepage_url = "https://www.abebooks.com"

# Use Google Chrome with webdriver and make it headless
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
WINDOW_SIZE = "1920,1080"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument(f'user-agent={USER_AGENT}')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

# Navigate to the home page
driver.get(homepage_url)

# Tell driver to wait
driver.implicitly_wait(20)

# Find the sign on link
sign_on_link = driver.find_element_by_id("sign-on")

# Click on the first sign on link
sign_on_link.click()

# Tell driver to wait
driver.implicitly_wait(20)

# Find the email input field
sign_on_email = driver.find_element_by_id("ap_email")

# Click on the email input field
sign_on_email.click()

# Type the account email into the email input field
sign_on_email.send_keys(email)

# Tell driver to wait
driver.implicitly_wait(20)

# Find the password input field
sign_on_password = driver.find_element_by_id("ap_password")

# Click on the password input field
sign_on_password.click()

# Type the password into the password input field
sign_on_password.send_keys(password)

# Submit the sign on credentials by hitting the Enter key
sign_on_password.send_keys(Keys.ENTER)

# Tell driver to wait
driver.implicitly_wait(20)
time.sleep(3)
driver.get_screenshot_as_file("CAPTCHA_TEST.png")

# Print ask the user to look to see if there is a CAPTCHA
print("Please check to see if there is a CAPTCHA.")
time.sleep(1)
print("Opening screenshot now...")
time.sleep(1)
os.system("open CAPTCHA_TEST.png")
captcha = input("Is there a CAPTCHA? (y/n): ")

# If there is a CAPTCHA
if captcha == "y":

    # Print message to user
    print("You have confirmed the existence of a CAPTCHA.")
    
    # Request the user to enter the CAPTCHA value
    captcha_value = input("Please enter the CAPTCHA value to continue: ")

    # Print message to user
    print("Attempting to solve CAPTCHA now...")
    
    # Attempt to find the CAPTCHA text field
    captcha_field = driver.find_element_by_id("auth-captcha-guess")

    # Enter the captcha value into the captcha field
    captcha_field.send_keys(captcha_value) 

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Re-locate the password field
    password_field = driver.find_element_by_id("ap_password")

    # Enter the password into the password field
    password_field.send_keys(password)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Attempt to find the sign in button
    sign_on_link = driver.find_element_by_id("signInSubmit")

    # Click the sign on button
    sign_on_link.click()

    # Tell driver to wait
    driver.implicitly_wait(20)
    time.sleep(3)

    # Close the CAPTCHA screenshot in Preview
    os.system("killall Preview")

    # Remove the CAPTCHA screenshot
    os.system("rm CAPTCHA_TEST.png")

    # Try the following
    try:

        # Test to see if the manage books link is now visible
        manage_books_link = driver.find_element_by_xpath('//a[@href="/servlet/InventoryListEntry"]')

        # Set the signed in value to be true
        signed_in = True

    except:

        # If the manage books link is still not available, quit driver and exit program
        print("ERROR: Sign in with CAPTCHA failed!")

# Else if there is no CAPTCHA
elif captcha == "n":

    # Print message to user
    print("You have confirmed there is no CAPTCHA.")

    # Close the CAPTCHA screenshot in Preview
    os.system("killall Preview")

    # Remove the CAPTCHA screenshot
    os.system("rm CAPTCHA_TEST.png")

    # Set the signed in value to be true
    signed_in = True

# If sign in was successful
if signed_in:

    # Print status message
    print("Successfully signed into AbeBooks!")
    print("Attempting to fill listing details...")

    # Find the manage books link
    manage_books_link = driver.find_element_by_xpath('//a[@href="/servlet/InventoryListEntry"]')

    # Click on the manage books link
    manage_books_link.click()

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the add listing link
    add_listing_link = driver.find_element_by_xpath('//a[@href="/servlet/AddListing"]')

    # Click on the add listing link
    add_listing_link.click()

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the book number field
    book_number_field = driver.find_element_by_name("vli")

    # Click on the book number field
    book_number_field.click()

    # Type the identifier into the book number field
    book_number_field.send_keys(identifier)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the author field
    author_field = driver.find_element_by_name("p_author")

    # Click on the author field
    author_field.click()

    # Type the author into the author field
    author_field.send_keys(author)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the title field
    title_field = driver.find_element_by_name("p_title")

    # Click on the title field
    title_field.click()

    # Type the title into the title field
    title_field.send_keys(title)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the publisher field
    publisher_field = driver.find_element_by_name("p_publisherinfo")

    # Click on the publisher field
    publisher_field.click()

    # Type the publisher into the publisher field
    publisher_field.send_keys(publisher)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the published year field
    published_year_field = driver.find_element_by_name("p_publisheryear")

    # Click on the published year field
    published_year_field.click()

    # Type the year into the published year field
    published_year_field.send_keys(year)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the price field
    price_field = driver.find_element_by_name("p_price")

    # Click on the price field
    price_field.click()

    # Clear the price field before typing
    price_field.clear()

    # Type the price into the price field
    price_field.send_keys(price)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the keywords field
    keywords_field = driver.find_element_by_name("p_keywords")

    # Click on the keywords field
    keywords_field.click()

    # Type the keywords into the keywords field
    keywords_field.send_keys("{0}, {1}, {2}".format(author, title, "Lunte Books"))

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the description field
    description_field = driver.find_element_by_name("p_description")

    # Click on the description field
    description_field.click()

    # Type the description into the description field
    description_field.send_keys(description)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the product menu
    product_menu = Select(driver.find_element_by_name("p_bsacodeproduct"))

    # Select the book product in the menu
    product_menu.select_by_visible_text("Book")

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the binding type menu
    binding_menu = Select(driver.find_element_by_name("p_bsacodebinding"))

    # Select the appropriate option in the menu
    binding_menu.select_by_visible_text(type)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # Find the condition menu
    condition_menu = Select(driver.find_element_by_name("p_bsacodebookcondition"))

    # Select the appropriate condition in the menu
    condition_menu.select_by_visible_text(condition)

    # Tell driver to wait
    driver.implicitly_wait(20)

    # If the edition is specified
    if edition != "":

        # Find the edition menu
        edition_menu = Select(driver.find_element_by_name("p_bsacodeedition"))

        # Select the appropriate edition in the menu
        edition_menu.select_by_visible_text(edition)

        # Tell driver to wait
        driver.implicitly_wait(20)

    # Print status message
    print("Successfully filled listing details!")

    # Quit the webdriver
    driver.quit()

# Else if failed to sign in
else:

    # Print error message
    print("ERROR: Unable to sign in")

    # Quit the driver
    driver.quit()
