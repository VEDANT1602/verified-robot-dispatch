"""Reoptimize both planners on the published finite layout panel under each valuation."""
import csv
from pathlib import Path
from statistics import fmean

from run import REGIMES, layout, replay

VISIT_WEIGHTS = (0, .2, .4)
STEP_PRICES = (0, .0125, .025, .05)
PROBABILITIES = (.1, .5, .9)
POLICIES = ("midpoint", "wide")
OUT = Path(__file__).resolve().parent


def utility(plan, probability, visit_weight, step_price):
    _, steps, visit, received_a, received_b = plan
    expected_receipt = probability * received_a + (1 - probability) * received_b
    return visit_weight * visit + (1 - visit_weight) * expected_receipt - step_price * steps


def choose(candidates, policy, visit_weight, step_price):
    probabilities = (.5,) if policy == "midpoint" else (.1, .9)

    def rank(plan):
        score = min(utility(plan, p, visit_weight, step_price) for p in probabilities)
        return round(score, 10), -plan[1], plan[0]

    return max(candidates, key=rank)


def main():
    panels = []
    for index, family in enumerate(REGIMES):
        for offset in range(600):
            seed = 300000 + index * 10000 + offset
            panels.append(layout(seed, family))

    rows = []
    for visit_weight in VISIT_WEIGHTS:
        for step_price in STEP_PRICES:
            for policy in POLICIES:
                receipts, steps, visits, lower, upper, local = [], [], [], [], [], []
                for candidates, world in panels:
                    plan = choose(candidates, policy, visit_weight, step_price)
                    actions, step_count, visit, a, b = plan
                    assert replay(world, actions) == (step_count, visit, a, b)
                    receipts.append(.5 * (a + b))
                    steps.append(step_count)
                    visits.append(visit)
                    lo, hi = [utility(plan, p, visit_weight, step_price) for p in (.1, .9)]
                    lower.append(lo)
                    upper.append(hi)
                    local.append(min(lo, hi))
                rows.append(dict(visit_credit=visit_weight, receipt_credit=1-visit_weight,
                                 price_per_step=step_price, policy=policy, layouts=len(panels),
                                 midpoint_receipt_pct=100*fmean(receipts), mean_steps=fmean(steps),
                                 visit_pct=100*fmean(visits), mean_layout_min=fmean(local),
                                 common_p_min=min(fmean(lower), fmean(upper))))

    with (OUT / "weight_sensitivity.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
