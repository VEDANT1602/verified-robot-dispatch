"""Recalculate the published dispatch comparisons using only the archived CSV."""
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import fmean


def check_close(label, actual, target, tolerance):
    if not math.isclose(actual, target, abs_tol=tolerance, rel_tol=0):
        raise ValueError(f"{label}: observed {actual}, expected {target} within {tolerance}")


def main():
    path = Path(__file__).with_name("results.csv")
    with path.open(encoding="utf-8", newline="") as stream:
        records = list(csv.DictReader(stream))
    layout_counts = Counter()
    seen = set()
    utility_by_route = defaultdict(list)
    utility_by_world = defaultdict(list)
    neutral = defaultdict(list)
    for row in records:
        layout, seed, policy = row["layout"], int(row["seed"]), row["policy"]
        p = float(row["p_A"])
        key = (layout, seed, policy, p)
        if key in seen:
            raise ValueError(f"Duplicate scenario {key}")
        seen.add(key)
        receipt = p * int(row["A_receipt"]) + (1-p) * int(row["B_receipt"])
        visit = int(row["goal_visit"])
        cost = int(row["steps"])
        check_close("receipt", receipt, float(row["verified"]), 1e-10)
        check_close("false visit", visit-receipt, float(row["false_visit"]), 1e-10)
        utility = 0.2*visit + 0.8*receipt - 0.025*cost
        utility_by_route[layout,seed,policy].append(utility)
        utility_by_world[policy,p].append(utility)
        if p == .5:
            if policy == "visit":
                layout_counts[layout] += 1
            neutral[policy].append((visit, receipt, cost, int(row["both_feasible"])))
    if len(seen) != 27000 or layout_counts != {"open":600, "clutter":600, "door":600}:
        raise ValueError(f"Unexpected experiment size or layout distribution: {len(seen)}, {layout_counts}")
    expected = {"visit":(98.56,0,4.78), "tag":(90.39,31.78,7.57), "midpoint":(93.17,55.00,11.99),
                "robust_narrow":(93.17,52.81,11.68), "robust":(86.61,36.64,9.26)}
    for policy, targets in expected.items():
        sample = neutral[policy]
        if len(sample) != 1800:
            raise ValueError(f"Incomplete midpoint evaluation for {policy}")
        observed = (100*fmean(r[0] for r in sample), 100*fmean(r[1] for r in sample), fmean(r[2] for r in sample))
        for label, value, target in zip(("visit %","receipt %","steps"),observed,targets):
            check_close(f"{policy} {label}", value, target, .00501)
        print(f"{policy:14}  visit {observed[0]:6.2f}%  receipt {observed[1]:6.2f}%  steps {observed[2]:5.2f}")
    for policy, shared, per_layout, restricted in [("midpoint", .3202, .1666, 35.16), ("robust", .2312, .2091, 5.98)]:
        min_after_mean = min(fmean(utility_by_world[policy,p]) for p in (.1,.5,.9))
        mean_after_min = fmean(min(values) for key,values in utility_by_route.items() if key[2] == policy)
        check_close("common reliability utility", min_after_mean, shared, .000051)
        check_close("layout-wise utility", mean_after_min, per_layout, .000051)
        constrained = [r[1] for r in neutral[policy] if not r[3]]
        if len(constrained) != 1213:
            raise ValueError("Expected 1,213 layouts where both items cannot be delivered together")
        check_close("receipt on constrained layouts", 100*fmean(constrained), restricted, .00501)
    if any(r[1] != 1 for r in neutral["robust"] if r[3]):
        raise ValueError("A feasible two-parcel delivery was missed")
    print("Verified 27,000 records, five planners, and both worst-case utility comparisons.")


if __name__ == "__main__":
    main()
