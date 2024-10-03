#!/bin/bash

# Define the base directory (assuming this script is executed from the project root)
BASE_DIR=$(pwd)
export BASE_DIR

# Enable error handling and debugging
function enable_error_handling_debugging {
    set -e
    set -x
    set -u
    set -o pipefail
}

function install_dependencies {
    # Define the dependencies required for functional testing.
    dependencies=("python3" "python3-pip" "python3-venv" "fonts-liberation" "libu2f-udev" "libvulkan1" "xdg-utils" "unzip" "xclip")

    # Update the package list to ensure the latest versions of the packages are available.
    echo "Updating package list..."
    for attempt in 1 2 3; do
        sudo apt-get update && break
        echo "apt-get update failed on attempt $attempt. Retrying in 5 seconds..."
        sleep 5
    done
   

    # Check if the dependencies are already installed, and if not, install them.
    echo "Checking and installing dependencies..."
    for pkg in "${dependencies[@]}"; do
        if dpkg --get-selections | grep -q "^$pkg[[:space:]]*install$" >/dev/null; then
            echo -e "$pkg is already installed"
        else
            echo -e "$pkg is NOT installed. Installing..."
            for attempt in {1..3}; do
                sudo apt-get install -y $pkg && break || { echo "Attempt $attempt to install $pkg failed. Retrying..."; sleep 5; }
            done
        fi
    done
}

function install_chrome_and_chrome_driver {
    echo "Adding Google Chrome repository..."
    if ! grep -q "^deb \[arch=amd64\] http://dl.google.com/linux/chrome/deb/ stable main" /etc/apt/sources.list.d/google-chrome.list 2>/dev/null; then
        sudo sh -c 'wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -'
        sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
    else
        echo "Google Chrome repository already added."
    fi



    # Attempt to install Google Chrome, fixing broken installs if necessary
    sudo apt-get update
    sudo apt-get -f install
    sudo apt-get install -y google-chrome-stable

    # Specify the known ChromeDriver version
    CHROMEDRIVER_VERSION="124.0.6367.78"

    # Construct the download URL using the specified version
    CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"

    echo "Downloading ChromeDriver version ${CHROMEDRIVER_VERSION}..."
    wget -q "${CHROMEDRIVER_URL}" -O chromedriver-linux64.zip

    # Check if the download was successful
    if [ ! -f chromedriver-linux64.zip ]; then
        echo "Failed to download ChromeDriver."
        exit 1
    fi


    echo "Unzipping ChromeDriver..."
    unzip -q chromedriver-linux64.zip
    cd chromedriver-linux64

    # Check if unzip was successful
    if [ ! -f chromedriver ]; then
        echo "Unzip failed to extract ChromeDriver."
        exit 1
    fi

    # Move ChromeDriver to /usr/bin/ or another directory in your PATH

    sudo mv chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver

    echo "ChromeDriver installation complete."
}

function setup_python {
    # Setup Python Virtual Environment
    echo "Setting up Python virtual envirnment..."
    python3 -m venv venv
     # Check if the virtual environment was created successfully
    if [ ! -d "venv" ]; then
        echo "Failed to create Python virtual environment."
        exit 1
    fi
    source venv/bin/activate
    # Install Python packages
    echo "Installing Python packages..."
    cd ${BASE_DIR}
    pip install -r config/requirements.txt || { echo "Failed to install Python packages."; exit 1; }
}

function configure_env_variables {
    # Configure Environment Variables
    echo 'Configuring environment variables...'
    export CHROME_DRIVER_PATH='/usr/bin/chromedriver'
    export TARGET_URL='http://skander-nextcloud.lijo'
    export USERNAME=$1
    export PASSWORD=$2
    export CREATED_FILES_PATH='created_files'
    export FILE_SIZE_MEDIUM=1
    export FILE_SIZE_LARGE=1
    export DOWNLOADS_PATH='downloads'
    export USERNAME='admin'
    export PASSWORD='?aymen!lijo!pass!'
}

function run_tests {
    # Run tests and handle failures   
    echo 'Runninng tests...'
    pytest -s file_management_cycle.py || { echo "Tests failed."; exit 1; }
}

function cleanup {

    echo "Cleaning up  downloaded files..."
    DOWNLOADS_DIRECTORY="$BASE_DIR/$DOWNLOADS_PATH"

    if [ "$(ls -A $DOWNLOADS_DIRECTORY)" ]; then
        python3 cleanup/delete_test_files.py
    else
        echo "No files found in $DOWNLOADS_DIRECTORY."
    fi

    # Deactivate the virtual environment
    echo "Deactivating the virtual environment..."
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi

    # Clean up ChromeDriver directory
    echo "Cleaning up ChromeDriver directory..."
    CHROMEDRIVER_DIRECTORY="$BASE_DIR/chromedriver-linux64"
    if [ -d "$CHROMEDRIVER_DIRECTORY" ]; then
        rm -rf "$CHROMEDRIVER_DIRECTORY"
    else
        echo "Directory $CHROMEDRIVER_DIRECTORY does not exist."
    fi

    # Clean up ChromeDriver zip file
    echo "Cleaning up ChromeDriver zip file..."
    CHROMEDRIVER_ZIP="$BASE_DIR/chromedriver-linux64.zip"
    if [ -f "$CHROMEDRIVER_ZIP" ]; then
        rm -f "$CHROMEDRIVER_ZIP"
    else
        echo "File $CHROMEDRIVER_ZIP does not exist."
    fi

    # Clean up Python Packages
    echo "Cleaning up Python packages..."
    pip uninstall -y -r $BASE_DIR/config/requirements.txt
    
    # Clean up ChromeDriver
    echo "Cleaning up ChromeDriver..."
    if [ -f "/usr/bin/chromedriver" ]; then
        sudo rm /usr/bin/chromedriver
    else
        echo "File /usr/bin/chromedriver does not exist."
    fi

    # Clean up Chrome
    echo "Cleaning up Chrome..."
    if dpkg --get-selections | grep -q "^google-chrome-stable[[:space:]]*install$"; then
        sudo apt-get remove -y google-chrome-stable
    else
        echo "Package google-chrome-stable is not installed."
    fi

    # Clean up the virtual environment
    if [ -d "venv" ]; then
        echo "Cleaning up the virtual environment..."
        rm -rf venv
    else
        echo "Directory venv does not exist."
    fi
    
    # Remove temporary files and directories
    echo "Removing temporary files and directories..."
    if [ -d "chromedriver-linux64" ]; then
        rm -rf chromedriver-linux64
    else
        echo "Directory chromedriver-linux64 does not exist."
    fi
    if [ -f "chromedriver-linux64.zip" ]; then
        rm -f chromedriver-linux64.zip
    else
        echo "File chromedriver-linux64.zip does not exist."
    fi

     # Delete created environment variables
    echo "Deleting created envronment variables"
    unset CHROME_DRIVER_PATH
    unset TARGET_URL
    unset USERNAME
    unset PASSWORD
    unset CREATED_FILES_PATH

}

function build_py_library {
    echo "Building Python library..."
    pip install --upgrade pip setuptools wheel
    cd ${BASE_DIR}
    cd ..
    pip install -e .
    cd functional_testing
}

# Run functions in order
enable_error_handling_debugging
trap cleanup EXIT
install_dependencies
install_chrome_and_chrome_driver
setup_python
configure_env_variables $1 $2
build_py_library
run_tests







