#!/bin/bash

WARM=25000000
SIM=25000000
OUT_DIR="results/task2b"
mkdir -p $OUT_DIR

THRESHOLDS=("0.15" "0.20" "0.25" "0.30" "0.35")
TAGS=("th15" "th20" "th25" "th30" "th35")

echo "=== Building 5 Dynamic I-RRIP Binaries for Sensitivity Study ==="

for i in "${!THRESHOLDS[@]}"; do
    TH="${THRESHOLDS[$i]}"
    TAG="${TAGS[$i]}"
    echo "--- Building dyn_irrip with THRESHOLD = $TH ($TAG) ---"
    sed -i "s/#define DYN_THRESHOLD .*/#define DYN_THRESHOLD $TH/" replacement/dyn_irrip.l2c_repl
    ./build_champsim.sh no dyn_irrip dyn_irrip_${TAG}
done

# Restore default threshold 0.25
sed -i "s/#define DYN_THRESHOLD .*/#define DYN_THRESHOLD 0.25/" replacement/dyn_irrip.l2c_repl

echo "=== All 5 binaries built successfully! ==="

echo "=== Running Sensitivity Simulations across 3 Traces ==="

for i in "${!THRESHOLDS[@]}"; do
    TH="${THRESHOLDS[$i]}"
    TAG="${TAGS[$i]}"
    BIN="./bin/hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-dyn_irrip-lru-lru-lru-lru-1core-dyn_irrip_${TAG}"

    echo "--- Running $TAG (Threshold = $TH) on Trace1, Trace2, Trace3 ---"
    $BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace1.gz > $OUT_DIR/dyn_irrip_${TAG}_Trace1.txt 2>&1 &
    PID1=$!
    $BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace2.gz > $OUT_DIR/dyn_irrip_${TAG}_Trace2.txt 2>&1 &
    PID2=$!
    $BIN -warmup_instructions $WARM -simulation_instructions $SIM -traces ../Trace3.gz > $OUT_DIR/dyn_irrip_${TAG}_Trace3.txt 2>&1 &
    PID3=$!

    wait $PID1 $PID2 $PID3
    echo "Completed simulations for $TAG."
done

echo "=== All Task 2B simulations finished! ==="
