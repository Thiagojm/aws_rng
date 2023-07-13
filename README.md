# True Random Number Generator (TRNG) Data Collector

This Python application is designed for a Raspberry Pi with a TRNG device (TrueRNG, TrueRNGpro, or TrueRNGoroV2). It reads in a number of bits from the TRNG at a user-specified interval and counts the number of 'ones'. The datetime and count are then stored in a .csv file and the bits collected are appended to a .bin file for cSontrol.

After a user-defined duration, the application will stop collecting, move the .csv and .bin files to an upload folder, and start collecting again. This process continues indefinitely.
### Requirements

- Python 3.x
- A Raspberry Pi with a TRNG device
- The following Python packages: **bitstring**, **python-dotenv**, **pyserial**, **boto3**.

### Setup

1. Install the required packages if they are not already installed: `pip install bitstring python-dotenv pyserial`

2. In the `vars` folder, edit the `variables.env` file to specify the sample size (in bits), the interval between samples, the duration for each data collection cycle, and the paths for the temporary and upload folders.

### Running the Application

To run the application, navigate to the folder containing the script and run the following command in the terminal:


>python main.py

The application will start reading data from the TRNG device at the specified interval, and it will write the count of 'ones' and the datetime to a .csv file and the bits to a .bin file in the temporary folder. After the specified duration, it will move all files in the temporary folder to the upload folder and start the next data collection cycle.