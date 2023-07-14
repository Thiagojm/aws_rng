# True Random Number Generator (TRNG) Data Collector

This Python application is designed for a Raspberry Pi with a TRNG device (TrueRNG, TrueRNGpro, or TrueRNGoroV2). It reads in a number of bits from the TRNG at a user-specified interval and counts the number of 'ones'. The datetime and count are then stored in a .csv file and the bits collected are appended to a .bin file for control.

The project consists of three main scripts:

1. Main Startup Script (start_rng.py): This script is the entry point of the project. At startup, it first checks for an Internet connection and upon establishing a successful connection, it synchronizes the system time to GMT-3 (São Paulo). Finally, it launches the two other scripts (rng_collect.py and send_aws.py) in separate terminals.

2. RNG Collect Script (rng_collect.py): This script collects random number generator (RNG) data.

3. Send AWS Script (send_aws.py): This script sends the collected RNG data to an AWS service.

The project also includes a variables.env file, which holds environment variables that are required by the rng_collect.py and send_aws.py scripts.

## Requirements

- Raspberry Pi with Python3 installed
- A TRNG device (TrueRNG)
- Internet access
- Python 3.x
- lxterminal package installed (default in most Raspberry Pi distributions)
- The following Python packages: **bitstring**, **python-dotenv**, **pyserial**, **boto3**, **requests**, **ntplib**, **pytz**.

## Setup

1. Install the required packages if they are not already installed: 
>
    pip install bitstring python-dotenv pyserial requests ntplib pytz

2. In the `vars` folder, rename the `variables.env.default` to `variables.env` and edit to specify the sample size (in bits), the interval between samples, the duration for each data collection cycle, and the paths for the temporary and upload folders. Also give your raspberry a unique ID name, use your AWS keys and bucket name. 

## Installation

Clone the repository or copy the scripts to your Raspberry Pi.
Give execute permissions to the scripts:

>
    chmod +x /path/to/start_rng.py  
    chmod +x /path/to/rng_collect.py  
    chmod +x /path/to/send_aws.py

Create an autostart entry:

> 
    nano /home/pi/.config/autostart/start_rng.desktop

Insert the following content into the .desktop file:

>
    [Desktop Entry]
    Type=Application
    Name=StartRng
    Exec=/usr/bin/lxterminal -e "python3 /path/to/start_rng.py.py; bash"

Save and exit the file.  
Make the .desktop file executable:

>
    chmod +x /home/pi/.config/autostart/start_rng.desktop

## Usage

The scripts will run automatically on startup. The main script checks for an internet connection and synchronizes the system time, while the rng_collect.py and send_aws.py scripts will be launched in separate terminal windows.

## Support

If you encounter any problems or have any suggestions, please open an issue or a pull request.

## License

This project is open source, under the MIT license.