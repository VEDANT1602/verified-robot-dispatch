# A delivery receipt for two-robot dispatch under uncertain package identity

Two robots reach the dock. Did either bring the item on the order? This experiment tracks dock arrival, correct parcel receipt and time in transit separately. Taking the worst case on each route and then averaging reverses the ranking of two dispatch policies compared with scoring a whole shift under one common tag reliability.

[Read the manuscript (PDF)](manuscript.pdf) · [Read the Markdown version](manuscript.md) · [Inspect the results](results.csv)

## Experiment

Two robots can stay idle, travel to a common dock, or collect one of two possible parcels en route. A breadth-first search computes the travel distances. The experiment enumerates feasible joint plans, then walks the selected paths and checks the inventory delivered to the dock. Each of the open-floor, clutter and single-doorway families contributes 600 seeded layouts. All five planners see the same feasible routes on each layout.

The uncertain parameter is the probability that A is the requested parcel. With that probability fixed at `p`, the expected correct receipt is `p × A_receipt + (1 − p) × B_receipt`. The multi-objective utility also rewards a dock visit and charges for team travel. The midpoint planner fixes `p` at 0.5. The wide robust planner protects each layout against every value from 0.1 to 0.9. A narrow robust planner uses 0.3 to 0.7. The other two planners use a dock-visit objective and an optimistic tag probability of 0.9.

## Findings

Dock visit is the percentage of the 1,800 layouts in which a robot reached the dock. Correct receipt is the expected percentage of orders filled when the parcel identities are equally likely. Mean team steps counts the combined travel of both robots per layout.

| Planner | Dock visit | Correct receipt | Mean team steps |
| --- | ---: | ---: | ---: |
| Visit only | 98.56% | 0.00% | 4.78 |
| Optimistic tag | 90.39% | 31.78% | 7.57 |
| Midpoint | 93.17% | 55.00% | 11.99 |
| Narrow robust | 93.17% | 52.81% | 11.68 |
| Wide robust | 86.61% | 36.64% | 9.26 |

On the 587 layouts where both parcels could reach the dock, the wide robust planner always delivered both. On the remaining 1,213, its expected receipt fell to 5.98%, compared with 35.16% for the midpoint policy. For a single tag reliability shared across the shift, the minimum mean utility was 0.3202 for midpoint and 0.2312 for wide robust. Applying the minimum on each layout gave 0.1666 and 0.2091, respectively.

These are finite-grid results. The model permits robots to share a cell and assumes deterministic travel and correct inventory records. A shift-wide robust optimizer, noisy scanners and measured dispatch logs would test different aspects of the finding.

## Reproduce

Use Python 3.11. All scripts use its standard library. Run the following commands from the repository root.

```console
python verify.py
python run.py
python verify.py
```

The first check reads the distributed CSV. The experiment then rewrites it from the map seeds. The final check recomputes receipt probabilities, compares both orders of minimization and averaging, and checks the headline values. The 27,000 rows represent 1,800 layouts × five planners × three identity probabilities. Three rows for the same layout and planner describe one chosen route under different identity assumptions.

## Research context

The finite search offers a small test case for robust rewards and hidden performance measures. [Liu, Sun and Zheng on correlated reward proxies](https://www.cs.tulane.edu/~zzheng3/publication/reward_hacking_iclr26.pdf) · [Leike et al. on hidden performance functions](https://arxiv.org/abs/1711.09883)

Maintained by Vedant Thaker.
