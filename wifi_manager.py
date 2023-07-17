import os
import subprocess

WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

def print_wpa_supplicant_content():
    try:
        print(subprocess.check_output(['sudo', 'cat', WPA_SUPPLICANT_CONF]).decode())
    except Exception as e:
        print(f"Failed to print the content of wpa_supplicant.conf: {str(e)}")

def add_wifi(ssid, password):
    try:
        with open(WPA_SUPPLICANT_CONF, "a") as f:
            f.write('\nnetwork={\n')
            f.write(f'\tssid="{ssid}"\n')
            f.write(f'\tpsk="{password}"\n')
            f.write('}\n')
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
        with open(WPA_SUPPLICANT_CONF, 'w') as f:
            f.write(network_string)
    except Exception as e:
        print(f"Failed to edit Wi-Fi: {str(e)}")

def remove_wifi(ssid):
    try:
        network_string = subprocess.check_output(['sudo', 'cat', WPA_SUPPLICANT_CONF]).decode()
        networks = network_string.split('network={')[1:]
        networks = [network for network in networks if f'ssid="{ssid}"' not in network]
        network_string = 'network={'.join(networks)
        with open(WPA_SUPPLICANT_CONF, 'w') as f:
            f.write(network_string)
    except Exception as e:
        print(f"Failed to remove Wi-Fi: {str(e)}")
