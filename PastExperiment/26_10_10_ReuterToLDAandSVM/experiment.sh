#! /bin/sh
python lda.py -s 0 -k 100 --alpha=0.1 --beta=0.01 -i 100
python lda.py -s 0 -k 100 --alpha=1.0 --beta=0.01 -i 100
python lda.py -s 0 -k 100 --alpha=3.0 --beta=0.01 -i 100
python lda.py -s 0 -k 100 --alpha=10.0 --beta=0.01 -i 100
python lda.py -s 0 -k 10 --alpha=1.0 --beta=0.01 -i 100
python lda.py -s 0 -k 1000 --alpha=1.0 --beta=0.01 -i 100