"""
pip install pyAudio may not work
Instead download and install a wheel from here:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

or use: 

pip install pipwin
pipwin install pyaudio
"""

# to display in separate Tk window
import matplotlib

matplotlib.use("TkAgg")

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

MIN_FREQ = 400
MAX_FREQ = 4000

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
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
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

ax2.set_xscale("log")  # Ustawienie logarytmicznej skali na osi X
ax2.set_xlim(MIN_FREQ, MAX_FREQ)  # Ustawienie zakresu od 400 Hz do 4000 Hz
# Format spectrum axes
ax2.set_title("Frequency Spectrum")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
# ax2.set_xlim(20, RATE // 2)
ax2.set_ylim(0, AMPLITUDE_LIMIT)


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
        magnitude = np.abs(rfft(data_np)) / (CHUNK / 2)  # Now returns 1025 samples
        line_fft.set_ydata(magnitude)

        frame_count += 1

        # Return the objects to update during animation
        return line, line_fft

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
    try:
        plt.show()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
        on_close()
