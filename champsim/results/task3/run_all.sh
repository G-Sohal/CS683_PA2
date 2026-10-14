#!/bin/bash
# Runs baseline / spp / dyn_irrip / spp + dyn_irrip on all three traces in parallel.
cd "$(dirname "$0")/../.."
OUT=results/task3
declare -A BIN=(
  [baseline]=hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-baseline
  [spp]=hashed_perceptron-no-spp-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-spp_sim
  [dyn_irrip]=hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-dyn_irrip-lru-lru-lru-lru-1core-dyn_irrip
  [spp_dyn_irrip]=hashed_perceptron-no-spp-no-no-no-no-no-lru-lru-lru-dyn_irrip-lru-lru-lru-lru-1core-spp_dyn_irrip
)
for cfg in baseline spp dyn_irrip spp_dyn_irrip; do
  for t in 1 2 3; do
    ./bin/${BIN[$cfg]} -warmup_instructions 25000000 -simulation_instructions 25000000 \
      -traces ../traces/Trace${t}.gz > $OUT/${cfg}_trace${t}.txt 2>&1 &
  done
done
wait
echo ALL_DONE
