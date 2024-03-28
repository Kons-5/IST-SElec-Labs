#!/usr/bin/env python3
import sys, T_Display, cmath, math, gc

# Global variables
tft = T_Display.TFT()      # TFT display interface
width = 240                # Max width (px)
height = 135               # Max height (px)
x_div = 10                 # Number of horizontal divisions
x_range = [5, 10, 20, 50]  # Time scale (ms)
x_range_index = 0          # Time scale starting index
y_div = 6                  # Number of vertical divisions
y_range = [1, 2, 5, 10]    # Amplitude scale (V)
y_range_index = 1          # Amplitude scale starting index

# uOscilloscope class definition
class uOscilloscope:
    """
    This class represents a digital oscilloscope and provides essential functions for interacting with an IoT display. Here's what it can do:
    - Data Acquisition: Samples and processes analog signals from an ADC.
    - Display and Visualization: Renders signal waveforms on an IoT display, including grid overlays and time/amplitude labels.
    - Signal Analysis: Calculates essential signal statistics (maximum, minimum, average, and RMS values).
    - Data Export: Sends measurement summaries and signal data via email.
    - Scale Adjustments: Provides controls to modify the X-axis (time) and Y-axis (amplitude) scales for optimal visualization.
    - Frequency Analysis: Performs Discrete Fourier Transform (DFT) or Fast Fourier Transform (FFT) to display frequency domain representation. 
    """
    def __init__(self):
        # Init IoT display for the first time
        self.time_display()

    def current_function(self):
        if self.function_flag == "time":
            self.time_display()
        elif self.function_flag == "freq":
            self.freq_display()

    def read_samples(self):
        self.samples = tft.read_adc(240, x_range[x_range_index] * x_div)
        
        if sys.implementation.name == "micropython":
            convert_sample = lambda sample: 0.012049 * sample - 24.059 # IoT 0003.03
        else:
            convert_sample = lambda sample: 0.0129 * sample - 26.62 # Simulator
            
        self.amplitudes = [convert_sample(sample) for sample in self.samples]

    def signal_metrics(self):
        self.max, self.min = max(self.amplitudes), min(self.amplitudes)
        self.avg = sum(self.amplitudes) / len(self.amplitudes)
        self.rms = (sum(value ** 2 for value in self.amplitudes) / len(self.amplitudes)) ** 0.5

    def estimate_frequency(self):
        """
        Estimate frequency by counting zero crossings. Works well for long low-noise sines, square, triangle, etc
        """
        fs = 240 * 1000/(x_range[x_range_index] * x_div)
        
        # Remove the DC offset from the signal
        self.avg = sum(self.amplitudes) / len(self.amplitudes)
        x = [value - self.avg for value in self.amplitudes]
        
        # Detect both rising and falling edges
        indices = []
        for i in range(1, len(x)):
            if (x[i] >= 0 and x[i-1] < 0) or (x[i] <= 0 and x[i-1] > 0):
                indices.append(i)

        if len(indices) < 2:
            return 0  # Not enough edges to determine frequency

        # Linear interpolation to find intersample
        crossings = [i - x[i] / (x[i] - x[i-1]) for i in indices[:-1]]
        
        diff = []
        previous = None
        for value in crossings: 
            if previous is not None:
                diff.append(value - previous)
            previous = value
        
        # Check for empty diff array
        if not diff:
            return 0 # No valid frequency calculation possible
        
        return fs / (2 * sum(diff) / len(diff))

    def clear_display(self):
        tft.display_set(tft.BLACK, 0, 0, width, height)                             # Erase display
        tft.set_wifi_icon(width - 16, height - 16)                                  # Set wifi icon

        if self.function_flag == "time":
            tft.display_write_grid(0, 0, width, height - 16, x_div, y_div, True)    # Set grid

            estimated_freq = round(self.estimate_frequency())

            formated_strings = [
                (f"{y_range[y_range_index]:02d}V/", 0),
                (f"{x_range[x_range_index]:02d}ms/", 45),
                (f"f={estimated_freq:03d} Hz", 100)
            ]
            
            # Print scales and signal frequency
            for text, x_pos in formated_strings:
                tft.display_write_str(tft.Arial16, text, x_pos, height - 16)

            # Print signal out of range error
            if (max(abs(value) for value in self.amplitudes) > y_range[y_range_index] * y_div / 2):
                tft.display_write_str(tft.Arial16, "scale", 175, height - 16, tft.RED)
            
        elif self.function_flag == "freq":
            tft.display_write_grid(0, 0, width, height - 16, x_div, y_div, False)   # Set grid

            formated_strings = [
                (f"{y_range[y_range_index]/2:.1f}V/", 0),
                (f"{round(1200/(x_range[x_range_index])):03d}Hz/", 50)
            ]
            
            # Print scales
            for text, x_pos in formated_strings:
                tft.display_write_str(tft.Arial16, text, x_pos, height - 16)
            
            # Print signal out of range error
            if (max(value for value in self.magnitudes) > y_range[y_range_index] * y_div / 2):
                tft.display_write_str(tft.Arial16, "scale", 175, height - 16, tft.RED)

    def time_display(self):
        x, y = [], []
        self.function_flag = "time"
        
        # Sampling and converting to the right range
        self.read_samples()
        
        # Plot sampled values in the current X and Y scale
        y_div_factor = y_range[y_range_index] * y_div / (height - 16)
        x = list(range(len(self.amplitudes)))
        y = [
            round(max(0, min((height - 16) / 2 + value / y_div_factor, height - 16)))
            for value in self.amplitudes
        ]
        
        # Clear the display and print the plot
        self.clear_display()
        tft.display_nline(tft.YELLOW, x, y) # Display the plot

    def send_email(self):
        # Sampling and converting to the right range
        self.read_samples()
    
        # Sample period and calculations on the sampled values
        fs = 240 * 1000 / (x_range[x_range_index] * x_div)
        estimated_freq = self.estimate_frequency()
        self.signal_metrics()
        
        # Message formatting
        stats = [self.max, self.min, self.avg, self.rms, estimated_freq]
        labels = ["Vmax", "Vmin", "Vavg", "rms", "\nEstimated Freq"]
        message = ", ".join(f"{label}: {value:.2f}" for label, value in zip(labels, stats))
        
        names = ["jrazevedogoncalves", "maria.teresa.ramos.nogueira", "tatianadelgado"]
        emails = ",".join(f"{name}@tecnico.ulisboa.pt" for name in names)
        
        tft.send_mail(1 / fs, self.amplitudes, message, emails)

    def write_to_display(self):
        # Erase display and set wifi icon
        tft.display_set(tft.BLACK, 0, 0, width, height)
        tft.set_wifi_icon(width - 16, height - 16)

        # Sampling and converting to the right range
        self.read_samples()

        # Calculations on the sampled values
        self.signal_metrics()
        estimated_freq = self.estimate_frequency()

        # Define data for display
        formated_strings = [
            (f"Vmax = {self.max:.2f}", 105),
            (f"Vmin = {self.min:.2f}", 75),
            (f"Vavg = {self.avg:.2f}", 45),
            (f"Vrms = {self.rms:.2f}", 15)
        ]

        # Iterate through data and display it
        for text, y_pos in formated_strings:
            tft.display_write_str(tft.Arial16, text, 20, y_pos)

        tft.display_write_str(tft.Arial16, f"f = {estimated_freq:.2f} Hz", 130, 15)

    def change_x_scale(self):
        global x_range_index
        x_range_index = x_range_index + 1
        if x_range_index == len(x_range):
            x_range_index = 0
        self.current_function()
    
    def change_y_scale(self):
        global y_range_index
        y_range_index = y_range_index + 1
        if y_range_index == len(y_range):
            y_range_index = 0
        self.current_function()

    def dft(self):
        """
        Calculates the DFT of a signal. This implementation directly computes the DFT formula:
        X[k] = sum_{n=0}^{N-1} x[n] * exp(-j * 2 * pi * k * n / N)
        """
        N = len(self.amplitudes)
        mag = [0.0] * N

        for k in range(N//2 - 1):
            real, imag = 0, 0

            for n in range(N):
                 theta = -k * (2 * cmath.pi) * (float(n) / N)
                 real += self.amplitudes[n] * cmath.cos(theta)
                 imag += self.amplitudes[n] * cmath.sin(theta)

            magnitude = abs(complex(real, imag)) / N
            
            # Adjust magnitude for non-zero frequencies
            magnitude *= 2 if k != 0 else 1
            
            # Store magnitudes in pairs of two
            mag[2 * k] = magnitude
            mag[2 * k + 1] = magnitude

        return mag

    def exp(self, p, q):  
        return cmath.exp((2.0 * cmath.pi * 1j * q) / p)

    def fft(self, x):
        """
        A recursive implementation of the 1D Cooley-Tukey FFT, the input should have a length of power of 2. 
        """
        N = len(x)
 
        if N == 1:
            return x 
        else:
            X_even = self.fft(x[0:N:2])
            X_odd = self.fft(x[1:N:2])

            mag = [0.0] * N 
            for k in range(N//2):
                mag[k] = X_even[k] + self.exp(N, -k) * X_odd[k]
                mag[k + N // 2] = X_even[k] - self.exp(N, -k) * X_odd[k]

        return mag
	
    def ifft(self, x):
        """
        Implements the 1D Inverse Fast Fourier Transform (IFFT). The input should have a length of power of 2.
        """
        N = len(x)

        if N == 1:
            return x 
        else:
            X_even = self.ifft(x[0:N:2])
            X_odd = self.ifft(x[1:N:2])

            mag = [0.0] * N 
            for k in range(N//2):
                mag[k] = X_even[k] + self.exp(N, k) * X_odd[k]  # Conjugate twiddle factor
                mag[k + N // 2] = X_even[k] - self.exp(N, k) * X_odd[k]

            return mag  

    def czt(self):
        """
        Calculates the Chirp Z-Transform.
        """
        n = len(self.amplitudes)
        m = n                             # Number of output points
        w = cmath.exp(-2j * cmath.pi / m) # Ratio between successive points on the spiral contour
        a = 1                             # Starting point on the Z-plane
          
        # Precompute chirp values
        chirp = [w**(i**2 / 2.0) for i in range(1 - n, max(n, m))]

        # Zero padding and preparation for FFTs
        N2 = int(2 ** math.ceil(math.log2(m + n - 1))) # Next power of 2

        dummy = chirp[n - 1 : n + n - 1]
        xp = [self.amplitudes[i] * a ** -i * dummy[i] for i in range(n)]
        xp = xp + [0.0] * (N2 - n)
        
        del dummy
        
        ichirpp = [1/i for i in chirp[: m + n - 1]]
        ichirpp = ichirpp + [0.0] * (N2 - (m + n - 1))
        
        # Calculate FFTs
        fft_xp = self.fft(xp)
        fft_ichirpp = self.fft(ichirpp)
       
        del xp, ichirpp
        gc.collect()
       
        # Convolution in frequency domain becomes a product
        k = [fft_xp[i] * fft_ichirpp[i] for i in range(N2)]
        r = self.ifft(k)
        r = [v / len(r) for v in r]
        r = r[n - 1 : m + n - 1]

        del k, fft_xp, fft_ichirpp
        gc.collect()

        # Scale and adjust phase based on chirp
        chirp = chirp[n - 1 : m + n - 1]
        result = [r[i] * chirp[i] for i in range(len(r) // 2)]
        
        del chirp
        gc.collect()
        
        # Grouping values two by two
        final = [0.0] * 2 * len(result)
        for i in range(m // 2):
            final[2 * i] = result[i]
            final[2 * i + 1] = final[2 * i]

        # Amplitude scaling and normalization
        final = [abs(value) / len(final) for value in final]
        for i in range(len(final)):
            final[i] *= 2 if i>1 else 1
        
        return final
    
    def freq_display(self):
        x, y = [], []
        self.function_flag = "freq"

        # Sampling and converting to the right range
        self.read_samples()
        
        # Method to calculate the frequency domain representation of the signal
        method = "fft"
        if method == "dft":
            self.magnitudes = self.dft()
        elif method == "fft": 
            self.magnitudes = self.czt()

        # Display the frequency representation in the current scales
        y_div_factor = (y_range[y_range_index] * y_div) / (2 * (height - 16))
        x = list(range(len(self.magnitudes)))
        y = [
            round(max(0, min(value / y_div_factor, height - 16)))
            for value in self.magnitudes
        ]

        # Clear the display and print the plot
        self.clear_display()
        tft.display_nline(tft.MAGENTA, x, y)

if __name__ == "__main__":
    # Create an instance of the uOscilloscope object
    osc = uOscilloscope()

    # Main loop
    while tft.working():
        button = tft.readButton()
        if button != tft.NOTHING:
            print("Button pressed:", button)
            if button == 11:                    # Fast click button 1
                osc.time_display()
            elif button == 12:                  # Long click button 1
                osc.send_email()
            elif button == 13:                  # Double click button 1
                osc.write_to_display()
            elif button == 21:                  # Fast click button 2
                osc.change_x_scale()
            elif button == 22:                  # Long click button 2
                osc.change_y_scale()
            elif button == 23:                  # Double click button 2
                osc.freq_display()
            else: print("Invalid button key")
