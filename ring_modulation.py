import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
x, f_sample = sf.read('input.wav')
f_carrier = 10000
n_samples = x.shape[0]
n = np.arange(n_samples)
if x.ndim == 1:
    print("Mono signal")
    y = np.zeros_like(x, dtype = 'float')
    for i in range(0, len(x)):
        y[i] = x[i] * np.cos(2 * np.pi * f_carrier * (i / f_sample))
    y = y / np.max(np.abs(y))
    plt.figure(figsize = (12, 16))
    plt.plot(n / f_sample, x, color = 'red')
    plt.plot(n / f_sample, y, color = 'green')
    plt.xlabel("Time[s]")
    plt.ylabel("Amplitude[dB]")
    plt.show()
elif x.ndim == 2:
    print("Stereo signal")
    y = np.zeros_like(x)
    for c in range(2):
        for i in range(0, len(x)):
            y[i, c] = x[i, c] * np.cos(2 * np.pi * f_carrier * (i / f_sample))
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
sf.write('output_ring.wav', y, f_sample)