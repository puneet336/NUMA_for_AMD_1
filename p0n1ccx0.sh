#!/bin/sh

export OMP_NUM_THREADS=NCORES
export GOMP_CPU_AFFINITY="2 18 34 50"
export OMP_PROC_BIND=true
#https://github.com/flame/blis/blob/master/travis/do_testsuite.sh
export BLIS_IR_NT=1
export BLIS_JR_NT=1
export BLIS_IC_NT=1
export BLIS_JC_NT=4
numactl --physcpubind=2,18,34,50 --membind=1 ./xhpl

