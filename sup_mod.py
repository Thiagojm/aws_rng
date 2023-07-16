import csv
import subprocess
import serial
import time
from serial.tools import list_ports
from bitstring import BitArray
from datetime import datetime
import os
import shutil
from dotenv import load_dotenv

# Load environment variables
def load_environment_variables():
    load_dotenv('vars/variables.env')
    num_bits = int(os.getenv('SAMPLE_VALUE'))  # in bits
    interval = int(os.getenv('INTERVAL_VALUE'))  # interval in seconds
    sample_duration = int(os.getenv('SAMPLE_DURATION'))  # duration in seconds
    temp_folder = os.getenv('TEMP_FOLDER')
    upload_folder = os.getenv('UPLOAD_FOLDER')
    fold = os.getenv('FOLD')
    return num_bits, interval, sample_duration, temp_folder, upload_folder, fold

# Check for and create folders
def check_and_create_folders(temp_folder, upload_folder):
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

########## Bitbabbler ##########
# check for bitbbabler
def check_bitb():
    # the command to run
    command = "seedd -sv"

    # create the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # read the output
    chunk, _ = process.communicate()
    msg = chunk.decode()
    if "No devices found" in msg or msg == "":
        print("No bitbbalber device found.")
        return False
    else:
        print("Found bitbbalber device.")
        return True

# Loop for bitbbabler
def collect_bitb(device, temp_folder, upload_folder, filename_base, num_bits, interval, sample_duration, fold):
    start_time = time.time()
    print(f"Starting capture...\n")
    num_loop = 1
    total_bytes = 0
    try:
        while True:
            current_time = time.time()
            if current_time - start_time >= sample_duration:
                num_loop = 1
                total_bytes = 0
                filename_base = move_files_and_update_filename(temp_folder, upload_folder, num_bits, interval, device, fold)
                start_time = current_time  # reset the start time       
            
            # the command to run
            command = f"seedd --limit-max-xfer --no-qa -f{fold} -b {(num_bits // 8)}"

            # create the process
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            # read the output
            bits, _ = process.communicate()
            count = count_ones(bits)
            
            # Write data to files in TEMP_FOLDER
            write_to_csv(count, os.path.join(temp_folder, filename_base + '.csv'))
            write_to_bin(bits, os.path.join(temp_folder, filename_base + '.bin'))

            # Sleep for the remaining time
            total_bytes += num_bits / 8    
            print(f"Collecting data - Loop: {num_loop} - Total bytes collected: {int(total_bytes)}")
            num_loop += 1
            time.sleep(max(interval - (time.time() - current_time), 0))
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Exiting.')
        return
    except Exception as e:
        print(f'Error: {e}')
        return

########## TrueRNG ##########
# Check for TrueRNG
def check_trng():
    rng_com_port = None

    # Call list_ports to get com port info
    ports_avaiable = list_ports.comports()

    for temp in ports_avaiable:
        if '04D8:F5FE' in temp[2]:
            print(f'Found TrueRNG on {temp[0]} \n')
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=temp[0]
        if '16D0:0AA0' in temp[2]:
            print(f'Found TrueRNGPro on {temp[0]} \n')
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=temp[0]
        if '04D8:EBB5' in temp[2]:
            print(f'Found TrueRNGoroV2 on {temp[0]} \n')
            if rng_com_port == None:        # always chooses the 1st TrueRNG found
                rng_com_port=temp[0]
    if rng_com_port == None:
        print(f'No TrueRNG found.\n')
        
    return rng_com_port

# Get the com port for the TrueRNG
def setup_serial(rng_com_port):
    # Try to setup and open the comport
    ser = serial.Serial(port=rng_com_port, timeout=10)  # timeout set at 10 seconds in case the read fails
            
    # Open the serial port if it isn't open
    if(ser.isOpen() == False):
        ser.open()

    # Set Data Terminal Ready to start flow
    ser.setDTR(True)

    # This clears the receive buffer so we aren't using buffered data
    ser.flushInput()

    return ser

# Read the bits from the TrueRNG
def read_bits(num_bytes, rng):
    # Read the specified number of bytes
    bits = rng.read(num_bytes)

    return bits

def collect_trng(device, temp_folder, upload_folder, filename_base, num_bits, interval, sample_duration, rng):
    start_time = time.time()
    print(f"Starting capture...\n")
    num_loop = 1
    total_bytes = 0
    while True:
        try:
            current_time = time.time()
            if current_time - start_time >= sample_duration:
                num_loop = 1
                total_bytes = 0
                filename_base = move_files_and_update_filename(temp_folder, upload_folder, num_bits, interval, device, fold=0)
                start_time = current_time  # reset the start time
            
            rng.flushInput()
            bits = read_bits(num_bits // 8, rng)
            count = count_ones(bits)
            
            # Write data to files in TEMP_FOLDER
            write_to_csv(count, os.path.join(temp_folder, filename_base + '.csv'))
            write_to_bin(bits, os.path.join(temp_folder, filename_base + '.bin'))

            # Sleep for the remaining time
            total_bytes += num_bits / 8    
            print(f"Collecting data - Loop: {num_loop} - Total bytes collected: {int(total_bytes)}")
            num_loop += 1
            time.sleep(max(interval - (time.time() - current_time), 0))
        except KeyboardInterrupt:
            print('Keyboard interrupt detected. Exiting.')
            return
        except Exception as e:
            print(f'Error: {e}')
            return

### File handling ###
# get filename base
def get_filename(num_bits, interval, device, fold):

    # Get current datetime and format it
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%dT%H%M%S")

    # Create base filename with pi serial and current datetime
    filename_base = f'{formatted_now}_{device}_s{num_bits}_i{interval}'  
    if device == 'bitb':
        filename_base += f'_f{fold}'

    return filename_base

# Move files from temp folder to upload folder and update filename base
def move_files_and_update_filename(temp_folder, upload_folder, num_bits, interval, device, fold):
    for file_name in os.listdir(temp_folder):
        shutil.move(os.path.join(temp_folder, file_name), upload_folder)

    filename_base = get_filename(num_bits, interval, device, fold)
    return filename_base

def write_to_csv(count, filename):
    now = datetime.now()

    # Format datetime to look like "2023-07-12T16:35:12"
    formatted_now = now.strftime("%Y%m%dT%H:%M:%S")

    # Open the CSV file in append mode
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write the current datetime and the count of ones
        writer.writerow([formatted_now, count])

def write_to_bin(bits, filename):
    # Open the binary file in append mode
    with open(filename, 'ab') as file:
        file.write(bits)

#### Computations ####

# Count the number of ones in the bit string
def count_ones(bits):
    bit_array = BitArray(bytes=bits)
    return bit_array.count('0b1')



# def get_rng_and_filename(num_bits, interval):
#     rng_com_port = find_trng()
#     if rng_com_port is None:
#         print('No RNG device found. Exiting.')
#         return None, None

#     rng = setup_serial(rng_com_port)

#     # Get current datetime and format it
#     now = datetime.now()
#     formatted_now = now.strftime("%Y%m%dT%H%M%S")

#     # Create base filename with pi serial and current datetime
#     filename_base = f'{formatted_now}_trng_s{num_bits}_i{interval}'  # 'pi_serial_2023-07-12T16:35:12_trng_s1000000_i0.1

#     return rng, filename_base


