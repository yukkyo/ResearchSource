#! /bin/sh
python 12_RunGibbsSampling.py -k 400 --alpha=0.5 --beta=0.5 -i 2
nohup python 12_RunGibbsSampling.py -k 400 --alpha=0.5 --beta=0.5 -i 300 > out1.log 2> err1.log < /dev/null &
nohup python 12_RunGibbsSampling.py -k 200 --alpha=0.5 --beta=0.5 -i 300 > out1.log 2> err1.log < /dev/null &
nohup python 12_RunGibbsSampling.py -k 100 --alpha=0.5 --beta=0.5 -i 300 > out1.log 2> err1.log < /dev/null &
# nohup python 12_RunGibbsSampling.py -k 200 --alpha=0.5 --beta=0.5 -i 250 > out2.log 2> err2.log < /dev/null &
# nohup python 12_RunGibbsSampling.py -k 100 --alpha=0.5 --beta=0.5 -i 250 > out3.log 2> err3.log < /dev/null &

# python 12_RunGibbsSampling.py -k 200 --alpha=0.1 --beta=0.01 -i 150
# python 12_RunGibbsSampling.py -k 100 --alpha=0.1 --beta=0.01 -i 150
