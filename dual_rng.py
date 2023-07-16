import os
import sup_mod as sm

# change to script directory
script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path)


def main():
    num_bits, interval, sample_duration, temp_folder, upload_folder, fold = sm.load_environment_variables()
    sm.check_and_create_folders(temp_folder, upload_folder)
    print("Searching for TrueRng device...\n")
    chk_bitb = sm.check_bitb()
    chk_trng = sm.check_trng()
    if chk_bitb == False and chk_trng == None:
        print('No RNG device found. Exiting.')
        return
    elif chk_bitb == True:
        print('Using bitbbabler as RNG device.')
        device = 'bitb'
        filename_base = sm.get_filename(num_bits, interval, device, fold)
        sm.collect_bitb(device, temp_folder, upload_folder, filename_base, num_bits, interval, sample_duration, fold)
    else:
        print('Using TrueRNG as RNG device.')
        device = 'trng'
        filename_base = sm.get_filename(num_bits, interval, device, fold)
        rng = sm.setup_serial(chk_trng)
        sm.collect_trng(device, temp_folder, upload_folder, filename_base, num_bits, interval, sample_duration, rng)


# Run the main function
if __name__ == '__main__':
    main()


