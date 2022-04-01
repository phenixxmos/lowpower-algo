# Copyright 2018-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import numpy as np
import scipy.io.wavfile
import argparse
import activity

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs='?', help="wav file to process", default='input.wav')
    parser.add_argument("output", nargs='?', help="output of activity detection", default='output.wav')
    parser.add_argument("block_size", nargs='?', help="number of samples in a block", default=240)
    parser.add_argument("block_count", nargs='?', help="number of blocks to use", default=10)
    parser.parse_args()
    args = parser.parse_args()
    return args


def test_data(input_data, block_size=240, block_count=10):

    file_length = len(input_data)
    output = np.zeros(file_length)

    act_det = activity.activity_detector(block_size, block_count)

    for frame_start in range(0, file_length-block_size*2, block_size):
        input_frame = input_data[frame_start:frame_start+block_size] # get a frames worth of data out of the array

        current_output = act_det.process_frame(input_frame)

        output[frame_start: frame_start + block_size] = current_output

    return output


def test_file(input_file, output_file, block_size=240, block_count=10):

    input_rate, input_wav_file = scipy.io.wavfile.read(input_file, 'r')
    input_wav_data = input_wav_file[:, 0] # grab the first channel

    output = test_data(input_wav_data, block_size, block_count)

    scipy.io.wavfile.write(output_file, input_rate)


if __name__ == "__main__":
    #The number of samples of data in the frame

    args = parse_arguments()
    test_file(args.input, args.output, args.block_size, args.block_count)
