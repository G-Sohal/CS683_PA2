#!/bin/bash
# Runs baseline / ip_stride / spp on all three traces in parallel.
cd "$(dirname "$0")/../.."
OUT=results/task1b
declare -A BIN=(
  [baseline]=hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-baseline
  [ip_stride]=hashed_perceptron-no-ip_stride-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-ip_stride_sim
  [spp]=hashed_perceptron-no-spp-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-spp_sim
)
for cfg in baseline ip_stride spp; do
  for t in 1 2 3; do
    ./bin/${BIN[$cfg]} -warmup_instructions 25000000 -simulation_instructions 25000000 \
      -traces ../traces/Trace${t}.gz > $OUT/${cfg}_trace${t}.txt 2>&1 &
  done
done
wait
echo ALL_DONE
