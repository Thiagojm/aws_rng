import os
import subprocess

WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

def add_wifi(ssid, password):
    command = f'sudo bash -c \'printf "\\nnetwork={{\\n\\tssid=\\"{ssid}\\"\\n\\tpsk=\\"{password}\\"\\n}}\\n" >> {WPA_SUPPLICANT_CONF}\''
    os.system(command)
    subprocess.run(["wpa_cli", "-i", "wlan0", "reconfigure"], check=True)

def get_all_ssids():
    ssids = []
    with open(WPA_SUPPLICANT_CONF, "r") as f:
        for line in f:
            if "ssid" in line:
                ssids.append(line.split('=')[1].strip().replace('"', ''))
    return ssids

def remove_wifi(ssid):
    # Copy wpa_supplicant.conf to a temp file
    os.system("sudo cp {} ./temp.conf".format(WPA_SUPPLICANT_CONF))
    
    with open("temp.conf", "r") as f:
        lines = f.readlines()
    with open("temp.conf", "w") as f:
        inside_network = False
        for line in lines:
            if "network={" in line:
                inside_network = True
            if inside_network and f'ssid="{ssid}"' in line:
                continue
            if "}" in line:
                inside_network = False
                if f'ssid="{ssid}"' not in lines:
                    f.write(line)
            elif not inside_network:
                f.write(line)
    
    # Replace wpa_supplicant.conf with the temp file
    os.system("sudo mv ./temp.conf {}".format(WPA_SUPPLICANT_CONF))
    subprocess.run(["wpa_cli", "-i", "wlan0", "reconfigure"], check=True)

def edit_wifi(ssid, new_password):
    remove_wifi(ssid)
    add_wifi(ssid, new_password)
