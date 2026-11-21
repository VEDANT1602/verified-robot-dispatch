# Preparation record

When parcel probabilities are shared: an exact robustness gap for two-robot dispatch

Vedant Thaker · 21 November 2026

## Original work

Vedant Thaker is the sole author. He designed the original two-robot dispatch study, wrote its manuscript, developed its original software, and requested the comparisons and checks reported in this revision.

The author reports that the research project began on 2 August 2026. The previous versions and the new revision represent different stages of the work.

## Revision activities

OpenAI Codex assisted with the affine worst-case gap argument, exact arithmetic checks, route replay, shared-batch optimum certificate, and valuation sensitivity analyses, as well as literature checks and preparation of the revised text. The author set the research question and requested the revision.

## Computational checks

The regenerated baseline CSV matched its pinned digest and passed its verifier. Path replay checked actual inventory under selected routes. Independent rational endpoint evaluation in theory_check.py reproduced L and C and their closed forms for every archived policy, the balanced policy and all four decisions in the two-layout example. These calculations certify the finite examples under the stated model. The symbolic proof establishes the general claim for affine utilities.

## Data and version records

The original route data and implementation are available in the baseline repository. The supplement contains the original 27,000 records, source and environment locks, the route-price and batch-optimum scripts, and theory_check.py. From the supplement directory run python verify.py, python run.py, python verify.py, python weight_sensitivity.py, python batch_optimum.py and python theory_check.py. The last program uses exact rational arithmetic to generate theory_values.csv.

[Original pinned software](https://github.com/VEDANT1602/verified-robot-dispatch/tree/d13914af20963306897a9865bbc2d3b5d293f4fa) · [Revision code and data](https://github.com/VEDANT1602/verified-robot-dispatch/tree/main/revision/supplement)

The reported checks are computational. No independent personal rerun or line-by-line review of these revisions by the author is asserted here.
