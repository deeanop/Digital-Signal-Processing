import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
x, f_sample = sf.read('input.wav')
delay = int(0.2 * f_sample)
alpha = 0.7
n_samples = x.shape[0]
n = np.arange(n_samples)
if x.ndim == 1:
    print("Mono signal")
    y = np.zeros_like(x, dtye = 'float')
    for i in range(0, len(x)):
        if i >= delay:
            y[i] = x[i] + alpha * x[i - delay]
        else:
            y[i] = x[i]    
    y = y / np.max(np.abs(y))
    plt.figure(figsize = (12, 16))
    plt.subplot(2, 1, 1)
    plt.plot(n / f_sample, x, color = 'red')
    plt.title("Original signal")
    plt.xlabel("Time[s]")
    plt.ylabel("Amplitude[dB]")
    plt.subplot(2, 1, 2)
    plt.plot(n / f_sample, y, color = 'green')
    plt.title("Echo effect applied")
    plt.xlabel("Time[s]")
    plt.ylabel("Amplitude[dB]")
    plt.show()
elif x.ndim == 2:
    print("Stereo signal")
    y = np.zeros_like(x, dtype = 'float')
    for c in range(2):
        for i in range(0, len(x)):
            if i >= delay:
                y[i, c] = x[i, c] + alpha * x[i - delay, c]
            else:
                y[i, c] = x[i, c]
    y = y / np.max(np.abs(y))
    plt.figure(figsize = (12, 16))
    plt.subplot(2, 1, 1)
    plt.plot(n / f_sample, x[:, 0], color = 'blue')
    plt.plot(n / f_sample, y[:, 0], color = 'yellow')
    plt.title("Left channel")
    plt.xlabel("Time[s]")
    plt.ylabel("Amplitude[dB]")
    plt.subplot(2, 1, 2)
    plt.plot(n / f_sample, x[:, 1], color = 'yellow')
    plt.plot(n / f_sample, y[:, 1], color = 'blue')
    plt.title("Right channel")
    plt.xlabel("Time[s]")
    plt.ylabel("Amplitude[dB]")
    plt.show()
sf.write('output_echo.wav', y, f_sample)
    
