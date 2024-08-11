#!/bin/bash

# Function to check if pyenv is installed
function check_pyenv_installed {
    if command -v pyenv &>/dev/null; then
        echo "pyenv is already installed."
        return 0
    else
        echo "pyenv is not installed. Installing pyenv..."
        return 1
    fi
}

# Function to install pyenv
function install_pyenv {
    curl https://pyenv.run | bash

    # Add pyenv to the shell
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    
    # Add pyenv to bashrc for future sessions
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
}

# Function to install Python 3 via pyenv
function install_python_via_pyenv {
    local python_version=$1

    if pyenv versions | grep -q "$python_version"; then
        echo "Python $python_version is already installed via pyenv."
    else
        echo "Installing Python $python_version via pyenv..."
        pyenv install $python_version
        pyenv global $python_version
    fi
}

# Function to check if pipenv is installed
function check_pipenv_installed {
    if pipenv --version &>/dev/null; then
        echo "pipenv is already installed."
        return 0
    else
        echo "pipenv is not installed. Installing pipenv..."
        return 1
    fi
}

# Function to install pipenv via pip
function install_pipenv {
    pip install pipenv
}

function install_other_python_deps {
    pip install Pillow
}

# Main script execution
PYTHON_VERSION="3.12"

if ! check_pyenv_installed; then
    install_pyenv
fi

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

install_python_via_pyenv $PYTHON_VERSION

if ! check_pipenv_installed; then
    install_pipenv
fi

install_other_python_deps

echo "Installation completed. Python $PYTHON_VERSION and pipenv are ready to use."