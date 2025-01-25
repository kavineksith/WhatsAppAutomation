import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import os
from time import sleep

# Custom Exceptions
class InvalidPhoneNumberError(Exception):
    """Raised when the phone number is invalid."""
    pass

class FileNotFoundError(Exception):
    """Raised when a file is not found."""
    pass

class MessageSendError(Exception):
    """Raised when a message fails to send."""
    pass

# Configure logging
logging.basicConfig(
    filename='whatsapp_messaging.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Base class to handle WhatsApp messaging using Selenium
class WhatsAppMessenger:
    def __init__(self, contacts_file: str, images_folder: str = None, messages: list = None, browser: str = 'chrome'):
        """Initialize with contacts file, images folder, and messages, and specify browser."""
        logging.info("Initializing WhatsAppMessenger class.")
        self._contacts_file = contacts_file
        self._images_folder = images_folder
        self._messages = messages or []
        self._contacts = self._load_contacts()  # Load contacts from CSV
        self.driver = self._init_driver(browser)

    def _init_driver(self, browser):
        """Initialize and return the Selenium WebDriver for the selected browser."""
        try:
            logging.info(f"Initializing WebDriver for {browser}.")
            if browser == 'chrome':
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--user-data-dir=chrome-data")  # Keeps the session persistent
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            elif browser == 'firefox':
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("-profile")
                firefox_options.add_argument("firefox-data")  # Keeps the session persistent
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
            else:
                logging.error(f"Unsupported browser: {browser}")
                raise ValueError("Unsupported browser. Please choose either 'chrome' or 'firefox'.")
            
            driver.get("https://web.whatsapp.com")
            logging.info("WhatsApp Web loaded.")
            input("Scan the QR code and then press Enter...")
            logging.info("QR code scanned, session started.")
            return driver
        except Exception as e:
            logging.error(f"Error initializing WebDriver: {e}")
            raise

    def _load_contacts(self):
        """Load contacts from CSV file and validate the phone numbers."""
        try:
            logging.info(f"Loading contacts from file: {self._contacts_file}")
            contacts_df = pd.read_csv(self._contacts_file)
            if 'phone' not in contacts_df.columns:
                logging.error("CSV file must have a 'phone' column.")
                raise FileNotFoundError("CSV file must have a 'phone' column.")
            
            contacts = contacts_df['phone'].tolist()
            self._validate_phone_numbers(contacts)
            logging.info(f"Loaded {len(contacts)} contacts from CSV.")
            return contacts
        except FileNotFoundError as e:
            logging.error(f"Error loading contacts: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while loading contacts: {str(e)}")
            raise

    def _validate_phone_numbers(self, phone_numbers):
        """Ensure all phone numbers are valid."""
        try:
            logging.info("Validating phone numbers.")
            for phone in phone_numbers:
                if not phone.startswith('+') or len(phone) < 10:
                    logging.error(f"Invalid phone number: {phone}")
                    raise InvalidPhoneNumberError(f"Invalid phone number: {phone}")
            logging.info("Phone numbers validated successfully.")
        except InvalidPhoneNumberError as e:
            logging.error(f"Validation failed: {e}")
            raise

    def _send_message(self, phone_number, message):
        """Send a text message using Selenium."""
        try:
            logging.info(f"Sending message to {phone_number}.")
            # Find the chat input box
            search_box = self.driver.find_element(By.XPATH, "//div[@title='Search or start new chat']")
            search_box.click()
            sleep(1)
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.RETURN)
            sleep(2)

            # Find the message input box
            message_box = self.driver.find_element(By.XPATH, "//div[@title='Type a message']")
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            logging.info(f"Message sent to {phone_number}")
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            raise MessageSendError(f"Failed to send message to {phone_number}")

    def _send_bulk_messages(self, message_collection):
        """Send bulk messages to all contacts."""
        try:
            logging.info("Sending bulk messages to contacts.")
            for contact in self._contacts:
                for message in message_collection:
                    self._send_message(contact, message)
                    sleep(2)  # Sleep for 2 seconds between each message to avoid rate limits
            logging.info("Bulk messages sent successfully.")
        except Exception as e:
            logging.error(f"Error during bulk messaging: {str(e)}")
            raise

