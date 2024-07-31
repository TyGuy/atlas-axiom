#!/bin/bash

# Function to check if Java is installed
function check_java_installed {
    if java -version &>/dev/null; then
        echo "Java is already installed."
        return 0
    else
        echo "Java is not installed. Installing Java..."
        return 1
    fi
}

# Function to install Java
function install_java {
    sudo apt update
    sudo apt install -y default-jdk
}

# Function to download UGS
function download_ugs {
    if [ ! -f "UniversalGcodeSender.zip" ]; then
        echo "Downloading UGS..."
        wget https://github.com/winder/Universal-G-Code-Sender/releases/download/v2.1.8/UniversalGcodeSender.zip
    else
        echo "UGS zip file already downloaded."
    fi
}

# Function to extract UGS
function extract_ugs {
    if [ ! -d "ugsplatform" ]; then
        echo "Extracting UGS..."
        unzip UniversalGcodeSender.zip -d ugsplatform
        cd ugsplatform/UniversalGcodeSender
        chmod 777 start.sh
    else
        echo "UGS already extracted."
    fi
}

# Main script execution
if ! check_java_installed; then
    install_java
fi

download_ugs
extract_ugs
