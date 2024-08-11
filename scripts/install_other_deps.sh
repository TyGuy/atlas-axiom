#!/bin/bash

# Function to check if sshpass is installed, and install it if it's not
check_and_install_sshpass() {
    if ! command -v sshpass &> /dev/null; then
        echo "sshpass not found. Installing sshpass..."
        sudo apt-get install -y sshpass
        if [ $? -eq 0 ]; then
            echo "sshpass installed successfully."
        else
            echo "Failed to install sshpass."
            exit 1
        fi
    else
        echo "sshpass is already installed."
    fi
}

# Run the function
check_and_install_sshpass