# Child class to handle text messages only
class TextMessageSender(WhatsAppMessenger):
    def __init__(self, contacts_file: str, messages: list, browser: str = 'chrome'):
        """Initialize with contacts file and list of text messages."""
        logging.info("Initializing TextMessageSender.")
        super().__init__(contacts_file, images_folder=None, messages=messages, browser=browser)
    
    def send_text_messages(self):
        """Send only text messages to all contacts."""
        try:
            logging.info("Sending text messages to all contacts.")
            self._send_bulk_messages(self._messages)
        except Exception as e:
            logging.error(f"Error while sending text messages: {str(e)}")
            raise

# Child class to handle image and text messages
class ImageMessageSender(WhatsAppMessenger):
    def __init__(self, contacts_file: str, images_folder: str, messages: list, browser: str = 'chrome'):
        """Initialize with contacts file, images folder, and list of messages."""
        logging.info("Initializing ImageMessageSender.")
        super().__init__(contacts_file, images_folder=images_folder, messages=messages, browser=browser)
    
    def _load_images(self):
        """Load all image files from the images folder."""
        try:
            logging.info(f"Loading images from folder: {self._images_folder}")
            if not os.path.exists(self._images_folder):
                logging.error(f"Images folder '{self._images_folder}' not found.")
                raise FileNotFoundError(f"Images folder '{self._images_folder}' not found.")
            images = []
            for filename in os.listdir(self._images_folder):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    images.append(os.path.join(self._images_folder, filename))
            if not images:
                logging.error("No valid images found in the images folder.")
                raise FileNotFoundError("No valid images found in the images folder.")
            logging.info(f"Loaded {len(images)} images from the folder.")
            return images
        except FileNotFoundError as e:
            logging.error(f"Error loading images: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while loading images: {str(e)}")
            raise

    def send_image_messages(self):
        """Send image messages with text to all contacts."""
        try:
            logging.info("Sending image messages to all contacts.")
            images = self._load_images()
            image_messages = [(image, self._messages[i % len(self._messages)]) for i, image in enumerate(images)]
            for image_path, message in image_messages:
                self._send_message_with_image(image_path, message)
            logging.info("Image messages sent successfully.")
        except Exception as e:
            logging.error(f"Error while sending image messages: {str(e)}")
            raise

    def _send_message_with_image(self, image_path, message):
        """Send an image message with text."""
        try:
            logging.info(f"Sending image message with {image_path} to contacts.")
            # Find the chat input box
            search_box = self.driver.find_element(By.XPATH, "//div[@title='Search or start new chat']")
            search_box.click()
            sleep(1)

            for contact in self._contacts:
                search_box.send_keys(contact)  # Search for each contact
                search_box.send_keys(Keys.RETURN)
                sleep(2)

                # Upload image
                attachment_box = self.driver.find_element(By.XPATH, "//div[@title='Attach']")
                attachment_box.click()
                sleep(1)

                image_box = self.driver.find_element(By.XPATH, "//input[@type='file']")
                image_box.send_keys(image_path)
                sleep(2)

                # Send text message
                message_box = self.driver.find_element(By.XPATH, "//div[@title='Type a message']")
                message_box.send_keys(message)
                message_box.send_keys(Keys.RETURN)

            logging.info(f"Image and message sent to all contacts with image {image_path}.")
        except Exception as e:
            logging.error(f"Error sending image message: {str(e)}")
            raise MessageSendError(f"Failed to send image message: {image_path}")

# Main function to automate sending messages
def main():
    contacts_file = 'contacts.csv'  # The CSV file containing contact numbers
    images_folder = 'images'  # The folder containing images for sending
    messages = [
        "Hello, this is an automated message!", 
        "Here's an update about our product!", 
        "Thank you for being a loyal customer!"
    ]  # Text messages

    browser_choice = input("Which browser would you like to use? (chrome/firefox): ").strip().lower()
    
    try:
        # Send text messages to all contacts
        logging.info("Starting text message sending process.")
        text_sender = TextMessageSender(contacts_file, messages, browser=browser_choice)
        text_sender.send_text_messages()

        # Send image messages to all contacts
        logging.info("Starting image message sending process.")
        image_sender = ImageMessageSender(contacts_file, images_folder, messages, browser=browser_choice)
        image_sender.send_image_messages()

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
