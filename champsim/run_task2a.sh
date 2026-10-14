#!/bin/bash

WARM=25000000
SIM=25000000

BASE_BIN="./bin/hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-baseline"
RRIP_BIN="./bin/hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-rrip-lru-lru-lru-lru-1core-rrip"
IRRIP_BIN="./bin/hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-irrip-lru-lru-lru-lru-1core-irrip"

OUT_DIR="results/task2a"
mkdir -p $OUT_DIR

echo "=== Starting Task 2A Simulations (25M warmup, 25M sim) ==="

echo "--- Running Baseline (LRU) on Trace1, Trace2, Trace3 ---"
$BASE_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace1.gz > $OUT_DIR/baseline_Trace1.txt 2>&1 &
PID1=$!
$BASE_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace2.gz > $OUT_DIR/baseline_Trace2.txt 2>&1 &
PID2=$!
$BASE_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace3.gz > $OUT_DIR/baseline_Trace3.txt 2>&1 &
PID3=$!
wait $PID1 $PID2 $PID3
echo "Baseline runs completed."

echo "--- Running RRIP on Trace1, Trace2, Trace3 ---"
$RRIP_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace1.gz > $OUT_DIR/rrip_Trace1.txt 2>&1 &
PID1=$!
$RRIP_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace2.gz > $OUT_DIR/rrip_Trace2.txt 2>&1 &
PID2=$!
$RRIP_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace3.gz > $OUT_DIR/rrip_Trace3.txt 2>&1 &
PID3=$!
wait $PID1 $PID2 $PID3
echo "RRIP runs completed."

echo "--- Running I-RRIP on Trace1, Trace2, Trace3 ---"
$IRRIP_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace1.gz > $OUT_DIR/irrip_Trace1.txt 2>&1 &
PID1=$!
$IRRIP_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace2.gz > $OUT_DIR/irrip_Trace2.txt 2>&1 &
PID2=$!
$IRRIP_BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace3.gz > $OUT_DIR/irrip_Trace3.txt 2>&1 &
PID3=$!
wait $PID1 $PID2 $PID3
echo "I-RRIP runs completed."

echo "=== All Task 2A simulations finished! ==="
