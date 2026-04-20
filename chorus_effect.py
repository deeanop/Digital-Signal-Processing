import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
x, f_sample = sf.read("input.wav")
n_samples = x.shape[0]
n = np.arange(n_samples)
delay_v1 = 15
delay_v2 = 22
delay_v3 = 18
delay_v4 = 27
sweep = 15
f_lfo1 = 0.3
f_lfo2 = 0.33
f_lfo3 = 0.36
f_lfo4 = 0.39
cross_spread = 0.4
mix_dry_wet = 0.7
time = n / f_sample
y = np.zeros_like(x)
if x.ndim == 1:
    print("Mono signal")
    delay1 = delay_v1 + sweep * np.sin(2 * np.pi * f_lfo1 * time)
    delay_samples1 = delay1 * f_sample / 1000
    delay2 = delay_v2 + sweep * np.sin(2 * np.pi * f_lfo2 * time + np.pi / 2)
    delay_samples2 = delay2 * f_sample / 1000
    for i in range(len(x)):
        d1 = delay_samples1[i]
        k1 = int(np.floor(d1))
        f1 = d1 - k1
        d2 = delay_samples2[i]
        k2 = int(np.floor(d2))
        f2 = d2 - k2
        if i - k1 - 1 < 0:
            delayed1 = 0
        else:
            delayed1 = (1 - f1) * x[i - k1 - 1] + f1 * x[i - k1]
        if i - k2 - 1 < 0:
            delayed2 = 0
        else:
            delayed2 = (1 - f2) * x[i - k2 - 1] + f2 * x[i - k2]
        y[i] = (1 - mix_dry_wet) * x[i] + mix_dry_wet * (delayed1 + delayed2)/2
    plt.figure(figsize = (16, 12))
    plt.plot(time, x, color = "red", label = "Original Signal")
    plt.plot(time, y, color = "green", label = "Chorus effect applied")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Chorus effect applied on mono signal")
    plt.legend()
    plt.show()
else:
    print("Stereo signal")
    delay_left1 = delay_v1 + sweep * np.sin(2 * np.pi * f_lfo1 * time)
    delay_samples_left1 = delay_left1 * f_sample / 1000
    delay_left2 = delay_v2 + sweep * np.sin(2 * np.pi * f_lfo2 * time + np.pi / 2)
    delay_samples_left2 = delay_left2 * f_sample / 1000
    delay_right1 = delay_v3 + sweep * np.sin(2 * np.pi * f_lfo3 * time + np.pi)
    delay_samples_right1 = delay_right1 * f_sample / 1000
    delay_right2 = delay_v4 + sweep * np.sin(2 * np.pi * f_lfo4 * time + 3 * np.pi / 2)
    delay_samples_right2 = delay_right2 * f_sample / 1000
    for i in range(len(x[:, 0])):
        d1 = delay_samples_left1[i]
        k1 = int(np.floor(d1))
        f1 = d1 - k1
        d2 = delay_samples_left2[i]
        k2 = int(np.floor(d2))
        f2 = d2 - k2
        d3 = delay_samples_right1[i]
        k3 = int(np.floor(d3))
        f3 = d3 - k3
        d4 = delay_samples_right2[i]
        k4 = int(np.floor(d4))
        f4 = d4 - k4
        if i - k1 - 1 < 0:
            delayed1 = 0
        else:
            delayed1 = (1 - f1) * x[i - k1 - 1, 0] + f1 * x[i - k1, 0]
        if i - k2 - 1 < 0:
            delayed2 = 0
        else:
            delayed2 = (1 - f2) * x[i - k2 - 1, 0] + f2 * x[i - k2, 0]
        if i - k3 - 1 < 0:
            delayed3 = 0
        else:
            delayed3 = (1 - f3) * x[i - k3 - 1, 1] + f3 * x[i - k3, 1]
        if i - k4 - 1 < 0:
            delayed4 = 0
        else:
            delayed4 = (1 - f4) * x[i - k4 - 1, 1] + f4 * x[i - k4, 1]
        y[i, 0] = (1 - mix_dry_wet) * x[i, 0] + mix_dry_wet * (delayed1 + delayed2)/2
        y[i, 1] = (1 - mix_dry_wet) * x[i, 1] + mix_dry_wet * (delayed3 + delayed4)/2
    y_left = y[:, 0].copy()
    y_right = y[:, 1].copy()
    y[:, 0] = (1 - cross_spread) * y_left + cross_spread * y_right
    y[:, 1] = (1 - cross_spread) * y_right + cross_spread * y_left
    plt.figure(figsize = (16, 12))
    plt.title("Chorus effect applied on stereo signal")
    plt.subplot(1, 2, 1)
    plt.plot(time, x[:, 0], color = "red", label = "Original Left Channel Signal")
    plt.plot(time, y[:, 0], color = "green", label = "Chorus effect applied on left channel")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(time, x[:, 1], color = "red", label = "Original Right Channel Signal")
    plt.plot(time, y[:, 1], color = "green", label = "Chorus effect applied on right channel")
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()
y = y / np.max(np.abs(y))
sf.write("output.wav", y, f_sample)    
    