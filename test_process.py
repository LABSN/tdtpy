from dsp_process import DSPProcess
import time

def main():
    #process = DSPProcess('test_physiology', 'RZ5', 0.1, 30)
    process = DSPProcess('physiology', 'RZ5', 0.1, 30)
    processed_buffer = process.get_buffer('processed', 'r', channels=16,
            block_size=1024)
    raw_buffer = process.get_buffer('raw', 'r', channels=16, block_size=1024)
    process.start()

    time.sleep(5)
    data = raw_buffer.read()
    process.terminate()
    print 'terminate'
    
    #from pylab import *
    #print 'import'
    #comtypesplot(data[0])
    #print 'plotted'
    #show()
    #print 'show'
    #for i in range(10):
        #time.sleep(0.1)
        #print "PROC_READ", raw_buffer.read().shape
    #process.get_tag('ch1_out_sf')
    #process.set_tag('ch1_out_sf', 50e3)
    #process.get_tag('ch1_out_sf')
    #time.sleep(1)
    #process.terminate()

if __name__ == "__main__":
    main()
    #import cProfile
    #cProfile.run('main()')
    #import pstats
    #p = pstats.Stats('profile.dmp')
    #p.strip_dirs().sort_stats('cumulative').print_stats(50)
