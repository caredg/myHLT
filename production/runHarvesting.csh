\rm -f DQMIO1.root
\rm -f DQMIO2.root
ln -s thread1/DQMIO.root DQMIO1.root
ln -s thread2/DQMIO.root DQMIO2.root
nohup cmsRun harvesting.py >&! harvesting.log &
