from fft import *


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
    # ser = config.serial_connection()
    ser = None

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
