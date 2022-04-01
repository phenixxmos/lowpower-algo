import numpy as np
import scipy.signal as spsig
import scipy.stats as spstat

class activity_detector:
    def __init__(self, block_size=240, block_count=10):
        self.block_size = block_size
        self.block_count = block_count
        self.time_domain_buffer = np.zeros(block_size * block_count)
        self.kurtosis_buffer = np.zeros(block_count)
        self.skewness_buffer = np.zeros(block_count)
        self.threshold = 1.0
    
    def process_frame(self, new_samples):
        # add the new samples to the buffer and shift along the old samples
        # this is UNTESTED and is probably wrong - maybe they should go the other way round?
        self.time_domain_buffer = np.concatenate((new_samples, self.time_domain_buffer[:-self.block_size]))

        new_kurtosis = spstat.kurtosis(self.time_domain_buffer)
        new_skewness = spstat.skewenss(self.time_domain_buffer)

        self.kurtosis_buffer = np.concatenate((new_kurtosis, self.kurtosis_buffer[:-1]))
        self.skewness_buffer = np.concatenate((new_skewness, self.skewness_buffer[:-1]))

        normality_test = np.mean(self.kurtosis_buffer - self.skewness_buffer**2.0)

        if normality_test > self.threshold:
            output = 1.0
        else:
            output = -1.0
        return output