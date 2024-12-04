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
import math
import serial

# Counts the frames
frame_count = 0


class Config:
    def __init__(
        self,
        chunk: int = 1024 * 2,  # Number of audio samples per frame for processing.
        format=pyaudio.paInt16,  # Audio format (16-bit integer, default for most audio applications).
        channels: int = 1,  # Number of audio channels (1 for mono, 2 for stereo).
        rate: int = 44100,  # Sample rate in Hz (common standard for audio, e.g., CD quality).
        amplitude_limit: int = 2048,  # Maximum amplitude value for visualization normalization.
        freq_min: int = 40,  # Minimum frequency in Hz for visualization (e.g., lowest note to display).
        freq_max: int = 14000,  # Maximum frequency in Hz for visualization (e.g., upper limit of audible range).
        bars_num: int = 144,  # Number of bars in the visualization equalizer.
        bars_limit: int = 255,  # Maximum height of a bar in the visualization (e.g., 8-bit LED range).
        serial_port: str = "COM6",  # Serial port for connecting to external hardware (e.g., LED controller).
        baud_rate: int = 115200,  # Baud rate for serial communication (default for many devices).
    ) -> None:
        # Audio settings
        self.chunk = chunk  # Number of audio samples processed at a time.
        self.format = format  # Format for PyAudio (defines how audio data is read).
        self.channels = channels  # Mono or stereo input.
        self.rate = rate  # Audio sampling rate in Hz.
        self.amplitude_limit = (
            amplitude_limit  # Upper bound for amplitude visualization.
        )

        # Frequency range for visualization
        self.freq_min = freq_min  # Lower bound of the frequency range displayed.
        self.freq_max = freq_max  # Upper bound of the frequency range displayed.

        # Visualization settings
        self.bars_num = bars_num  # Total number of bars in the equalizer visualization.
        self.bars_limit = bars_limit  # Maximum value for bar height normalization (e.g., LED intensity).

        # Serial connection settings
        self.serial_port = (
            serial_port  # Name of the serial port used for hardware communication.
        )
        self.baud_rate = baud_rate  # Speed of serial communication in bits per second.

    def stream_audio(self, input: bool = True, output: bool = False):
        try:
            p = pyaudio.PyAudio()  # Initialize PyAudio

            # Open audio stream
            stream = p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=input,
                output=output,
                frames_per_buffer=self.chunk,
            )
            return p, stream

        except Exception as e:
            print(f"Error opening audio stream: {e}")
            p.terminate()
            exit()


# ------------ Audio Setup ---------------
CHUNK = 1024 * 2  # samples per frame
FORMAT = pyaudio.paInt16  # audio format (16-bit integer)
CHANNELS = 1  # single channel for microphone
RATE = 44100  # samples per second
AMPLITUDE_LIMIT = 2048  # limiting amplitude

MIN_FREQ = 40
MAX_FREQ = 14000
N_BARS = 144  # Number of equalizer bars
LIMIT_BARS = 255

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

# Ustawienia portu szeregowego
SERIAL_PORT = "COM6"  # Zmień, jeśli COM5 jest inny
BAUD_RATE = 115200

try:
    # Otwórz połączenie szeregowe
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Połączono z {SERIAL_PORT}")

except serial.SerialException as e:
    print(f"Błąd połączenia: {e}")
except KeyboardInterrupt:
    print("Przerwano przez użytkownika.")

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
ax3.set_ylim(0, LIMIT_BARS)
ax3.set_title("Equalizer")
ax3.set_xlabel("Bars")
ax3.set_ylabel("Amplitude")


# Precompute frequency ranges for the bars
log_bins = np.logspace(
    np.log10(MIN_FREQ), np.log10(MAX_FREQ), N_BARS + 1
)  # Logarithmic bin edges


def normalize_bars(bar_heights):
    global LIMIT_BARS, AMPLITUDE_LIMIT
    """
    Normalize bar heights to the range [0, limit_bars], scaling by amplitude_limit.
    Values are rounded up to the nearest integer.
    """
    for i, value in enumerate(bar_heights):
        if bar_heights[i] < 1:
            bar_heights[i] = value * LIMIT_BARS / AMPLITUDE_LIMIT
        else:
            bar_heights[i] = math.ceil(value * LIMIT_BARS / AMPLITUDE_LIMIT)
    return bar_heights


def map_fft_to_linear_bars(magnitude, freq_bins, log_bins):
    global ser
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
    result = normalize_bars(bar_heights)

    # Mapowanie wartości na int i odwrócenie kolejności (np.flip)
    data = ",".join(map(str, map(int, np.flip(result)))) + "\n"

    # Wyślij dane przez Serial
    ser.write(data.encode())
    # print(f"Wysłano: {data.strip()}")
    return result


def on_close(evt):
    """Handle figure close event."""
    global frame_count, start_time, fig, ser
    frame_rate = frame_count / (time.time() - start_time)

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.close(fig)
    ser.close()

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


def main() -> None:
    start_time = time.time()
    print(f"Stream started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create the animation object with blit=True
    anim = animation.FuncAnimation(
        fig, animate, interval=10, blit=True, cache_frame_data=False
    )
    fig.canvas.mpl_connect("close_event", on_close)
    fig.subplots_adjust(hspace=0.4)
    plt.tight_layout()

    try:
        plt.show()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
        on_close()


if __name__ == "__main__":
    main()
