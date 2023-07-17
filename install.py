import os
import subprocess
import wifi_manager

def create_env_file():
    # Path to the default file
    default_file_path = os.path.expanduser("~/Desktop/aws_rng/vars/variables.env.default")

    # Path to the new file
    new_file_path = os.path.expanduser("~/Desktop/aws_rng/vars/variables.env")

    # Open the default file
    with open(default_file_path, 'r') as default_file:
        # Open the new file
        with open(new_file_path, 'w') as new_file:
            # Loop over each line in the default file
            for line in default_file:
                # If the line contains an equals sign
                if '=' in line:
                    # Split the line into a key and a comment
                    key, default_value_comment = line.split('=')
                    # Try to split into default value and comment
                    parts = default_value_comment.split('#', 1)
                    default_value = parts[0].strip()

                    # If there's a comment, we take it. Otherwise, we use an empty string
                    comment = parts[1].strip() if len(parts) > 1 else ""

                    # If the key ends with a space, remove it
                    if key.endswith(' '):
                        key = key[:-1]

                    # Ask the user for the value of the key
                    value = input(f"Please enter a value for {key} (default: {default_value}): ")

                    # Use default value if user did not provide one
                    if not value:
                        value = default_value

                    # Write the key-value pair to the new file
                    new_file.write(f"{key}={value} # {comment}\n")
                else:
                    # Write the line to the new file as-is
                    new_file.write(line)

    print("Created new environment file at: ", new_file_path)


def full_install():
    print("Starting Full Install...")

    # Install Python packages
    packages = ["bitstring", "python-dotenv", "pyserial", "requests", "ntplib", "pytz", "boto3", "ntplib"]
    try:
        subprocess.check_call(["pip3", "install"] + packages)
        print("Python packages installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install Python packages.")
        return

    # Install the device
    device_file_path = os.path.expanduser("~/Desktop/aws_rng/bitbabbler_setup/bit-babbler_0.8_arm64.deb")
    try:
        subprocess.check_call(["sudo", "dpkg", "-i", device_file_path])
        print("Device installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install the device.")
        return

    # Create the UDEV rule
    udev_rule = (
        '# Voicetronics BitBabbler Black and White\n'
        'SUBSYSTEM=="usb", ACTION=="add|change", ATTRS{idVendor}=="0403", '
        'ATTRS{idProduct}=="7840", SYMLINK="BitBabbler", MODE="0666"'
    )
    udev_rule_path = "/etc/udev/rules.d/60-bit-babbler.rules"
    try:
        # Use 'sudo' to create and write to the file
        subprocess.check_call(["sudo", "bash", "-c", f"echo '{udev_rule}' > {udev_rule_path}"])
        subprocess.check_call(["sudo", "udevadm", "control", "--reload-rules"])
        print("UDEV rule created successfully.")
    except Exception as e:
        print(f"Failed to create the UDEV rule: {e}")
        return

    # Make python scripts executable
    scripts = ["start_rng.py", "rng_collect.py", "send_aws.py"]
    for script in scripts:
        script_path = os.path.expanduser(f"~/Desktop/aws_rng/{script}")
        try:
            subprocess.check_call(["chmod", "+x", script_path])
            print(f"{script} made executable.")
        except subprocess.CalledProcessError:
            print(f"Failed to make {script} executable.")
            return

    # Create autostart entry
    desktop_entry_content = (
        '[Desktop Entry]\n'
        'Type=Application\n'
        'Name=StartRng\n'
        'Exec=/usr/bin/lxterminal -e "python3 /home/pi/Desktop/aws_rng/start_rng.py; bash"'
    )
    desktop_entry_dir = "/home/pi/.config/autostart"
    desktop_entry_path = f"{desktop_entry_dir}/start_rng.desktop"
    try:
        # Check if the directory exists, if not, create it
        if not os.path.isdir(desktop_entry_dir):
            os.makedirs(desktop_entry_dir)

        # Use 'sudo' to create and write to the file
        subprocess.check_call(["sudo", "bash", "-c", f"echo '{desktop_entry_content}' > {desktop_entry_path}"])
        subprocess.check_call(["sudo", "chmod", "+x", desktop_entry_path])
        print("Autostart entry created successfully.")
    except Exception as e:
        print(f"Failed to create autostart entry: {e}")
        return

    # Create variables.env file from template
    create_env_file()


def main():
    while True:
        print("Welcome to Raspberry Pi Installer!")
        print("1- Full Install")
        print("2- Wifi Setup")
        print("3- Change Install")
        print("4- Quit")
        
        choice = input("Please enter a number: ")

        if choice == '1':
            full_install()
        elif choice == '2':
            wifi_setup()  # implement your wifi setup function here
        elif choice == '3':
            change_install()  # implement your change installation function here
        elif choice == '4':
            break  # Exit the while loop
        else:
            print("Invalid input. Please enter a number from 1 to 4.")

        print("\n")  # print a newline for better readability


def wifi_setup():
    while True:
        print("\n1. Add Wi-Fi\n2. Edit Wi-Fi\n3. Remove Wi-Fi\n4. Back")
        choice = input("Choose an option: ")
        if choice == "1":
            ssid = input("Enter the SSID of the Wi-Fi network you want to add: ")
            password = input("Enter the password: ")
            wifi_manager.add_wifi(ssid, password)
            print(f"Wi-Fi network {ssid} added successfully.")
        elif choice == "2":
            ssid = input("Enter the SSID of the Wi-Fi network you want to edit: ")
            new_password = input("Enter the new password: ")
            wifi_manager.edit_wifi(ssid, new_password)
            print(f"Password updated for Wi-Fi network {ssid}.")
        elif choice == "3":
            ssid = input("Enter the SSID of the Wi-Fi network you want to remove: ")
            wifi_manager.remove_wifi(ssid)
            print(f"Wi-Fi network {ssid} removed successfully.")
        elif choice == "4":
            break
        else:
            print("Invalid option. Please try again.")


def change_install():
    create_env_file()


if __name__ == "__main__":
    main()
