"""
based on mark's code:
https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/spec_anim.py
"""

import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as mcolors

matplotlib.use("TkAgg")  # to display in separate Tk window

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from numpy.fft import rfft
import time
from tkinter import TclError

# Counts the frames
frame_count = 0

# ------------ Audio Setup ---------------
CHUNK = 1024 * 2  # samples per frame
FORMAT = pyaudio.paInt16  # audio format (16-bit integer)
CHANNELS = 1  # single channel for microphone
RATE = 44100  # samples per second
AMPLITUDE_LIMIT = 2048  # limiting amplitude

MIN_FREQ = 40
MAX_FREQ = 14000
N_BARS = 144  # Number of equalizer bars

# Initialize PyAudio
p = pyaudio.PyAudio()

try:
    # Open audio stream
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=False,
        frames_per_buffer=CHUNK,
    )
except Exception as e:
    print(f"Error opening audio stream: {e}")
    p.terminate()
    exit()

# ------------ Plot Setup ---------------
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(15, 10))
x = np.arange(0, 2 * CHUNK, 2)  # samples (waveform)
xf = np.linspace(0, RATE // 2, CHUNK // 2 + 1)  # frequencies (spectrum)

# Create line objects
(line,) = ax1.plot(x, np.zeros(CHUNK), "-", lw=2)
(line_fft,) = ax2.semilogx(xf, np.zeros(CHUNK // 2 + 1), "-", lw=2)

# Format waveform axes
ax1.set_title("Audio Waveform")
ax1.set_xlabel("Samples")
ax1.set_ylabel("Amplitude")
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax1.set_xlim(0, 2 * CHUNK)

ax2.set_xscale("log")  # Logarithmic scale on X-axis
ax2.set_xlim(MIN_FREQ, MAX_FREQ)
ax2.set_title("Frequency Spectrum")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
ax2.set_ylim(0, AMPLITUDE_LIMIT)

# Equalizer setup
bar_positions = np.arange(N_BARS)  # Linear positions for the bars
bars = ax3.bar(
    bar_positions, np.zeros(N_BARS), width=0.8, align="center", edgecolor="k"
)

# Assign colors to bars using a colormap
cmap = cm.get_cmap("rainbow", N_BARS)  # Tęczowy gradient
colors = [cmap(i) for i in reversed(range(N_BARS))]
for bar, color in zip(bars, colors):
    bar.set_color(color)

ax3.set_xlim(0, N_BARS)
ax3.set_ylim(0, AMPLITUDE_LIMIT)
ax3.set_title("Equalizer")
ax3.set_xlabel("Bars")
ax3.set_ylabel("Amplitude")


# Precompute frequency ranges for the bars
log_bins = np.logspace(
    np.log10(MIN_FREQ), np.log10(MAX_FREQ), N_BARS + 1
)  # Logarithmic bin edges


def map_fft_to_linear_bars(magnitude, freq_bins, log_bins):
    """Map FFT magnitudes to equalizer bars with linear x-axis using interpolation."""
    bar_heights = np.zeros(len(log_bins) - 1)
    for i in range(len(log_bins) - 1):
        # Find FFT bins within the current log range
        start_idx = np.searchsorted(freq_bins, log_bins[i])
        end_idx = np.searchsorted(freq_bins, log_bins[i + 1])

        # If the range has data, calculate the max value
        if end_idx > start_idx:
            bar_heights[i] = np.max(magnitude[start_idx:end_idx])
        else:
            # Interpolate value for empty ranges
            bar_heights[i] = np.interp(
                (log_bins[i] + log_bins[i + 1])
                / 2,  # The center frequency of the interval
                freq_bins,
                magnitude,
            )
    return bar_heights


def on_close(evt):
    """Handle figure close event."""
    global frame_count, start_time, fig
    frame_rate = frame_count / (time.time() - start_time)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.close(fig)

    print("Stream stopped")
    print(f"Average frame rate: {frame_rate:.2f} FPS")
    quit()


def animate(i):
    """Update plot for animation."""
    global frame_count

    try:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        data_np = np.frombuffer(data, dtype=np.int16)

        # Update waveform
        line.set_ydata(data_np)

        # Compute FFT and update spectrum
        magnitude = np.abs(rfft(data_np)) / (CHUNK / 2)
        line_fft.set_ydata(magnitude)

        # Update equalizer bars
        bar_heights = map_fft_to_linear_bars(magnitude, xf, log_bins)
        for bar, height in zip(bars, bar_heights):
            bar.set_height(height)

        frame_count += 1

        return line, line_fft, *bars

    except TclError as e:
        print(f"TclError: {e}")
        on_close(None)

    except Exception as e:
        print(f"Unexpected error: {e}")
        on_close(None)


if __name__ == "__main__":
    start_time = time.time()
    print(f"Stream started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create the animation object with blit=True
    anim = animation.FuncAnimation(
        fig, animate, interval=20, blit=True, cache_frame_data=False
    )
    fig.canvas.mpl_connect("close_event", on_close)
    fig.subplots_adjust(hspace=0.4)
    plt.tight_layout()

    try:
        plt.show()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
        on_close()
