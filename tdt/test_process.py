from .dsp_process import DSPProcess
import time


def main():
    process = DSPProcess()
    circuit = process.load_circuit('components/test_physiology_RZ5', 'RZ5')
    # processed_buffer = circuit.get_buffer('processed', 'r', channels=16)
    raw_buffer = circuit.get_buffer('raw', 'r', channels=16, block_size=4098)
    print("BUFFER SIZE", raw_buffer.size)

    process.start()

    last_ctime = 0

    read = 0
    time.sleep(2)
    shape = raw_buffer.read().shape
    read += shape[-1]
    print(shape)
    ctime = circuit.get_tag('zTime')
    print(ctime, ctime-last_ctime)
    last_ctime = ctime
    time.sleep(2)
    shape = raw_buffer.read().shape
    read += shape[-1]
    print(shape)
    ctime = circuit.get_tag('zTime')
    print(ctime, ctime-last_ctime)
    last_ctime = ctime
    time.sleep(2)
    shape = raw_buffer.read().shape
    read += shape[-1]
    print(shape)
    ctime = circuit.get_tag('zTime')
    print(ctime, ctime-last_ctime)
    last_ctime = ctime
    time.sleep(2)
    shape = raw_buffer.read().shape
    read += shape[-1]
    print(shape)
    ctime = circuit.get_tag('zTime')
    print(ctime, ctime-last_ctime)
    last_ctime = ctime
    circuit.stop()
    time.sleep(2)
    shape = raw_buffer.read().shape
    read += shape[-1]
    print(shape)
    print("Samples read", read)
    ctime = circuit.get_tag('zTime')
    print(ctime, ctime-last_ctime)
    last_ctime = ctime
    process.terminate()

    # from pylab import *
    # print 'import'
    # comtypesplot(data[0])
    # print 'plotted'
    # show()
    # print 'show'
    # for i in range(10):
    #     time.sleep(0.1)
    #     print "PROC_READ", raw_buffer.read().shape
    # process.get_tag('ch1_out_sf')
    # process.set_tag('ch1_out_sf', 50e3)
    # process.get_tag('ch1_out_sf')
    # time.sleep(1)
    # process.terminate()

if __name__ == "__main__":
    main()
    # import cProfile
    # cProfile.run('main()')
    # import pstats
    # p = pstats.Stats('profile.dmp')
    # p.strip_dirs().sort_stats('cumulative').print_stats(50)
