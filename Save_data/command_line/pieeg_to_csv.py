"""
Record data from PiEEG-16 and write to CSV

"""

# imports
import numpy as np
from datetime import datetime
from time import sleep
import argparse

from utils import setup_pieeg16, get_voltage


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Record ephys data.')
    parser.add_argument('--fname', type=str, 
                        help='Output filename of ephys data ')
    parser.add_argument('--duration', type=int, default=600,
                        help='Duration of recording (seconds). Default is 600 seconds')
    parser.add_argument('--fs', type=int, default=10,
                        help='Sampling frequency of the data (Hz). Default is 10 Hz')
    parser.add_argument('--gain', type=int, default=1,
                        help='Gain of the data (1, 2, 4, 6, 8, 12, or 24). Default is 1')
    args = parser.parse_args()
    if args.fname is None:
        raise ValueError("Please input an output filename (--fname)")

    # setup GPIO device (PiEEG-16)
    print("\nSetting up recording device...")
    print(f"  Recording settings:")
    print(f"    Filename: {args.fname}")
    print(f"    Duration: {args.duration} seconds")
    print(f"    Sampling frequency: {args.fs} Hz")
    print(f"    Gain: {args.gain}")
    spi_1, spi_2, cs_line = setup_pieeg16(args.gain)

    # initialize csv file for recording data
    columns = "time,chan_1,chan_2,chan_3,chan_4,chan_5,chan_6,chan_7,chan_8,chan_9,chan_10,chan_11,chan_12,chan_13,chan_14,chan_15,chan_16\n"
    with open(args.fname, 'w') as f:
        f.write(columns)

    # start clock
    start_time = datetime.now()

    # record data
    print("\nRecording data...")
    for i_sample in range(args.duration*args.fs):
        # wait for sample time
        if (datetime.now()-start_time).total_seconds() < (i_sample/args.fs):
            sleep((i_sample/args.fs)-(datetime.now()-start_time).total_seconds())
        timepoint = (datetime.now()-start_time).total_seconds()

        # read data
        output_1=spi_1.readbytes(27)
        cs_line.set_value(0)
        output_2=spi_2.readbytes(27)
        cs_line.set_value(1)

        data = np.zeros(16)
        for a in range (3, 25, 3):
            data[int(a/3)-1] = get_voltage(output_1, a)
            data[int(a/3)+7] = get_voltage(output_2, a)

        # write data
        with open(args.fname, 'a') as f:
            f.write(f"{timepoint}, {data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}, {data[7]}, {data[8]}, {data[9]}, {data[10]}, {data[11]}, {data[12]}, {data[13]}, {data[14]}, {data[15]}\n")
            
    print(f"Data saved to {args.fname}")


if __name__ == "__main__":
    main()
