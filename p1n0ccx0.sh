#!/bin/sh

export OMP_NUM_THREADS=NCORES
export GOMP_CPU_AFFINITY="1 17 33 49"
export OMP_PROC_BIND=true
#https://github.com/flame/blis/blob/master/travis/do_testsuite.sh
export BLIS_IR_NT=1
export BLIS_JR_NT=1
export BLIS_IC_NT=1
export BLIS_JC_NT=4
numactl --physcpubind=1,17,33,49 --membind=4 ./xhpl

