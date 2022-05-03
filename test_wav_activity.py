# Copyright 2018-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
import numpy as np
import scipy.io.wavfile
import argparse
import activity
from enum import Enum

#this expects stero input
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs='?', help="wav file to process", default='input.wav')
    parser.add_argument("output", nargs='?', help="output of activity detection", default='output.wav')
    parser.add_argument("block_size", nargs='?',type=int, help="number of samples in a block", default=240)
    parser.add_argument("buffer_count",nargs='?',type=int,help="the number of frames to use for the time buffer",default=334)
    parser.parse_args()
    args = parser.parse_args()
    return args
"""
input_data - audio data samples
filel - length of the input file
block_size - the size of a processing box
buffer_count - the number of buffer periods to use
"""

def test_data(input_data, block_size=240, buffer_count=334,fs=16000):

    file_length = len(input_data)
    output = np.zeros(file_length)

    act_det = activity.activity_detector(block_size, buffer_count,fs)

    for frame_start in range(0, file_length-block_size*2, block_size):
        input_frame = input_data[frame_start:frame_start+block_size] # get a frames worth of data out of the array

        current_output = act_det.process_frame(input_frame)
        act_det.increment_block()
        output[frame_start: frame_start + block_size] = current_output

    return output


def test_file(input_file, output_file, block_size=240, buffer_count=334):

    input_rate, input_wav_file = scipy.io.wavfile.read(input_file, 'r')
    if input_wav_file.ndim>1:
        input_wav_data = input_wav_file[:, 0] # grab the first channel

    output = test_data(input_wav_data, block_size, buffer_count,input_rate)

    scipy.io.wavfile.write(output_file, input_rate,output)


if __name__ == "__main__":
    #The number of samples of data in the frame

    args = parse_arguments()
    test_file(args.input, args.output, args.block_size, args.buffer_count)
