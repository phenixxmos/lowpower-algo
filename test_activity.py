import numpy as np
from run_wav_activity import run_data

def test_white_noise():
    fs = 16000
    T = 3.0
    N = int(fs * T)

    x = np.random.randn(N)
    y = run_data(x)
    assert x.shape[0] == y.shape[0]
