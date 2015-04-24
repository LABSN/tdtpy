# There are apparently two more possible RCX types: 74 and 78.  It's not clear
# what these represent.

RCX_UNDEFINED = 65
RCX_BUFFER = 68
RCX_INTEGER = 73
RCX_FLOAT = 83
RCX_COEFFICIENT = 80
RCX_BOOL = 76

RCX_CAST = {
    RCX_INTEGER: int,
    RCX_FLOAT: float,
    RCX_BOOL: bool,
}

# Eventually I'd like to bind the device-specific variables as "constants" on
# the correct DSPCircuit so people can leverage these in their programs rather
# than having to look up the correct channel.  However, we need to compile a
# list of all the necessary module-level variables first.
RX6_DEFAULTS = {
    'DAC_CHANNEL_1':    1,
    'DAC_CHANNEL_2':    2,
    'ADC_CHANNEL_1':    128,
    'ADC_CHANNEL_2':    129,
}

# Value is the bit number containing the status for the corresponding value as
# returned by RP.GetStatus()
RCX_STATUS_BITMASK = {
    'connected':   0,
    'loaded':   1,
    'running':   2,
}
