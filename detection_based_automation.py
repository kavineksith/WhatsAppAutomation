import logging
import pywhatkit as kit
import pandas as pd
import os
from datetime import datetime
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

# Setup Logging
log_filename = "whatsapp_messaging.log"
logging.basicConfig(
    filename=log_filename, 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Base class to handle WhatsApp messaging
class WhatsAppMessenger:
    def __init__(self, contacts_file: str, images_folder: str = None, messages: list = None):
        """Initialize with contacts file, images folder, and messages."""
        logging.info(f"Initializing WhatsAppMessenger with contacts file: {contacts_file}")
        self._contacts_file = contacts_file
        self._images_folder = images_folder
        self._messages = messages or []
        self._contacts = self._load_contacts()  # Load contacts from CSV

    def _load_contacts(self):
        """Load contacts from CSV file and validate the phone numbers."""
        try:
            logging.info(f"Loading contacts from file: {self._contacts_file}")
            contacts_df = pd.read_csv(self._contacts_file)
            if 'phone' not in contacts_df.columns:
                raise FileNotFoundError("CSV file must have a 'phone' column.")
            
            contacts = contacts_df['phone'].tolist()
            self._validate_phone_numbers(contacts)
            logging.info(f"Loaded {len(contacts)} contacts successfully.")
            return contacts
        except FileNotFoundError as e:
            logging.error(f"Error loading contacts: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while loading contacts: {str(e)}")
            raise

    def _validate_phone_numbers(self, phone_numbers):
        """Ensure all phone numbers are valid."""
        logging.info("Validating phone numbers.")
        for phone in phone_numbers:
            if not phone.startswith('+') or len(phone) < 10:
                logging.error("Invalid phone number encountered.")
                raise InvalidPhoneNumberError("Invalid phone number.")
        logging.info("Phone numbers validated successfully.")

    def _send_message(self, phone_number, message):
        """Send message using pywhatkit."""
        try:
            logging.info(f"Preparing to send message to {phone_number}")
            if isinstance(message, str):
                kit.sendwhatmsg(phone_number, message, datetime.now().hour, datetime.now().minute + 2)
            elif isinstance(message, tuple) and len(message) == 2:  # Image and message
                image_path = message[0]
                text = message[1]
                kit.sendwhats_image(phone_number, image_path, text)
            else:
                raise MessageSendError("Invalid message format.")
            logging.info(f"Message sent to {phone_number}")
        except Exception as e:
            logging.error(f"Error sending message to {phone_number}: {str(e)}")
            raise MessageSendError(f"Failed to send message to {phone_number}")

    def _send_bulk_messages(self, message_collection):
        """Send bulk messages to all contacts."""
        logging.info(f"Sending bulk messages to {len(self._contacts)} contacts.")
        for contact in self._contacts:
            for message in message_collection:
                self._send_message(contact, message)
                sleep(2)  # Sleep for 2 seconds between each message to avoid rate limits
        logging.info("Bulk messages sent successfully.")

# Child class to handle text messages only
class TextMessageSender(WhatsAppMessenger):
    def __init__(self, contacts_file: str, messages: list):
        """Initialize with contacts file and list of text messages."""
        logging.info("Initializing TextMessageSender.")
        super().__init__(contacts_file, images_folder=None, messages=messages)
    
    def send_text_messages(self):
        """Send only text messages to contacts."""
        logging.info("Sending text messages.")
        self._send_bulk_messages(self._messages)

# Child class to handle image and text messages
class ImageMessageSender(WhatsAppMessenger):
    def __init__(self, contacts_file: str, images_folder: str, messages: list):
        """Initialize with contacts file, images folder, and list of messages."""
        logging.info("Initializing ImageMessageSender.")
        super().__init__(contacts_file, images_folder=images_folder, messages=messages)
    
    def _load_images(self):
        """Load all image files from the images folder."""
        try:
            logging.info(f"Loading images from folder: {self._images_folder}")
            if not os.path.exists(self._images_folder):
                raise FileNotFoundError(f"Images folder '{self._images_folder}' not found.")
            images = []
            for filename in os.listdir(self._images_folder):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    images.append(os.path.join(self._images_folder, filename))
            if not images:
                raise FileNotFoundError("No valid images found in the images folder.")
            logging.info(f"Loaded {len(images)} images.")
            return images
        except FileNotFoundError as e:
            logging.error(f"Error loading images: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while loading images: {str(e)}")
            raise

    def send_image_messages(self):
        """Send image messages with text to contacts."""
        logging.info("Sending image messages.")
        images = self._load_images()
        # Ensure messages and images are paired correctly, wrap around messages if there are fewer messages than images
        image_messages = [(image, self._messages[i % len(self._messages)]) for i, image in enumerate(images)]
        self._send_bulk_messages(image_messages)

# Main function to automate sending messages
def main():
    contacts_file = 'contacts.csv'  # The CSV file containing contact numbers
    images_folder = 'images'  # The folder containing images for sending
    messages = [
        "Hello, this is an automated message!", 
        "Here's an update about our product!", 
        "Thank you for being a loyal customer!"
    ]  # Text messages

    try:
        # Send text messages to all contacts
        logging.info("Starting text message sending process.")
        text_sender = TextMessageSender(contacts_file, messages)
        text_sender.send_text_messages()

        # Send image messages to all contacts
        logging.info("Starting image message sending process.")
        image_sender = ImageMessageSender(contacts_file, images_folder, messages)
        image_sender.send_image_messages()

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
