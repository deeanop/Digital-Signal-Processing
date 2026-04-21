import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
x, f_sample = sf.read('input.wav')
k = 8 #sample value kept for k steps
b = 4 #possible values of a sample amplitude
q = 2 ** (b - 1)
n_samples = x.shape[0]
n = np.arange(n_samples)
operation = int(input("Choose an operation: \n1. Bit Depth Reduction \n2. Downsampling"))
if operation == 1:
    if x.ndim == 1:
        y = np.zeros_like(x)
        for i in range(0, len(x)):
            y[i] = np.round(x[i] * q) / q
        y = y / np.max(np.abs(y))
        plt.figure(figsize = (12, 16))
        plt.plot(n / f_sample, x, color = 'red')
        plt.plot(n / f_sample, y, color = 'green')
        plt.title("Bit Depth Reduction")
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[dB]")
        plt.show()
    elif x.ndim == 2:
        y = np.zeros_like(x)
        for c in range(2):
            for i in range(0, len(x)):
                y[i, c] = np.round(x[i, c] * q) / q
        y = y / np.max(np.abs(y))
        plt.figure(figsize = (12, 16))
        plt.subplot(2, 1, 1)
        plt.plot(n / f_sample, x[:, 0], color = 'red')
        plt.plot(n / f_sample, y[:, 0], color = 'green')
        plt.title("Left channel")
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[dB]")
        plt.subplot(2, 1, 2)
        plt.plot(n / f_sample, x[:, 1], color = 'blue')
        plt.plot(n / f_sample, y[:, 1], color = 'yellow')
        plt.title("Right channel")
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[dB]")
        plt.show()
    sf.write('output_bitcrusher.wav', y, f_sample)
elif operation == 2:
    if x.ndim == 1:
        y = np.zeros_like(x)
        for i in range(0, len(x)):
            y[i] = x[i - i % k]
        y = y / np.max(np.abs(y))
        plt.figure(figsize = (12, 16))
        plt.plot(n / f_sample, x, color = 'red')
        plt.plot(n / f_sample, y, color = 'green')
        plt.title("Downsampling")
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[dB]")
        plt.show()
    elif x.ndim == 2:
        y = np.zeros_like(x)
        for c in range(2):
            for i in range(0, len(x)):
                y[i, c] = x[i - i % k, c]
        y = y / np.max(np.abs(y))
        plt.figure(figsize = (12, 16))
        plt.subplot(2, 1, 1)
        plt.plot(n / f_sample, x[:, 0], color = 'red')
        plt.plot(n / f_sample, y[:, 0], color = 'green')
        plt.title("Left channel")
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[dB]")
        plt.subplot(2, 1, 2)
        plt.plot(n / f_sample, x[:, 1], color = 'blue')
        plt.plot(n / f_sample, y[:, 1], color = 'yellow')
        plt.title("Right channel")
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[dB]")
        plt.show()
    sf.write('output_bitcrusher.wav', y, f_sample)
