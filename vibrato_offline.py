import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
x, f_sample = sf.read('input.wav')
f_lfo = 5
depth = 100
n_samples = x.shape[0]
n = np.arange(n_samples)
lfo = depth * np.sin(2 * np.pi * f_lfo * n/f_sample)
if x.ndim == 1:
    print("Mono signal")
    n_new = n + lfo
    floor_idx = np.floor(n_new).astype(int)
    ceil_idx = np.ceil(n_new).astype(int)
    frac = n_new - floor_idx
    floor_idx = np.clip(floor_idx, 0, n_samples - 1)
    ceil_idx = np.clip(ceil_idx, 0, n_samples - 1)
    y = x[floor_idx] * (1 - frac) + x[ceil_idx] * frac
else:
    print("Stereo signal")
    y = np.zeros_like(x, dtype = float)
    for c in range(2):
        n_new = n + lfo
        floor_idx = np.floor(n_new).astype(int)
        ceil_idx = np.ceil(n_new).astype(int)
        frac = n_new - floor_idx
        floor_idx = np.clip(floor_idx, 0, n_samples  - 1)
        ceil_idx = np.clip(ceil_idx, 0, n_samples - 1)
        y[:, c] = x[floor_idx, c] * (1 - frac) + x[ceil_idx, c] * frac 
y = y / np.max(np.abs(y))
sf.write('output_vibrato.wav', (y * 32767).astype(np.int16), f_sample)
NFFT = 1024
noverlap = 512
plt.figure(figsize = (12, 16))
if x.ndim == 1:
    plt.subplot(2, 1, 1)
    plt.plot(n/f_sample, x, color = 'blue')
    plt.title("Original signal")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.subplot(2, 1, 2)
    plt.plot(n/f_sample, y, color = "orange")
    plt.title("Vibrato effect applied")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
else:
    plt.subplot(3, 1, 1)
    plt.plot(n/f_sample, x[:, 0], color = "blue", label = "left channel")
    plt.plot(n/f_sample, x[:, 1], color = "cyan", label = "right channel")
    plt.title("Original signal")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude");
    plt.legend()
    plt.subplot(3, 1, 2)
    plt.plot(n/f_sample, y[:, 0], color = "orange", label = "left channel")
    plt.plot(n/f_sample, y[:, 1], color = "yellow", label = "right channel")
    plt.title("Vibrato effect applied")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.legend()
plt.subplot(3, 1, 3)
plt.specgram(y[:, 0] if y.ndim == 2 else y, NFFT, f_sample, noverlap, cmap = "magma")
plt.title("Spectrogram")
plt.xlabel("Time(s)")
plt.ylabel("Frequency(Hz)")
plt.colorbar(label = "Amplitude")
plt.show()
    
