# WhatsApp Messaging Script Documentation

This script automates the process of sending both text and image messages to a list of contacts via WhatsApp using the `pywhatkit` library. It supports both text-only and image-with-text messaging modes. The script is designed to load contact information and messages, and then send those messages in bulk. Error handling and logging are implemented to ensure smooth execution and troubleshooting.

## Features

- Load contacts from a CSV file.
- Validate phone numbers before sending messages.
- Send bulk text messages to contacts.
- Send bulk image messages with accompanying text to contacts.
- Logging to track successful operations and errors.
- Custom exceptions to handle specific error scenarios.

---

## Classes

### 1. **Custom Exceptions**

- `InvalidPhoneNumberError`: Raised when an invalid phone number is detected.
- `FileNotFoundError`: Raised when a file (CSV for contacts or images folder) is not found.
- `MessageSendError`: Raised when a message fails to send.

### 2. **WhatsAppMessenger**

This is the base class for handling WhatsApp messaging functionalities.

#### Methods:

- **`__init__(self, contacts_file: str, images_folder: str = None, messages: list = None)`**  
  Initializes the messenger with the provided contacts file, an optional image folder, and a list of messages.
  
- **`_load_contacts(self)`**  
  Loads contacts from a CSV file, validates phone numbers, and returns a list of valid phone numbers.

- **`_validate_phone_numbers(self, phone_numbers)`**  
  Validates the phone numbers to ensure they start with a "+" and are of a valid length.

- **`_send_message(self, phone_number, message)`**  
  Sends a message to a given phone number. It supports both text messages and image-with-text messages.

- **`_send_bulk_messages(self, message_collection)`**  
  Sends a list of messages to all contacts. Ensures a 2-second delay between each message to avoid rate limits.

### 3. **TextMessageSender** (Child Class of `WhatsAppMessenger`)

This class is designed to send text messages only.

#### Methods:

- **`__init__(self, contacts_file: str, messages: list)`**  
  Initializes the text message sender with a contacts file and a list of text messages.

- **`send_text_messages(self)`**  
  Sends all the text messages to the contacts.

### 4. **ImageMessageSender** (Child Class of `WhatsAppMessenger`)

This class is designed to send messages that include both images and text.

#### Methods:

- **`__init__(self, contacts_file: str, images_folder: str, messages: list)`**  
  Initializes the image message sender with a contacts file, an images folder, and a list of messages.

- **`_load_images(self)`**  
  Loads all image files (JPEG or PNG) from the provided folder.

- **`send_image_messages(self)`**  
  Sends image messages (with accompanying text) to all contacts. If there are more images than messages, it loops through the messages to pair them with images.

---

## Functions

### `main()`

This is the main function that drives the automation of sending messages. It first sends text messages and then sends image messages to all contacts.

#### Process:

1. Loads the contact list from a CSV file.
2. Loads images from a specified folder.
3. Sends text messages to all contacts using the `TextMessageSender` class.
4. Sends image messages to all contacts using the `ImageMessageSender` class.

The function uses the `logging` library to log the status of message sending and handles exceptions if any errors occur.

---

## Logging

Logging is set up to track the status of the script's execution:

- Logs are stored in a file named `whatsapp_messaging.log`.
- The logging level is set to `DEBUG`, so detailed logs are recorded.
- Additionally, logs are displayed in the console at the `INFO` level for real-time updates.

---

## Example Usage

To use this script, follow these steps:

1. Prepare a CSV file (`contacts.csv`) containing a column named `phone` with phone numbers of contacts (must include the international dialing code, e.g., `+1234567890`).
2. Prepare a folder (`images`) containing images you want to send (optional if only sending text).
3. Modify the `messages` list in the script with the text messages you want to send.
4. Run the script.

The script will:

- Send the text messages to all contacts.
- Send image messages (if images and corresponding messages are provided).

---

## Error Handling

The script includes custom error handling for the following situations:

- **Invalid Phone Numbers**: If any phone number in the contacts list is invalid (does not start with '+' or is too short), an `InvalidPhoneNumberError` will be raised.
- **File Not Found**: If the contacts CSV file or the images folder cannot be found, a `FileNotFoundError` will be raised.
- **Message Sending Failure**: If there is an issue with sending a message (e.g., an unsupported message format), a `MessageSendError` will be raised.

---

## Dependencies

- `pywhatkit`: Used for sending WhatsApp messages and images.
- `pandas`: Used to handle loading and processing the contacts CSV file.
- `os`: Used for interacting with the filesystem (e.g., to load image files).
- `datetime`: Used to get the current time to schedule the messages.
- `time`: Used to add delays between message sends.

---

## Notes

- The script sends messages with a delay of 2 seconds between each to avoid hitting rate limits on WhatsApp.
- Make sure that the script is run in an environment where WhatsApp Web is logged in and active for the automation to work.
- Ensure that the contact phone numbers include the country code (e.g., `+1` for the USA, `+44` for the UK).

---

## Conclusion

This script is a useful tool for automating WhatsApp messaging tasks, especially when you need to send bulk text or image messages to a list of contacts. With custom error handling and logging, it ensures a smooth user experience and helps in troubleshooting if any issues arise during the process.