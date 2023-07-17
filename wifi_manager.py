import os
import subprocess
import tempfile

WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

def print_wpa_supplicant_content():
    try:
        print(subprocess.check_output(['sudo', 'cat', WPA_SUPPLICANT_CONF]).decode())
    except Exception as e:
        print(f"Failed to print the content of wpa_supplicant.conf: {str(e)}")

def add_wifi(ssid, password):
    try:
        network_string = f'\nnetwork={{\n\tssid="{ssid}"\n\tpsk="{password}"\n}}\n'
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(network_string.encode())
        
        # Append the new network to the original file
        subprocess.check_call(['sudo', 'bash', '-c', f'cat {tmpfile.name} >> {WPA_SUPPLICANT_CONF}'])

    except Exception as e:
        print(f"Failed to add Wi-Fi: {str(e)}")

def edit_wifi(ssid):
    # Read the file with sudo
    process = subprocess.Popen(['sudo', 'cat', WPA_SUPPLICANT_CONF], stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()

    lines = output.split("\n")
    found = False
    for index, line in enumerate(lines):
        if ssid in line:
            found = True
            print(f"\nSSID {ssid} found. Please enter the new password.")
            password = input("New Password: ")
            lines[index + 1] = f'\tpsk="{password}"'
            break

    if not found:
        print(f"\nSSID {ssid} not found. Please check and try again.")
        return

    # Write the changes back to the file
    process = subprocess.Popen(['sudo', 'tee', WPA_SUPPLICANT_CONF], stdin=subprocess.PIPE)
    process.communicate("\n".join(lines).encode())
    print(f"Wi-Fi password updated for SSID {ssid}.")


def remove_wifi(ssid):
    try:
        network_string = subprocess.check_output(['sudo', 'cat', WPA_SUPPLICANT_CONF]).decode()
        networks = network_string.split('network={')[1:]
        networks = [network for network in networks if f'ssid="{ssid}"' not in network]
        network_string = 'network={'.join(networks)
        
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(network_string.encode())
        
        # Replace the original file with the temp file
        subprocess.check_call(['sudo', 'mv', tmpfile.name, WPA_SUPPLICANT_CONF])
    except Exception as e:
        print(f"Failed to remove Wi-Fi: {str(e)}")
