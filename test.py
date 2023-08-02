import subprocess


try:
    subprocess.check_call(["sudo", "systemctl", "disable", "--now", "seedd.service"])
    print("Device installed successfully.")
except subprocess.CalledProcessError:
    print("Failed to install the device.")
