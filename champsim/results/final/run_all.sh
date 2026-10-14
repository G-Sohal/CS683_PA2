#!/bin/bash
# Runs every Task 1B / 2B / 3 configuration on all three traces (12 at a time).
# Launched from inside traces/ with "-traces TraceN.gz" so that ChampSim derives the
# same random seed (from the trace name) as the Task 2A/2B runs (../TraceN.gz).
export ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

run_one() {
    local cfg=$1 t=$2 P=hashed_perceptron-no bin
    case $cfg in
        baseline)          bin=$P-no-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-baseline ;;
        ip_stride)         bin=$P-ip_stride-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-ip_stride_sim ;;
        spp)               bin=$P-spp-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-spp_sim ;;
        dyn_irrip)         bin=$P-no-no-no-no-no-no-lru-lru-lru-dyn_irrip-lru-lru-lru-lru-1core-dyn_irrip ;;
        spp_dyn_irrip)     bin=$P-spp-no-no-no-no-no-lru-lru-lru-dyn_irrip-lru-lru-lru-lru-1core-spp_dyn_irrip ;;
        spp_dyn_irrip_noaware) bin=$P-spp-no-no-no-no-no-lru-lru-lru-dyn_irrip_noaware-lru-lru-lru-lru-1core-spp_dyn_irrip_noaware ;;
    esac
    "$ROOT/bin/$bin" -warmup_instructions 25000000 -simulation_instructions 25000000 \
        -traces Trace$t.gz > "$ROOT/results/final/${cfg}_trace$t.txt" 2>&1
}
export -f run_one

cd "$ROOT/../traces"
for cfg in ${CONFIGS:-baseline spp dyn_irrip spp_dyn_irrip ip_stride spp_dyn_irrip_noaware}; do
    for t in 1 2 3; do echo "$cfg $t"; done
done | xargs -P 12 -n 2 bash -c 'run_one "$@"' _
echo ALL_DONE
