#!/bin/bash

# Function to update Linux
update_linux() {
    echo "Updating Linux..."
    sudo apt update
    sudo apt upgrade -y
    echo "Linux update completed."
}

# Function to include WiFi credentials
include_wifi_credentials() {
    echo "Please enter your WiFi credentials:"
    read -p "SSID: " ssid
    read -p "Password: " password
    echo ""
    
    # Configure WiFi
    sudo cat >> /etc/wpa_supplicant/wpa_supplicant.conf <<EOT 
network={
    ssid="$ssid"
    psk="$password"
}
EOT
    
    echo "WiFi credentials added."
}

# Main script
while true; do
    echo "Select an option:"
    echo "1. Update Linux"
    echo "2. Include WiFi credentials"
    echo "3. Quit"
    
    read -p "Enter your choice: " choice
    echo ""
    
    case $choice in
        1)
            update_linux
            ;;
        2)
            include_wifi_credentials
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
    
    echo ""
done