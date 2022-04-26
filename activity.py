import numpy as np
import scipy.signal as spsig
import scipy.stats as spstat
from enum import Enum

ccir_16k_b=[2.2892,-1.0301,-1.4187,-0.20671,0.027113,-0.14509,0.076876,0.49515,-0.05634,-0.032802]
ccir_16k_a=[1,0.44781,-0.080789,-0.16007,-0.14565,-0.21476,-0.1661,0.046494,0.010907,0.0088031]

ccir_32k_b=[1.6216,-1.3253,-0.1814,0.33405,-0.54517,-0.021544,0.3011,-0.23395,-0.081136,0.34941,-0.44204,0.064593,0.15605,-0.03497,0.13075,0.029991,-0.12037]
ccir_32k_a=[1,-1.3374,1.4778,-1.0905,0.65639,-0.39374,0.33019,-0.33853,0.26515,-0.094816,-0.14693,0.16499,-0.15518,0.092042,0.015555,-0.010563,0.0073406]

ccir_48k_b=[0.59277,-0.64278,0.1597,0.010847,-0.0093632,0.045265,-0.14758,0.012525,0.034439,-0.025168,0.021699,-0.043273,-0.069614,0.13181,-0.038812,-0.076451,0.011089,0.019465,0.014415];
ccir_48k_a=[1,-3.1159,5.4642,-6.6845,6.5435,-5.4023,3.8997,-2.4889,1.4974,-0.93754,0.70747,-0.62996,0.48873,-0.15423,-0.21824,0.35243,-0.26741,0.11689,-0.026244];

class Detection(Enum):
            ACTIVITY=1
            BUFFERING=0
            PLACID=-1

class activity_detector:
    def __init__(self, block_size=240, block_count=10,Fs=16000):
        self.block_size = block_size
        self.block_count = block_count
        self.time_domain_buffer = np.zeros(self.block_size * self.block_count)
        self.threshold = 1.0
        self.samplerate = Fs
        self.block_tot=0
    
    def process_frame(self, new_samples):
        # add the new samples to the buffer and shift along the old samples
        # this is UNTESTED and is probably wrong - maybe they should go the other way round?
        self.time_domain_buffer = np.concatenate((new_samples, self.time_domain_buffer[:-self.block_size]))

        if self.block_tot >= self.block_count:
        
            if self.samplerate==16000:
                wieghted=spsig.lfilter(ccir_16k_b,ccir_16k_a,self.time_domain_buffer)
            elif self.samplerate==32000:
                wieghted=spsig.lfilter(ccir_32k_b,ccir_32k_a,self.time_domain_buffer)
            elif self.samplerate==48000:
                wieghted=spsig.lfilter(ccir_48k_b,ccir_48k_a,self.time_domain_buffer)
            else:
                print("Unsupported Samplerate.")
                #output = Detection.BUFFERING.value
                output = 0
                
            kurt = spstat.kurtosis(wieghted)
            skew = spstat.skew(wieghted)
            normality_test = kurt - skew**2.0

            if normality_test >= self.threshold:
                #output = Detection.ACTIVITY.value
                print("Activity Detected")
                output = 1
            else:
                #output = Detection.PLACID.value
                print("Placid Activity")
                output = -1

        else:
            #output = Detection.BUFFERING.value
            output = 0
        return output
        
    def increment_block(self):
        self.block_tot = self.block_tot + 1
        
            
        
