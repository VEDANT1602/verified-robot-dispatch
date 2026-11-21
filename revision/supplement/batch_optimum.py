"""Certify a common-reliability optimum on the published, fully known layout panel."""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import fmean, variance
from math import sqrt
from run import REGIMES, layout, decide, utility, replay


def main():
    routes = []
    paired = defaultdict(list)
    for k, family in enumerate(REGIMES):
        for offset in range(600):
            seed = 300000 + k*10000 + offset
            choices, world = layout(seed, family)
            midpoint = decide(choices, "midpoint")
            wide = decide(choices, "robust")
            paired[family].append(.5*(sum(midpoint[3:])-sum(wide[3:])))
            exchange = None
            if midpoint[3:] == (0, 1):
                eligible = [c for c in choices if c[3:] == (1, 0) and c[1] == midpoint[1]]
                if eligible:
                    exchange = max(eligible, key=lambda c: c[0])
            routes.append((family, seed, world, midpoint, exchange))
    a = sum(item[3][3] for item in routes)
    b = sum(item[3][4] for item in routes)
    assert (a, b) == (972, 1008)
    flips, chosen = 0, []
    for family, seed, world, midpoint, exchange in routes:
        switch = flips < (b-a)//2 and exchange is not None
        plan = exchange if switch else midpoint
        assert replay(world, plan[0]) == plan[1:]
        assert abs(utility(plan, .5) - utility(midpoint, .5)) < 1e-12
        flips += int(switch)
        chosen.append((family, seed, switch, *plan[0], *plan[1:],
                       utility(midpoint, .5), utility(plan, .1), utility(plan, .9)))
    mean_upper = fmean(row[-3] for row in chosen)
    endpoint_min = min(fmean(row[i] for row in chosen) for i in (-2, -1))
    assert abs(mean_upper - endpoint_min) < 1e-12
    with Path(__file__).with_name("batch_optimum.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["family", "seed", "switched", "robot_0", "robot_1", "steps",
                         "visit", "receipt_A", "receipt_B", "midpoint_upper_bound",
                         "selected_lo_utility", "selected_hi_utility"])
        writer.writerows(chosen)
    mean_gap = fmean(fmean(values) for values in paired.values())
    se = sqrt(sum(variance(values)/len(values) for values in paired.values())/len(paired)**2)
    print("Midpoint A/B:", a, b, "eligible exchanges:", sum(row[-1] is not None for row in routes),
          "switched:", flips, "upper bound:", mean_upper, "achieved minimum:", endpoint_min)
    print("Paired receipt difference (percentage points), approximate stratified 95% interval:",
          100*mean_gap, 100*(mean_gap-1.96*se), 100*(mean_gap+1.96*se))

if __name__ == "__main__":
    main()
