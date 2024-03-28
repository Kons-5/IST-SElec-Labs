import time, math, cmath
import gc

def dft(amplitudes):
    N = len(amplitudes)
    mag = [0.0] * N

    for k in range(N//2 - 1):
        real, imag = 0, 0

        for n in range(N):
             theta = -k * (2 * cmath.pi) * (float(n) / N)
             real += amplitudes[n] * cmath.cos(theta)
             imag += amplitudes[n] * cmath.sin(theta)

        magnitude = abs(complex(real, imag)) / N
        
        # Adjust magnitude for non-zero frequencies
        magnitude *= 2 if k != 0 else 1
        
        # Store magnitudes in pairs of two
        mag[2 * k] = magnitude
        mag[2 * k + 1] = magnitude

    return mag
    
def exp(p, q):  
    return cmath.exp((2.0 * cmath.pi * 1j * q) / p)

def fft(x):
    N = len(x)

    if N == 1:
        return x 
    else:
        X_even = fft(x[0:N:2])
        X_odd = fft(x[1:N:2])

        mag = [0.0] * N 
        for k in range(N//2):
            mag[k] = X_even[k] + exp(N, -k) * X_odd[k]
            mag[k + N // 2] = X_even[k] - exp(N, -k) * X_odd[k]

    return mag

def ifft(x):
    N = len(x)

    if N == 1:
        return x 
    else:
        X_even = ifft(x[0:N:2])
        X_odd = ifft(x[1:N:2])

        mag = [0.0] * N 
        for k in range(N//2):
            mag[k] = X_even[k] + exp(N, k) * X_odd[k]  # Conjugate twiddle factor
            mag[k + N // 2] = X_even[k] - exp(N, k) * X_odd[k]

        return mag  

def czt(x):
    n = len(x)
    m = n                             # Number of output points
    w = cmath.exp(-2j * cmath.pi / m) # Ratio between successive points on the spiral contour
    a = 1                             # Starting point on the Z-plane
      
    # Precompute chirp values
    chirp = [w**(i**2 / 2.0) for i in range(1 - n, max(n, m))]

    # Zero padding and preparation for FFTs
    N2 = int(2 ** math.ceil(math.log2(m + n - 1))) # Next power of 2

    dummy = chirp[n - 1 : n + n - 1]
    xp = [x[i] * a ** -i * dummy[i] for i in range(n)]
    xp = xp + [0.0] * (N2 - n)
    
    del dummy
    
    ichirpp = [1/i for i in chirp[: m + n - 1]]
    ichirpp = ichirpp + [0.0] * (N2 - (m + n - 1))
    
    # Calculate FFTs
    fft_xp = fft(xp)
    fft_ichirpp = fft(ichirpp)
   
    del xp, ichirpp
    gc.collect()
   
    # Convolution in frequency domain becomes a product
    k = [fft_xp[i] * fft_ichirpp[i] for i in range(N2)]
    r = ifft(k)
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
    
"""
for i in range(1, 20):
    arr=random.randint(100, size=(i * 100))
    start = timeit.default_timer()
    czt(arr)
    end = timeit.default_timer()
    print(str(end - start))
"""

if __name__ == '__main__':
    arr = [value for value in range(240)]
    
    # Chirp Z Transform
    czt(arr)
    
    """
    # Discrete Fourier Transform
    dft(arr)
    """