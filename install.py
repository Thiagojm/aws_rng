import os
import subprocess

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
    packages = ["bitstring", "python-dotenv", "pyserial", "requests", "ntplib", "pytz", "boto3"]
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
    udev_rule_path = "/etc/udev/rules.d/99-BitBabbler.rules"
    try:
        with open(udev_rule_path, 'w') as f:
            f.write(udev_rule)
        subprocess.check_call(["sudo", "udevadm", "control", "--reload-rules"])
        print("UDEV rule created successfully.")
    except Exception as e:
        print(f"Failed to create the UDEV rule: {e}")
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
    # Implement your wifi setup procedure here
    print("Setting Up Wifi...")

def change_install():
    # Implement your change installation procedure here
    print("Changing Install...")

if __name__ == "__main__":
    main()
