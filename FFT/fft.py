import pyaudio
import numpy as np


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
            p.terminate()
            print(f"Error opening audio stream: {e}")
            raise

    def serial_connection(
        self, serial_port: str = None, baud_rate: int = None, timeout: int = 1
    ):
        import serial

        if serial_port is None:
            serial_port = self.serial_port

        if baud_rate is None:
            baud_rate = self.baud_rate

        try:
            ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
            print(f"Connected with {serial_port}")
            return ser

        except serial.SerialException as e:
            print(f"Connection error: {e}")
        except KeyboardInterrupt:
            print("User interrupt.")


def normalize_equalizer(input, input_limit, result_limit):
    """
    Normalize bar heights to the range [0, limit_bars], scaling by amplitude_limit.
    Values are rounded up to the nearest integer.
    """
    from math import ceil

    result = input.copy()
    for i, value in enumerate(result):
        value = value * result_limit / input_limit
        if value > 1:  # reduce noise
            value = ceil(value)
        result[i] = value
    result = result.astype(np.int64)
    return result


def map_spectrum_to_equalizer(magnitude, spectrum, log_bins):
    """Map FFT magnitudes to equalizer bars with linear x-axis using interpolation."""
    bar_heights = np.zeros(len(log_bins) - 1)
    for i in range(len(log_bins) - 1):
        # Find FFT bins within the current log range
        start_idx = np.searchsorted(spectrum, log_bins[i])
        end_idx = np.searchsorted(spectrum, log_bins[i + 1])

        # If the range has data, calculate the max value
        if end_idx > start_idx:
            bar_heights[i] = np.max(magnitude[start_idx:end_idx])
        else:
            # Interpolate value for empty ranges
            bar_heights[i] = np.interp(
                (log_bins[i] + log_bins[i + 1])
                / 2,  # The center frequency of the interval
                spectrum,
                magnitude,
            )

    return bar_heights


def get_waveform(stream, chunk: int):
    data = stream.read(chunk, exception_on_overflow=False)
    data_np = np.frombuffer(data, dtype=np.int16)
    return data_np


def get_spectrum_magnitude(waveform_data, chunk: int):
    from numpy.fft import rfft

    magnitude = np.abs(rfft(waveform_data)) / (chunk / 2)
    return magnitude


def main() -> None:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import animation, colormaps

    matplotlib.use("TkAgg")  # to display in separate Tk window

    import time
    from tkinter import TclError

    # Configuration
    config = Config()
    p, stream = config.stream_audio()
    ser = config.serial_connection()
    # ser = None

    # Plot Setup
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(15, 10))
    waveform = np.arange(0, 2 * config.chunk, 2)  # samples (waveform)
    spectrum = np.linspace(
        0, config.rate // 2, config.chunk // 2 + 1
    )  # frequencies (spectrum)
    equalizer = np.arange(config.bars_num)  # Linear positions for the bars

    # Create line objects
    (waveform_line,) = ax1.plot(waveform, np.zeros(config.chunk), "-", lw=2)
    (spectrum_line,) = ax2.semilogx(
        spectrum, np.zeros(config.chunk // 2 + 1), "-", lw=2
    )
    equalizer_bar = ax3.bar(
        equalizer, np.zeros(config.bars_num), width=0.8, align="center", edgecolor="k"
    )

    # Format waveform axes
    ax1.set_title("Audio Waveform")
    ax1.set_xlabel("Samples")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlim(0, 2 * config.chunk)
    ax1.set_ylim(-config.amplitude_limit, config.amplitude_limit)

    # Format spectrum axes
    ax2.set_xscale("log")  # Logarithmic scale on X-axis
    ax2.set_title("Frequency Spectrum")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.set_xlim(config.freq_min, config.freq_max)
    ax2.set_ylim(0, config.amplitude_limit)

    # Format equalizer axes
    ax3.set_title("Equalizer")
    ax3.set_xlabel("Bars")
    ax3.set_ylabel("Amplitude")
    ax3.set_xlim(0, config.bars_num)
    ax3.set_ylim(0, config.bars_limit)

    # Assign colors to bars using a colormap
    cmap = colormaps["rainbow"].resampled(config.bars_num)
    colors = [cmap(i / (config.bars_num - 1)) for i in reversed(range(config.bars_num))]
    for bar, color in zip(equalizer_bar, colors):
        bar.set_color(color)

    # Precompute frequency ranges for the bars
    log_bins = np.logspace(
        np.log10(config.freq_min), np.log10(config.freq_max), config.bars_num + 1
    )  # Logarithmic bin edges

    # Figure layout
    fig.subplots_adjust(hspace=0.4)
    plt.tight_layout()

    # Counting FPS by mutable object
    frame_count = [0]

    def animate(i):
        """
        Update plot for animation
        based on mark's code:
        https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/spec_anim.py
        """
        try:
            # Read audio data
            waveform_data = get_waveform(stream, config.chunk)

            # Update waveform
            waveform_line.set_ydata(waveform_data)

            # Compute FFT and update spectrum
            spectrum_data = get_spectrum_magnitude(waveform_data, config.chunk)
            spectrum_line.set_ydata(spectrum_data)

            # Update equalizer bars
            bar_heights = map_spectrum_to_equalizer(spectrum_data, spectrum, log_bins)
            bar_heights = normalize_equalizer(
                bar_heights, config.amplitude_limit, config.bars_limit
            )

            if ser is not None:
                # Map values to INT and flip data
                data = ",".join(map(str, np.flip(bar_heights))) + "\n"
                ser.write(data.encode())

            for bar, height in zip(equalizer_bar.patches, bar_heights):
                bar.set_height(height)

            frame_count[0] += 1

            # Return the objects to update during animation
            return waveform_line, spectrum_line, *equalizer_bar.patches

        except TclError as e:
            print(f"TclError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    start_time = time.time()
    print(f"Stream started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create animate function using factory
    anim = animation.FuncAnimation(
        fig,
        animate,
        interval=10,
        blit=True,
        cache_frame_data=False,
    )

    # Start the visualization
    try:
        plt.show()
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Print frame count and FPS
        if frame_count[0] is not None:
            elapsed_time = time.time() - start_time
            print(
                f"Stream stopped. Average frame rate: {frame_count[0] / elapsed_time:.2f} FPS"
            )

        # Stop the audio stream
        if stream is not None:
            stream.stop_stream()
            stream.close()

        # Terminate PyAudio
        if p is not None:
            p.terminate()

        # Close the serial port if open
        if ser is not None and ser.is_open:
            ser.close()

        # Close the figure
        if fig is not None:
            plt.close(fig)


if __name__ == "__main__":
    main()
