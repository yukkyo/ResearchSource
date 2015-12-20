#! /bin/sh
python 12_RunGibbsSampling.py -k 400 --alpha=0.1 --beta=0.01 -i 1
# nohup python 12_RunGibbsSampling.py -k 400 --alpha=0.1 --beta=0.01 -i 150 > out.log 2> err.log < /dev/null &
# nohup python 12_RunGibbsSampling.py -k 400 --alpha=0.1 --beta=0.01 -i 150 > out1.log 2 > err.log &
# python 12_RunGibbsSampling.py -k 200 --alpha=0.1 --beta=0.01 -i 150
# python 12_RunGibbsSampling.py -k 100 --alpha=0.1 --beta=0.01 -i 150
