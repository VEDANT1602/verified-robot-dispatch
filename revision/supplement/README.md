# Two-robot dispatch | reproduction and new analyses

## Original benchmark

Original version: https://github.com/VEDANT1602/verified-robot-dispatch/tree/d13914af20963306897a9865bbc2d3b5d293f4fa . The included run.py, verify.py, requirements.txt, CITATION.cff and results.csv come from this commit. The original repository identifies Vedant Thaker as software author. No repository-wide license file appeared at this commit. The publisher should obtain the rights holder’s choice of code license before redistribution.

Use Python 3.11, standard library only. The verification for this revision also ran on Python 3.12.14. From this directory:

1. Run `python verify.py` to validate the distributed CSV.
2. Run `python run.py` to regenerate results.csv.
3. Run `python verify.py` again. The CSV matched SHA-256 3f551d8f41b392f43f1f518caf9572f0874c27a0534e80ca624a4ac03e1038b1 in this revision.

The 27,000 rows are 1,800 seeded layouts × five planners × three evaluation probabilities. The three probability rows are different expectations for a single selected plan.

## Revision analyses

Run `python weight_sensitivity.py`. The script reoptimizes both planners at each of 12 valuations, replays every chosen route and writes 24 summary rows to weight_sensitivity.csv. Expected receipts use equal identity odds. The two utility columns respectively minimize before or after averaging across layouts.

Run `python batch_optimum.py`. This writes the 1,800 selected plans to batch_optimum.csv and prints the achieved and bounding utilities and the paired, family-stratified interval for the baseline midpoint–wide receipt difference. Switching 18 equal-cost midpoint ties gives 990 receipts of each type and certifies the finite-batch common-p optimum under the published valuation. The program assumes all maps in the batch are known before assignments are fixed.

The two revision scripts and their outputs are supplied with this manuscript package. They were added separately from the pinned public benchmark.

## Environment lock

Create separate Linux x86_64 virtual environments with CPython 3.12.14 for the revision and 3.11.9 for the baseline. In the activated revision environment run `python -m pip install --require-hashes -r revision-cp312-linux-x86_64.lock`. For the original checkout, install `baseline-cp311-linux-x86_64.lock` the same way in the baseline environment, then run the commands above. Both workflows use only the standard library. The empty package lists are intentional. The lock headers identify the platform; the baseline transitive pins reconstruct a compatible environment for the published direct requirements.

## Affine utility proof check

Run `python theory_check.py` after the batch certificate. The script checks both formulas in exact fractions for every policy, the certified solution and all four decisions in the two-layout counterexample, then writes theory_values.csv.
