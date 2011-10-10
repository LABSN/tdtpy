import re

def ispow2(n):
    '''
    True if n is a power of 2, False otherwise

    >>> ispow2(5)
    False
    >>> ispow2(4)
    True
    '''
    return (n & (n-1)) == 0

def nextpow2(n):
    '''
    Given n, return the nearest power of two that is >= n

    >>> nextpow2(1)
    1
    >>> nextpow2(2)
    2
    >>> nextpow2(5)
    8
    >>> nextpow2(17)
    32
    '''
    if ispow2(n):
        return n
    
    count = 0
    while n != 0:
        n = n >> 1
        count += 1
    return 1 << count

class SamplingRateError(ValueError):
    '''
    Indicates that the conversion of frequency to sampling rate could not be
    performed.
    '''

    def __init__(self, fs, requested_fs):
        self.fs = fs
        self.requested_fs = requested_fs

    def __str__(self):
        mesg = 'The requested sampling rate, %f Hz, is greater than ' + \
               'the DSP clock frequency of %f Hz.'
        return mesg % (self.requested_fs, self.fs)

def convert(src_unit, dest_unit, value, dsp_fs):
    '''
    Converts value to desired unit give the sampling frequency of the DSP.

    Parameters specified in paradigms are typically expressed as
    frequency and time while many DSP parameters are expressed in number of
    samples (referenced to the DSP sampling frequency).  This function provides
    a convenience method for converting between conventional values and the
    'digital' values used by the DSP.

    Note that for converting units of time/frequency to n/nPer, we have to
    coerce the value to a multiple of the DSP period (e.g. the number of 'ticks'
    of the DSP clock).

    Appropriate strings for the unit types:

        fs
            sampling frequency
        nPer
            number of samples per period
        n
            number of samples
        s
            seconds
        ms
            milliseconds
        nPow2
            number of samples, coerced to the next greater power of 2 (used for
            ensuring efficient FFT computation)

    >>> convert('s', 'n', 0.5, 10000)
    5000
    >>> convert('fs', 'nPer', 500, 10000)
    20
    >>> convert('s', 'nPow2', 5, 97.5e3)
    524288

    Parameters
    ----------
    src_unit: string
    dest_unit: string
        Destination unit
    value: numerical (e.g. integer or float)
        Value to be converted

    Returns
    -------
    converted unit : numerical value
    '''
    
    def fs_to_nPer(req_fs, dsp_fs):
        if dsp_fs < req_fs:
            raise SamplingRateError(dsp_fs, req_fs)
        return int(dsp_fs/req_fs)
    
    def nPer_to_fs(nPer, dsp_fs):
        return dsp_fs/nPer
    
    def n_to_s(n, dsp_fs):
        return n/dsp_fs
    
    def s_to_n(s, dsp_fs):
        return int(s*dsp_fs)

    def ms_to_n(ms, dsp_fs):
        return int(ms*1e-3*dsp_fs)

    def n_to_ms(n, dsp_fs):
        return n/dsp_fs*1e3
   
    def s_to_nPow2(s, dsp_fs):
        return nextpow2(s_to_n(s, dsp_fs))

    fun = '%s_to_%s' % (src_unit, dest_unit)
    return locals()[fun](value, dsp_fs)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
