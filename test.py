import subprocess


try:
    subprocess.check_call(["sudo", "systemctl", "disable", "--now", "seedd.service"])
    print("seedd.service disabled successfully.")
except subprocess.CalledProcessError:
    print("Failed to disable seedd.service.")
