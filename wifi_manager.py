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

def edit_wifi(ssid, password):
    try:
        network_string = subprocess.check_output(['sudo', 'cat', WPA_SUPPLICANT_CONF]).decode()
        networks = network_string.split('network={')[1:]
        for i, network in enumerate(networks):
            if f'ssid="{ssid}"' in network:
                networks[i] = f'\nnetwork={{\n\tssid="{ssid}"\n\tpsk="{password}"\n}}\n'
        network_string = 'network={'.join(networks)
        
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(network_string.encode())
        
        # Replace the original file with the temp file
        subprocess.check_call(['sudo', 'mv', tmpfile.name, WPA_SUPPLICANT_CONF])

    except Exception as e:
        print(f"Failed to edit Wi-Fi: {str(e)}")

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
