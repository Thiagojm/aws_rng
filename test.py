import subprocess

# the command to run
command = "bin/seedd -sv"

# create the process
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# read the output
chunk, _ = process.communicate()
msg = chunk.decode()
print(msg)
if "No devices found." in msg or msg == "":
    print("No bitbbalber device found.")
    
else:
    print("Found bitbbalber device.")
    