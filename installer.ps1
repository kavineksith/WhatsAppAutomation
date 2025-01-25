# Define a class for the Python installation and environment setup process
class PythonSetup {
    [string]$pythonVersion
    [string]$pythonInstallUrl
    [string]$pythonInstallPath = "C:\Python\python-installer.exe"
    [string]$envName = "whatsappenv"
    [string]$projectFolder = "C:\WhatsAppMessaging"
    [array]$pythonPackages = @("pywhatkit", "pandas", "selenium", "webdriver-manager")
    
    # Constructor to initialize the Python version and set the installation URL
    PythonSetup([string]$version) {
        $this.pythonVersion = $version
        if ($this.pythonVersion -eq "3.10") {
            $this.pythonInstallUrl = "https://www.python.org/ftp/python/3.10.6/python-3.10.6.exe"
        } elseif ($this.pythonVersion -eq "3.11") {
            $this.pythonInstallUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe"
        } else {
            Write-Host "Unsupported Python version. Please set to either '3.10' or '3.11'."
            exit 1
        }
    }

    # Check if Python is installed
    [bool]Check-PythonInstalled() {
        try {
            $pythonVersion = & python --version
            Write-Host "Python is already installed: $pythonVersion"
            return $true
        } catch {
            Write-Host "Python is not installed."
            return $false
        }
    }

    # Download and install Python
    Install-Python() {
        Write-Host "Downloading Python installer..."
        Invoke-WebRequest -Uri $this.pythonInstallUrl -OutFile $this.pythonInstallPath

        Write-Host "Installing Python..."
        Start-Process -FilePath $this.pythonInstallPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

        # Verify Installation
        if ($this.Check-PythonInstalled()) {
            Write-Host "Python installation successful."
        } else {
            Write-Error "Python installation failed."
            exit 1
        }
    }

    # Create Python virtual environment
    Create-VirtualEnv() {
        Write-Host "Creating virtual environment..."

        # Navigate to project folder
        if (-Not (Test-Path -Path $this.projectFolder)) {
            Write-Host "Creating project folder..."
            New-Item -ItemType Directory -Path $this.projectFolder
        }

        Set-Location -Path $this.projectFolder

        # Create virtual environment
        python -m venv $this.envName
        Write-Host "Virtual environment '$this.envName' created successfully."
    }

    # Install required packages into the virtual environment
    Install-Packages() {
        Write-Host "Activating virtual environment and installing packages..."
        
        # Activate virtual environment (Windows specific)
        .\$this.envName\Scripts\Activate.ps1

        # Install required Python packages
        foreach ($package in $this.pythonPackages) {
            Write-Host "Installing package: $package"
            pip install $package
        }

        # Update all packages to latest versions
        Write-Host "Updating all installed packages..."
        pip install --upgrade --quiet --no-cache-dir -r requirements.txt

        Write-Host "All packages installed and updated successfully."
    }

    # Setup necessary files and folders
    Setup-Files() {
        Write-Host "Setting up necessary files and folders..."

        # Create contacts.csv with 'phone' column
        $csvFilePath = "$this.projectFolder\contacts.csv"
        if (-Not (Test-Path -Path $csvFilePath)) {
            $contactsCsvContent = "phone`n"
            $contactsCsvContent | Out-File -FilePath $csvFilePath
            Write-Host "Created contacts.csv file with 'phone' column."
        }

        # Create images folder
        $imagesFolderPath = "$this.projectFolder\images"
        if (-Not (Test-Path -Path $imagesFolderPath)) {
            New-Item -ItemType Directory -Path $imagesFolderPath
            Write-Host "Created images folder."
        }
    }

    # Copy Python files into the project folder
    Copy-PythonFiles([string]$sourceFile1, [string]$sourceFile2) {
        Write-Host "Copying Python files to project folder..."

        $destinationFolder = "$this.projectFolder"
        
        # Copy first Python file
        if (Test-Path -Path $sourceFile1) {
            Copy-Item -Path $sourceFile1 -Destination $destinationFolder
            Write-Host "Copied first Python file."
        } else {
            Write-Host "First Python file not found."
        }

        # Copy second Python file
        if (Test-Path -Path $sourceFile2) {
            Copy-Item -Path $sourceFile2 -Destination $destinationFolder
            Write-Host "Copied second Python file."
        } else {
            Write-Host "Second Python file not found."
        }
    }
}

# Define a helper class for handling script execution
class ScriptExecutor {
    [PythonSetup]$pythonSetup
    [string]$sourceFile1
    [string]$sourceFile2

    # Constructor to initialize Python setup and source file paths
    ScriptExecutor([string]$pythonVersion, [string]$file1, [string]$file2) {
        $this.pythonSetup = [PythonSetup]::new($pythonVersion)
        $this.sourceFile1 = $file1
        $this.sourceFile2 = $file2
    }

    # Run the complete setup process
    Run() {
        Write-Host "Starting the setup process..."

        # Check for Python installation or install if not present
        if (-Not $this.pythonSetup.Check-PythonInstalled()) {
            $this.pythonSetup.Install-Python()
        }

        # Create virtual environment
        $this.pythonSetup.Create-VirtualEnv()

        # Install required Python packages
        $this.pythonSetup.Install-Packages()

        # Setup project files and folders
        $this.pythonSetup.Setup-Files()

        # Copy Python files (ensure you specify correct paths for your files)
        $this.pythonSetup.Copy-PythonFiles($this.sourceFile1, $this.sourceFile2)

        Write-Host "Setup complete."
    }
}

# Main Script Execution
$pythonVersion = "3.11"  # Choose either "3.10" or "3.11"

# Get the current script directory where the PowerShell script is located
$currentScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set the source Python files based on the current script directory
$sourcePythonFile1 = "$currentScriptDirectory\detection_based_automation.py"  # Adjust this file name
$sourcePythonFile2 = "$currentScriptDirectory\web_based_automation.py"  # Adjust this file name

# Instantiate the ScriptExecutor class and run the setup
$executor = [ScriptExecutor]::new($pythonVersion, $sourcePythonFile1, $sourcePythonFile2)
$executor.Run()
