#!/bin/csh
#sleep 30m
echo "lauching timing jobs...."
set cidx=0
# the idea is to saturate the 8 cores in one socket so you use
#only one logical core per physical core in the socket.
# Look at /proc/cpuinfo for to see how the idexes match
#the physical cores.  Basically they go like core 1: logicals 0 and 8,
# core 2: logicals 1 and 9 and so on.
foreach i ( 1 2 ) 
    @ cidx2 = $cidx + 3
    echo $cidx2
    echo "job" $i 
    \rm -rf thread${i}
    mkdir thread${i}
    cp -p filelist.txt thread${i}/
    cp -p hltTiming.py thread${i}/
    cp -p *.json thread${i}/.
    cd thread${i}
    /usr/bin/time taskset -c 0-7 cmsRun hltTiming.py >&! full.log &
#    /usr/bin/time taskset -c ${cidx}-${cidx2} cmsRun hltTiming.py >&! full.log &
#    echo "/usr/bin/time taskset -c ${cidx}-${cidx2} cmsRun hltTiming.py >&! full.log &"
    @ cidx = $cidx + 4
    cd -
end

#sleep 1.2h
#source runHarvesting.csh 
