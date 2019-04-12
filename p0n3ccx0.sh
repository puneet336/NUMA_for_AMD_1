#!/bin/sh

export OMP_NUM_THREADS=NCORES
export GOMP_CPU_AFFINITY="6 22 38 54"
export OMP_PROC_BIND=true
#https://github.com/flame/blis/blob/master/travis/do_testsuite.sh
export BLIS_IR_NT=1
export BLIS_JR_NT=1
export BLIS_IC_NT=1
export BLIS_JC_NT=4
numactl --physcpubind=6,22,38,54 --membind=3 ./xhpl

