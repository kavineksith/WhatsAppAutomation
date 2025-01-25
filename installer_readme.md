# Python Environment Setup Script - Documentation

This script automates the process of setting up a Python environment for WhatsApp messaging automation using PowerShell. It handles the installation of Python, creation of a virtual environment, installation of necessary Python packages, and setup of project folders and files. The script supports Python versions 3.10 and 3.11, and can be customized for various project file paths and requirements.

---

## Features

- **Python Installation**: Automates downloading and installing Python (versions 3.10 or 3.11).
- **Virtual Environment Setup**: Creates a Python virtual environment for isolating project dependencies.
- **Package Installation**: Installs required Python packages like `pywhatkit`, `pandas`, `selenium`, and `webdriver-manager`.
- **File and Folder Setup**: Automatically sets up necessary project files (e.g., `contacts.csv`) and folders (e.g., images folder).
- **Script File Management**: Copies Python files to the project folder.
- **Customizable**: Can be adjusted to work with different Python versions and file paths.

---

## Classes

### 1. **PythonSetup**

This class handles the installation and setup of the Python environment, virtual environment creation, package installation, and project file management.

#### Properties:

- **`pythonVersion`**: The Python version to be installed (either "3.10" or "3.11").
- **`pythonInstallUrl`**: The download URL for the selected Python version.
- **`pythonInstallPath`**: The local path to save the Python installer.
- **`envName`**: The name of the Python virtual environment (default: "whatsappenv").
- **`projectFolder`**: The folder where the project files will be located (default: "C:\WhatsAppMessaging").
- **`pythonPackages`**: An array of required Python packages to be installed (default: `("pywhatkit", "pandas", "selenium", "webdriver-manager")`).

#### Methods:

- **`PythonSetup([string]$version)`**: Initializes the setup class with the selected Python version and corresponding installation URL.
- **`Check-PythonInstalled()`**: Checks if Python is already installed on the system.
- **`Install-Python()`**: Downloads and installs the specified Python version.
- **`Create-VirtualEnv()`**: Creates a virtual environment in the specified project folder.
- **`Install-Packages()`**: Installs the required Python packages into the virtual environment.
- **`Setup-Files()`**: Sets up the necessary project files (e.g., `contacts.csv`) and folders (e.g., `images`).
- **`Copy-PythonFiles([string]$sourceFile1, [string]$sourceFile2)`**: Copies Python files from source to the project folder.

---

### 2. **ScriptExecutor**

This class helps execute the setup process by calling methods from the `PythonSetup` class.

#### Properties:

- **`pythonSetup`**: An instance of the `PythonSetup` class to manage the setup process.
- **`sourceFile1`**: Path to the first Python file to be copied to the project folder.
- **`sourceFile2`**: Path to the second Python file to be copied to the project folder.

#### Methods:

- **`ScriptExecutor([string]$pythonVersion, [string]$file1, [string]$file2)`**: Initializes the executor with the specified Python version and source file paths.
- **`Run()`**: Runs the entire setup process, including Python installation, virtual environment creation, package installation, and file copying.

---

## Script Execution Flow

### 1. **Choose Python Version**:
   - The script prompts for Python version 3.10 or 3.11. It will download the appropriate installer and proceed with the installation.

### 2. **Check Python Installation**:
   - The script first checks if Python is already installed. If Python is found, it skips the installation process. Otherwise, it downloads and installs the selected version.

### 3. **Create Virtual Environment**:
   - After Python installation, the script creates a virtual environment inside the specified project folder (`C:\WhatsAppMessaging` by default) to isolate dependencies.

### 4. **Install Required Packages**:
   - The script installs the necessary Python packages, including `pywhatkit`, `pandas`, `selenium`, and `webdriver-manager`, into the virtual environment.

### 5. **Setup Project Files and Folders**:
   - It sets up essential files like `contacts.csv` and creates necessary directories such as `images`.

### 6. **Copy Python Files**:
   - The specified Python files (`detection_based_automation.py` and `web_based_automation.py`) are copied to the project folder.

### 7. **Completion**:
   - The setup process completes, and the environment is ready for use.

---

## Dependencies

- **PowerShell**: Required to run the script.
- **Python 3.10 or 3.11**: The script installs one of these Python versions.
- **Packages**: 
  - `pywhatkit`: For WhatsApp automation.
  - `pandas`: For data manipulation.
  - `selenium`: For web automation.
  - `webdriver-manager`: To automatically manage WebDriver binaries.

---

## Example Usage

1. **Prepare the Python Files**:
   - Ensure that the `detection_based_automation.py` and `web_based_automation.py` files are available in the same directory as the PowerShell script.

2. **Run the Script**:
   - Open a PowerShell window and execute the script. The script will check for Python installation, create a virtual environment, install required packages, and copy necessary Python files to the project folder.

3. **Check the Project Folder**:
   - After running the script, check the project folder (`C:\WhatsAppMessaging`) to verify that the necessary files and folders (such as `contacts.csv` and the `images` folder) have been created.

---

## Customization

- **Python Version**: You can change the Python version in the script by modifying the `$pythonVersion` variable. Choose either "3.10" or "3.11".
- **Source Files**: You can adjust the paths of the source Python files (`detection_based_automation.py` and `web_based_automation.py`) based on their location on your system.
- **Project Folder**: If you want to use a different project folder, change the `$projectFolder` variable in the `PythonSetup` class.

---

## Logging

The script uses `Write-Host` to log progress and errors to the PowerShell console. You can monitor the progress of each step in the setup process, including Python installation, package installation, and file setup.

---

## Conclusion

This PowerShell script streamlines the process of setting up a Python environment for WhatsApp messaging automation. It automates Python installation, environment setup, package installation, and project file management, making it easier to get started with automation projects.