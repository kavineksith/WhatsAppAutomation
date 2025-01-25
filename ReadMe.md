# WhatsApp Automation Environment Setup

This script automates the setup process of a Python environment for WhatsApp messaging automation on your Windows system. It installs Python, sets up a virtual environment, installs required dependencies, and prepares the necessary project files.

## Prerequisites

- **Windows OS**: The script is designed to run on Windows. Ensure you have PowerShell available to execute the script.
- **Internet Connection**: The script downloads Python and required packages from the internet.
- **Python Version 3.10 or 3.11**: The script supports Python versions 3.10 and 3.11.

## Features

- Downloads and installs Python (version 3.10 or 3.11).
- Creates a Python virtual environment.
- Installs required Python packages (`pywhatkit`, `pandas`, `selenium`, `webdriver-manager`).
- Sets up essential files and directories for the project (e.g., `contacts.csv`, `images` folder).
- Copies specified Python files to the project folder.

## Installation Steps

### Step 1: Download the PowerShell Script

1. Download the provided PowerShell script file (`setup.ps1`) to your computer.

### Step 2: Prepare the Project Files

1. Ensure you have the following Python files in the same folder as the PowerShell script:
   - `detection_based_automation.py`
   - `web_based_automation.py`

### Step 3: Open PowerShell

1. Open **PowerShell** as an Administrator (right-click on the Start menu and select "Windows PowerShell (Admin)").

### Step 4: Run the Script

1. Navigate to the directory where the PowerShell script and Python files are located. For example:

   ```powershell
   cd "C:\Path\To\Your\Project\Folder"
   ```

2. Run the script:

   ```powershell
   .\setup.ps1
   ```

   The script will perform the following tasks:

   - **Check for Python**: If Python is not installed, it will automatically download and install Python 3.10 or 3.11 (you can configure the version in the script).
   - **Create Virtual Environment**: It will create a virtual environment in the `C:\WhatsAppMessaging` folder (can be changed in the script).
   - **Install Required Packages**: Installs the required Python packages (`pywhatkit`, `pandas`, `selenium`, `webdriver-manager`).
   - **Set Up Project Files**: Creates necessary files like `contacts.csv` and an `images` folder in the project directory.
   - **Copy Python Files**: It will copy the `detection_based_automation.py` and `web_based_automation.py` files into the project folder.

### Step 5: Verify the Setup

Once the script completes, you should have:

- **Python** installed (either version 3.10 or 3.11).
- A Python **virtual environment** named `whatsappenv` located in the `C:\WhatsAppMessaging` folder.
- Required Python packages installed and updated.
- Project files set up, including a `contacts.csv` file with a `phone` column and an `images` folder.

You can now start working on your WhatsApp automation project.

## Customization

- **Python Version**: You can choose either Python version 3.10 or 3.11 by modifying the `$pythonVersion` variable in the script.
- **Project Folder**: If you want to store the project files in a different folder, change the `$projectFolder` variable in the `PythonSetup` class.
- **Python Files**: Ensure the correct paths to your Python files are specified in the script (e.g., `detection_based_automation.py`, `web_based_automation.py`).

## Troubleshooting

- **Error: "Python installation failed"**:
  - Ensure that you have administrative privileges to install software on your computer.
  - If the issue persists, manually download and install Python from [Python.org](https://www.python.org/).
  
- **Error: "Virtual environment creation failed"**:
  - Ensure that your system has sufficient permissions to create folders and virtual environments.
  
- **Error: "Package installation failed"**:
  - Verify that your internet connection is stable.
  - Manually activate the virtual environment and install missing packages with the following command:
  
    ```powershell
    .\whatsappenv\Scripts\Activate.ps1
    pip install <package_name>
    ```

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### **Disclaimer:**
Kindly note that this project is developed solely for educational purposes, not intended for industrial use, as its sole intention lies within the realm of education. We emphatically underscore that this endeavor is not sanctioned for industrial application. It is imperative to bear in mind that any utilization of this project for commercial endeavors falls outside the intended scope and responsibility of its creators. Thus, we explicitly disclaim any liability or accountability for such usage.