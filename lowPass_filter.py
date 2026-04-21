import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
x, f_sample = sf.read('input.wav')
f_cutoff = 100
if x.ndim == 1:
    print("Mono signal")
    X = np.fft.fft(x)
    frequencies = np.fft.fftfreq(len(x), 1 / f_sample)
    mask = np.abs(frequencies) <= f_cutoff
    X_filtered = X * mask
    y = np.fft.ifft(X_filtered)
    y = np.real(y)
    y = y / np.max(np.abs(y))
    plt.figure(figsize = (10, 4))
    plt.specgram(y, NFFT = 1024, Fs = f_sample, noverlap = 512, cmap = 'plasma')
    plt.title("Mono signal spectrogram")
    plt.xlabel("Time[s]")
    plt.ylabel("Frequency[Hz]")
    plt.colorbar(label = "Amplitude[dB]")
    plt.show()
elif x.ndim == 2:
    print("Stereo signal")
    y = np.zeros_like(x)
    X_left = np.fft.fft(x[:, 0])
    frequencies_left = np.fft.fftfreq(len(x[:, 0]), 1 / f_sample)
    mask_left = np.abs(frequencies_left) <= f_cutoff
    X_left_filtered = X_left * mask_left 
    X_right = np.fft.fft(x[:, 1])
    frequencies_right = np.fft.fftfreq(len(x[:, 1]), 1 / f_sample)
    mask_right = np.abs(frequencies_right) <= f_cutoff
    X_right_filtered = X_right * mask_right
    y_left = np.fft.ifft(X_left_filtered)
    y_left = np.real(y_left)
    y_right = np.fft.ifft(X_right_filtered)
    y_right = np.real(y_right)
    y[:, 0] = y_left
    y[:, 1] = y_right
    y = y / np.max(np.abs(y))
    plt.figure(figsize = (10, 4))
    plt.subplot(1, 2, 1)
    plt.specgram(y[:, 0], NFFT = 1024, Fs = f_sample, noverlap = 512, cmap = 'hot')
    plt.title("Stereo signal spectrogram (left)")
    plt.xlabel("Time[s]")
    plt.ylabel("Frequency[Hz]")
    plt.colorbar(label = "Amplitude[dB]")
    plt.subplot(1, 2, 2)
    plt.specgram(y[:, 1], NFFT = 1024, Fs = f_sample, noverlap = 512, cmap = 'spring')
    plt.title("Stereo signal spectrogram (right)")
    plt.xlabel("Time[s]")
    plt.ylabel("Frequency[Hz]")
    plt.colorbar(label = "Amplitude[dB]")
    plt.show()
sf.write('output_lowPass.wav', y, f_sample)
