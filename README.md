# Did the dock receive the right parcel?

On open-floor layout 300000, the visit-only dispatch sends one robot straight to the dock and leaves the other idle. It scores a dock visit in five steps. The receiving inventory is empty. On the very same layout, the midpoint dispatch sends a robot for parcel A and another for B. The routes cost 18 team steps and the dock has the requested item whichever tag is correct. [Visit-only receipt](results.csv?plain=1#L3) · [Two-parcel receipt](results.csv?plain=1#L9)

A path replay records which item arrives with each robot. This separates arrival, expected correct receipt, and travel. Across 1,800 simulated layouts, the visit-only policy reaches the dock on 98.56% and delivers zero correct parcels. With equally likely parcel identities, midpoint dispatch has 55% expected correct receipt at 11.99 mean team steps. [Inventory update](run.py#L79) · [Full dispatch records](results.csv)

## One tag reliability per shift or one per layout?

The wide robust policy protects against tag reliability anywhere from 0.1 to 0.9. Scoring the worst case separately on each layout makes it look better than midpoint, with mean utilities of 0.2091 and 0.1666. Requiring one common tag reliability across the entire shift reverses the ordering to 0.2312 and 0.3202. The model of uncertainty determines which number answers the dispatch question.

The search considers 600 seeded layouts in each of three map families. Travel is deterministic, robots may share a cell, and dock inventory is read without error. [Objective and assumptions](manuscript.md) · [Paper PDF](manuscript.pdf)

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
