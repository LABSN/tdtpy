:mod:`tdt.dsp_buffer` -- Wrapper for RPvds buffer objects
=========================================================

Each buffer requires data_tag and index_tag.  All other tags are optional, but
will be used if present.  The data tag and supporting tags can have any name;
however, the recommended approach is to use the data tag plus one of the
following prefixes indicating the purpose of the supporting tag.

    i
        index tag (idx_tag)
    n
        size tag (size_tag)
    sf
        scaling factor tag (sf_tag)
    c
        cycle tag (cycle_tag)
    d
        downsampling tag (dec_tag)

If no value is provided for a tag, the default extension is added to the value
for the data_tag and the circuit is checked to see if the tag exists.  For
example, if you have `spikes`, `spikes_i`, and `spikes_n` tags in your RPvds
circuit, you can simply initialize the class by passing only the name of the
data tag (`spikes`) and it will automatically use `spikes_i` and `spikes_n` as
the index and size tags, respectively.

>>> buffer = circuit.open_buffer('spikes', 'r')

If a required tag cannot be found (either by explicitly defining the tag name or
automatically by adding the default extension to the data tag name), an error is
raised.

Tags
----
data_tag : string (required)
    Tag to read data from
idx_tag : defaults to data_tag_i (required)
    Tag indicating current index of buffer.  For buffer reads this tag
    serves as a "handshake" (i.e. when the index changes, new data is
    available).
size_tag : defaults to data_tag_n (optional)
    Tag indicating current size of buffer.
sf_tag : defaults to data_tag_sf (optional)
    Tag indicating scaling factor applied to data before it is stored in the
    buffer.
cycle_tag : defaults to data_tag_c (optional)
    Tag indicating number of times buffer has wrapped around to beginning.
    Used to ensure no data is lost.
dec_tag : defaults to data_tag_d (optional)
    Tag indicating decimation factor.  Used to compute sampling frequency of
    data stored in buffer: e.g. if circuit runs at 100 kHz, but you only
    sample every 25 cycles, the actual sampling frequency is 4 kHz.  
    
Additional Parameters
----------------------
circuit
    Circuit object buffer is attached to
block_size : int
    Coerce data read/write to multiple of the block size.  Must be a
    multiple of the channel number.
src_type :
    Type of data in buffer (can be a string or numpy dtype).  Valid data
    formats are float32, int32, int16 and int8.
dest_type :
    Type to convert data to
channels :
    Number of channels stored in buffer

Available attributes
--------------------
data_tag, idx_tag, size_tag, sf_tag, cycle_tag, dec_tag :
    Names of supporting tags present in the circuit (both the names provided
    as well as the ones automatically discovered when the buffer is created.
    None if the tag is not present.
src_type
    Numpy dtype of the data stored on the device
dest_type
    Numpy dtype of array returned when data is read from the device
compression
    Number of samples stored in a single 32-bit "slot" on the device.  For
    example, if you are using the MCFloat2Int8 to convert four samples of
    data into 8-bit integers and storing these four samples as a single
    32-bit work, the compression factor is 4.
sf
    Scaling factor of the data
resolution
    If data is being compressed, computes the actual resolution of the
    acquired data given the scaling factor.  For example, if you are
    compressing data into an 8-bit integer using a scaling factor of 10,
    then the resolution of the acquired data will be 0.1 since numbers will
    get rounded to the nearest tenth (e.g. 0.183 will get rounded to 0.2).
dec_factor
    Also called the "downsampling rate".  Indicates the number of device
    cycles before a sample is acquired and stored in the buffer.  If 1, a
    sample is acquired on every cycle.  If 2, a sample is acquired on every
    other cycle.
fs
    Sampling frequency of data stored in buffer.  This is basically the
    sampling frequency of the device divided by the decimation factor
    (dec_factor): e.g. if a sample is acquired only on every other cycle,
    then the sampling frequency of the buffer is effectively half of the
    device clock rate.
channels
    Number of channels
block_size
    Coerce read size to multiples of this value (can be overridden if needed)

Buffer size attributes
----------------------

There are three ways to think about the buffer size.  First, how many 32-bit
words can the buffer hold?  All buffer components in a RPvds store data in
32-bit word segments.  However, we can two 16-bit values or four 8-bit values
into a single word.  Even if a buffer can only hold 1000 32-bit words, it may
actually hold 2000 or 4000 samples if we are compressing two or four samples of
data into a single buffer "slot".  Now, if we are storing multiple channels of
data in a single buffer, then the buffer will fill up more quickly than an
identically-sized buffer storing only a single channel of data.  By reporting
buffer size as the number of samples per channel, we can get a sense for how
quickly the buffer will fill up.

>>> buffer = circuit.get_buffer('spikes', 'r', channels=16)
>>> print buffer.compression    # number of samples in each buffer slot
2
>>> print buffer.n_slots        # number of slots
4000
>>> print buffer.n_samples      # number of samples
8000
>>> print buffer.size           # number of samples per channel
500

In the above example, we know that even though the buffer can hold 8,000
samples of data, it will fill up after only 500 samples of 16-channel data are
collected.  This provides a useful metric for knowing whether we have set the
buffer size appropriately.

n_slots
    Size in number of 32-bit words (the buffer's atomic unit of of storage)
n_samples
    Size in number of samples (data points) that can be stored in the buffer.
    The size will be either 1x, 2x or 4x the size of n_slots depending on how
    many samples are stored in each slot.
size
    Size in number of samples (data points) per channel.
sample_time
    How many seconds before the buffer is full?

It is also possible to resize buffers in the RPvds circuit if a size_tag is
present.  The above attributes reflect the current size of the buffer, which may
be smaller than the maximum possible size allocated.

n_slots_max
    Maximum size in number of 32-bit words
n_samples_max
    Maximum size in number of samples
size_max
    Maximum size in number of channels
