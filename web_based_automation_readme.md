# WhatsApp Messaging Automation with Selenium - Documentation

This script automates the process of sending both text and image messages to a list of contacts via WhatsApp Web using Selenium WebDriver. It supports both text-only and image-with-text messaging modes and allows users to choose between using Chrome or Firefox for the automation process. The script handles loading contacts, sending messages, and managing browser sessions.

## Features

- **Supports multiple browsers**: Chrome and Firefox (via Selenium).
- **Automates WhatsApp Web**: Send text and image messages via WhatsApp Web.
- **Load contacts from a CSV file**: Validates and loads contacts for messaging.
- **Supports bulk messaging**: Sends messages to all contacts.
- **Persistent browser sessions**: Keeps the session persistent using browser profiles.
- **Logging**: Tracks the success and failure of message sending, providing detailed logs.
- **Custom error handling**: Handles errors like invalid phone numbers, missing files, and message sending failures.

---

## Classes

### 1. **Custom Exceptions**

- `InvalidPhoneNumberError`: Raised when an invalid phone number is detected.
- `FileNotFoundError`: Raised when a file (CSV for contacts or images folder) is not found.
- `MessageSendError`: Raised when a message fails to send.

### 2. **WhatsAppMessenger**

This is the base class that handles all WhatsApp messaging functionalities using Selenium WebDriver.

#### Methods:

- **`__init__(self, contacts_file: str, images_folder: str = None, messages: list = None, browser: str = 'chrome')`**  
  Initializes the class with the provided contacts file, optional image folder, list of messages, and browser selection (either Chrome or Firefox).

- **`_init_driver(self, browser)`**  
  Initializes and returns the Selenium WebDriver for the selected browser (`chrome` or `firefox`).

- **`_load_contacts(self)`**  
  Loads contacts from a CSV file and validates phone numbers. The CSV file must contain a `phone` column.

- **`_validate_phone_numbers(self, phone_numbers)`**  
  Validates that all phone numbers are in the correct format (starting with "+" and a length of at least 10 characters).

- **`_send_message(self, phone_number, message)`**  
  Sends a text message to a given phone number using Selenium.

- **`_send_bulk_messages(self, message_collection)`**  
  Sends a collection of messages to all contacts.

### 3. **TextMessageSender** (Child Class of `WhatsAppMessenger`)

This class is designed to send text-only messages.

#### Methods:

- **`__init__(self, contacts_file: str, messages: list, browser: str = 'chrome')`**  
  Initializes the text message sender with a contacts file, a list of text messages, and a selected browser.

- **`send_text_messages(self)`**  
  Sends all the text messages to the contacts.

### 4. **ImageMessageSender** (Child Class of `WhatsAppMessenger`)

This class is designed to send image messages with accompanying text.

#### Methods:

- **`__init__(self, contacts_file: str, images_folder: str, messages: list, browser: str = 'chrome')`**  
  Initializes the image message sender with a contacts file, images folder, list of messages, and a selected browser.

- **`_load_images(self)`**  
  Loads all image files (JPEG or PNG) from the provided folder.

- **`send_image_messages(self)`**  
  Sends image messages with text to all contacts. The images are paired with the messages, and the messages are sent along with the images.

- **`_send_message_with_image(self, image_path, message)`**  
  Sends a message with an image to all contacts.

---

## Functions

### `main()`

The main function that automates sending messages using the `TextMessageSender` and `ImageMessageSender` classes.

#### Process:

1. Prompts the user to select a browser (Chrome or Firefox).
2. Loads the contact list from a CSV file (`contacts.csv`).
3. Loads images from the specified folder (`images`).
4. Sends text messages to all contacts using the `TextMessageSender` class.
5. Sends image messages with text to all contacts using the `ImageMessageSender` class.

The function handles exceptions and logs any errors during the message sending process.

---

## Logging

Logging is configured to capture detailed logs:

- Logs are saved to a file named `whatsapp_messaging.log`.
- The logging level is set to `DEBUG`, providing detailed logs.
- Console output at `INFO` level gives real-time updates during execution.

Logs include information about the initiation of processes, successful message sends, errors, and warnings.

---

## Error Handling

The script includes custom error handling for the following scenarios:

- **Invalid Phone Numbers**: If any phone number is invalid (does not start with '+' or is too short), the `InvalidPhoneNumberError` exception is raised.
- **File Not Found**: If the contacts CSV file or the images folder is missing or contains errors, the `FileNotFoundError` exception is raised.
- **Message Sending Failures**: If a message cannot be sent (due to an issue with Selenium or the WhatsApp Web interface), the `MessageSendError` exception is raised.

These errors are logged for easy identification and resolution.

---

## Dependencies

- **`selenium`**: Used for automating the WhatsApp Web interface.
- **`webdriver-manager`**: Automatically manages the WebDriver binaries for Chrome and Firefox.
- **`pandas`**: Used to load and manipulate the contacts CSV file.
- **`os`**: For interacting with the filesystem (e.g., to load image files).
- **`time`**: Used for adding delays between actions (e.g., to avoid rate limits).

---

## Example Usage

1. **Prepare the Contacts File**:  
   Ensure the `contacts.csv` file contains a `phone` column with valid international phone numbers (e.g., `+1234567890`).

2. **Prepare the Images Folder** (Optional for Image Messages):  
   Ensure the `images` folder contains valid image files (e.g., `.jpg`, `.png`) if you're sending image messages.

3. **Modify the Messages List**:  
   Edit the `messages` list in the script with the text you want to send to the contacts.

4. **Run the Script**:  
   When you run the script, it will prompt you to choose a browser (Chrome or Firefox). Once the browser is selected and the QR code is scanned, it will send the messages.

5. **Check Logs**:  
   The script will log its activities, so you can check `whatsapp_messaging.log` for detailed progress and errors.

---

## Notes

- **Browser Profiles**: The script keeps the browser session persistent by using a custom profile (`chrome-data` for Chrome and `firefox-data` for Firefox). This allows you to scan the QR code once and use the same session for subsequent runs.
  
- **Message Rate Limits**: The script sleeps for 2 seconds between each message to avoid rate limits imposed by WhatsApp Web.

- **QR Code Scan**: When using the script for the first time, you must scan the QR code manually. After scanning, press Enter to continue with the message sending process.

---

## Conclusion

This script is a useful automation tool for sending bulk text and image messages via WhatsApp Web using Selenium. It supports both Chrome and Firefox browsers, and includes robust error handling and logging to ensure smooth operation.