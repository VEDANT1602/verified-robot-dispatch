# When parcel probabilities are shared: an exact robustness gap for two-robot dispatch

**Vedant Thaker**  
Independent Researcher, Jeffersonville, Indiana, United States  
Correspondence: vthaker1@asu.edu  
21 November 2026

## Abstract

A dispatcher with uncertain order identity can protect each order against its own worst-case parcel probability or protect a batch against one common probability. For affine receipt utility we derive the exact difference between these criteria. It is positive precisely when a plan favors one parcel on some positive-weight layouts and the other parcel on others, provided the probability interval has positive width. A two-layout example then reverses the ordering of two plans: empty visits maximize the order-wise minimum, whereas opposite single-parcel deliveries maximize the shared minimum. On 1,800 generated layouts, order-wise mean worst utilities were 0.2091 for wide-interval dispatch and 0.1666 for midpoint dispatch; their shared-parameter minima were 0.2312 and 0.3202. Eighteen equal-cost route exchanges balanced the receipt counts and attained the exact finite-panel optimum of 0.3266. The proof concerns a family of ambiguity sets, and the examples use specified conditional probabilities rather than measured scanner reliabilities.

## 1. What can vary from one order to the next?

Two robots share one dock and two labeled candidate parcels. A route that unloads only A succeeds exactly when A was requested. If orders share a common probability of requesting the indicated parcel, sending A on one layout and B on another can offset exposure to an erroneous indication. That protection disappears if a different unfavorable probability can apply to every order.

Gerkey and Matarić classify multi-robot allocation by robot, task and assignment requirements [1]. Our robots choose one route each, may idle, and cannot both claim the same parcel; the uncertainty concerns which physical receipt fills the order. Wiesemann, Kuhn and Rustem distinguish uncertainty sets that couple parameters across decisions from rectangular sets that permit independent variation [2]. Here the effect can be calculated in closed form for fixed finite dispatch plans, including exactly when it changes a ranking.

## 2. Conditional order identity and a replayable route

A simple generative interpretation starts with two physical identities. Conditional on layout i, let the true request Z be equally likely to be either physical parcel; let an observed tag T name Z with probability q and the other parcel with probability 1 − q, symmetrically. Call the parcel named by T “A” and the other one “B.” Then pᵢ = Pr(Z = T | T, i) = q. With an unequal prior or asymmetric tag errors, the equality need not hold: if a physical parcel has prior probability λ and a symmetric classifier names it, its posterior is qλ/[qλ + (1 − q)(1 − λ)]. The simulation enumerates outcomes conditional on a tag with A already designated. It generates maps and routes and integrates out the request; it draws no scanner observations or calibrating tag labels.

The two starts, two parcel cells and dock occupy five distinct locations in one connected component of each accepted map. Unused cells may lie in other components. The open family has an 8 × 8 grid, obstacle probability 0.10 and a 13-step deadline. Clutter uses 9 × 9, 0.23 and 14. Door uses 10 × 10, 0.08 and 15, with the central column replaced by a wall with one opening. Independent seeds generate 600 layouts per family, starting at 300000, 310000 and 320000. Disconnected marked cells trigger a redraw. Policies see the complete map at decision time. No parameters were fitted on the panel. Differences across families combine size, obstacle density, deadline and, for Door, topology.

Each robot can stay, travel directly to the dock or collect one parcel and unload it at the dock. Cardinal moves, pickup and unload each cost one step. The deadline applies to each robot separately. Team travel S is the sum of both route lengths. Robots may share any cell, including the dock, and cannot claim the same parcel. Breadth-first distances determine route feasibility. A second path traversal follows each selected route, tracks cargo and checks dock inventory and travel against the enumerated plan.

For fixed route i, let Vᵢ denote any dock visit and Aᵢ, Bᵢ indicate receipts of the designated and alternative parcels. Correct receipt has expectation Dᵢ(p) = pAᵢ + (1 − p)Bᵢ. The descriptive utility Uᵢ(p) = 0.2Vᵢ + 0.8Dᵢ(p) − 0.025Sᵢ awards a small service credit for a visit and charges Sᵢ team steps. These illustrated values specify preferences in the example. No facility supplied a service valuation.

## 3. The exact gap between two worst cases

Let i index finitely many layouts with weights wᵢ > 0 summing to one. Fix a plan π choosing one feasible route per layout. Write Uᵢ(p) = Uᵢ(m) + bᵢ(p − m), where [m − h, m + h] is the uncertainty interval, h ≥ 0 and bᵢ = 0.8(Aᵢ − Bᵢ) under the illustrated valuation. Let M be the weighted mean of Uᵢ(m), K the weighted mean of |bᵢ| and J the absolute value of the weighted mean of bᵢ.

Proposition. The order-wise minimum L(π) over independent layout probabilities equals M − hK. The shared minimum C(π), with one p on every layout, equals M − hJ. Hence C(π) − L(π) = h(K − J). To prove this, the minimum of each affine line over the interval is its midpoint value minus h times its absolute slope. Applying this once per line gives L; applying it to their weighted sum gives C. The triangle inequality gives K ≥ J. Equality holds if h = 0 or all nonzero slopes on positive-weight layouts have the same sign. This includes plans that deliver both parcels or neither everywhere.

Strict ranking reversal has an exact criterion. Write ΔM, ΔK and ΔJ for quantities of plan X minus those of plan Y. The simultaneous conditions L(X) > L(Y) and C(X) < C(Y) hold exactly when hΔK < ΔM < hΔJ. This follows by substituting the two formulas. A positive coupling gap for one plan alone does not guarantee reversal: the difference between the two plans’ gaps must exceed X’s order-wise advantage.

## 4. A two-layout reversal with the same travel prices

Give two layouts equal weight. Both offer an empty direct visit in one step. Each also offers a five-step visit carrying a single parcel: only A on the first layout, only B on the second. Use the baseline utility and p between 0.1 and 0.9. Empty travel earns 0.175 in either layout. Delivery has endpoint scores 0.155 and 0.795, in opposite order across layouts. Delivering in both layouts therefore guarantees only 0.155 per layout if the endpoint can vary, but its mean is 0.475 at every shared p. A mixed plan that delivers on just one layout has a minimum mean of 0.165 under either rule. Enumeration of the four plans proves both maxima for these restricted menus. The example requires no map sampling, route tie or numerical optimizer.

## 5. Five dispatch rules on a seeded panel

The visit-only policy maximizes V − 0.025S. The tag-favoring and midpoint rules maximize U at p = 0.9 and p = 0.5. Narrow and wide robustness maximize the minimum U over [0.3, 0.7] and [0.1, 0.9], respectively. The endpoint check is exact because U is affine in p. Equal scores to ten decimal places favor fewer steps and then the lexicographically greatest action pair. The route is selected once and evaluated at three probabilities. Each policy's worst utility below takes the minimum on each layout over the wide interval, then averages over 1,800 layouts.

| Policy | Visit % | D(.1) % | D(.5) % | D(.9) % | Steps | Worst U |
| --- | --- | --- | --- | --- | --- | --- |
| Visit | 98.56 | 0.00 | 0.00 | 0.00 | 4.78 | 0.078 |
| Tag | 90.39 | 9.16 | 31.78 | 54.40 | 7.57 | 0.042 |
| Midpoint | 93.17 | 55.80 | 55.00 | 54.20 | 11.99 | 0.167 |
| Narrow | 93.17 | 53.36 | 52.81 | 52.25 | 11.68 | 0.187 |
| Wide | 86.61 | 37.11 | 36.64 | 36.17 | 9.26 | 0.209 |

Table 1. Map-weighted outcomes under the baseline valuation. D is expected correct receipt.

## 6. Single-parcel deliveries under a travel charge

At equal identity odds the midpoint–wide receipt gap was 18.36 percentage points. Treating layouts as independent generator draws within each equally weighted family, a paired normal approximation gives a 95% interval of 17.13 to 19.59 points. The standard error uses the within-family variance of paired differences divided by 600 and combines the three strata with weights of one third. The interval describes Monte Carlo error for this generator. Comparing policies within a layout preserves the actual unit of replication.

Both parcels could be delivered on 587 layouts. The wide planner did so in all 587. The midpoint planner achieved 96.00% expected receipt in that stratum. On the other 1,213 maps the corresponding rates were 5.98% and 35.16%. Relative to an empty visit, adding one parcel provides at most 0.08 of worst-case credit at the baseline weights. Four more steps cost 0.10, enough to favor an empty visit. At p = 0.5 the false-success rates were 49.97% for wide and 38.17% for midpoint. An oracle given the identity in advance, subject to the deadline but free to ignore travel cost, achieved a 59.56% upper bound on expected receipt.

Two-parcel delivery was feasible on 46.50% of open, 31.33% of clutter and 20.00% of door layouts. At p = 0.5 the wide policy delivered on average with probabilities of 49.75%, 35.33% and 24.83%. For midpoint those figures were 66.58%, 54.92% and 43.50%.

## 7. Reoptimizing the routes as valuations change

The sensitivity experiment reselected routes at every setting. It varied visit credit over 0, 0.2 and 0.4, awarded the remaining unit credit to receipt and charged 0, 0.0125, 0.025 or 0.05 per step. The baseline credits appear in the first four rows of Table 2. At zero travel price both planners could collect every affordable extra parcel, subject to the per-robot deadline, and tied on expected receipt at all three visit credits. At every positive travel price examined, midpoint earned higher expected receipt at p = 0.5. Travel savings were less consistent: with a 0.4 visit credit and a 0.025 step price, wide averaged 10.25 steps and midpoint 9.82. The remaining cells and utilities are supplied with the scripts.

| Visit credit | Receipt credit | Step price | Midpoint D(.5) % | Wide D(.5) % |
| --- | --- | --- | --- | --- |
| 0.2 | 0.8 | 0 | 56.31 | 56.31 |
| 0.2 | 0.8 | 0.0125 | 56.31 | 48.36 |
| 0.2 | 0.8 | 0.025 | 55.00 | 36.64 |
| 0.2 | 0.8 | 0.05 | 25.36 | 8.17 |
| 0 | 1 | 0.025 | 56.25 | 32.61 |
| 0.4 | 0.6 | 0.025 | 44.39 | 36.25 |

Table 2. Selected cells from the 3 × 4 valuation grid. All cells use the same 1,800 maps.

## 8. A certificate for the optimum on all 1,800 layouts

On the seeded panel L is 0.2091 for wide and 0.1666 for midpoint. Their mean-absolute slopes K were 0.06444 and 0.40000, respectively. The corresponding absolute mean slopes J were only 0.00933 and 0.01600. Thus h(K − J), with h = 0.4, adds approximately 0.0220 to wide and 0.1536 to midpoint when the parameter is shared. The resulting scores are 0.2312 and 0.3202. The gap formula explains why the ranking reverses.

The shared-p optimum can be certified on this known panel. For any batch plan, its minimum mean utility cannot exceed its mean utility at p = 0.5. The sum of the layout-wise midpoint maxima therefore bounds every feasible batch plan. The published midpoint tie-break delivers A on 972 layouts and B on 1,008. There are 42 layouts on which an equal-cost A-only route can replace the chosen B-only route. Switching the first 18 eligible routes in family and seed order leaves midpoint utility unchanged and yields 990 receipts of each parcel. The aggregate utility is then constant in p and equals the upper bound, 0.3266389. Receipt probability at p = 0.5 and mean steps remain 0.55 and 11.99.

Use an order-wise minimum if misses must be tolerable on each layout despite potentially different failure rates. A common endpoint is appropriate when one unknown reliability describes the entire batch and performance is judged in aggregate. With multiple scanners or shifts, group orders by the reliability mechanism and justify any pooling. The certificate uses the full layout panel. A sequential dispatcher that discovers orders only as they arrive would need an online rule and a fresh evaluation.

## 9. Scope of the probability model

Collision avoidance and handoffs can change which routes fit a deadline. The inventory replay assumes that a completed unload identifies the physical parcel without error. A scanner-dependent deployment needs parcel-level comparison against a trusted inventory, estimates of error clustering by scanner or shift, measured route times and a service valuation. Simulated receipt, team steps and the common-p certificate do not establish performance on a physical fleet.

A shift, a scanner or a product family defines a plausible pooling unit only if tagged, independently verified orders support that level of calibration. A common underlying scanner accuracy with layout-specific priors can still yield different posterior probabilities. Without evidence about those priors, the shared-p and layout-wise calculations should be reported as alternative assumptions.

## Data and code availability

The original route data and implementation are available in the baseline repository. The supplement contains the original 27,000 records, source and environment locks, the route-price and batch-optimum scripts, and theory_check.py. From the supplement directory run python verify.py, python run.py, python verify.py, python weight_sensitivity.py, python batch_optimum.py and python theory_check.py. The last program uses exact rational arithmetic to generate theory_values.csv.

[Pinned baseline](https://github.com/VEDANT1602/verified-robot-dispatch/tree/d13914af20963306897a9865bbc2d3b5d293f4fa) · [Revision code and data](https://github.com/VEDANT1602/verified-robot-dispatch/tree/main/revision/supplement) · [Preparation record](https://github.com/VEDANT1602/verified-robot-dispatch/blob/main/revision/PREPARATION.md)

## Computational verification

The regenerated baseline CSV matched its pinned digest and passed its verifier. Path replay checked actual inventory under selected routes. Independent rational endpoint evaluation in theory_check.py reproduced L and C and their closed forms for every archived policy, the balanced policy and all four decisions in the two-layout example. These calculations certify the finite examples under the stated model. The symbolic proof establishes the general claim for affine utilities.

## Author contribution

Vedant Thaker is the sole author. He designed the original two-robot dispatch study, wrote its manuscript, developed its original software, and requested the comparisons and checks reported in this revision.

## Use of computational assistance

OpenAI Codex assisted with the affine worst-case gap argument, exact arithmetic checks, route replay, shared-batch optimum certificate, and valuation sensitivity analyses, as well as literature checks and preparation of the revised text. The author set the research question and requested the revision.

## Funding

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

## Competing interests

The author declares no competing interests.

## References

[1] B. P. Gerkey and M. J. Matarić. A Formal Analysis and Taxonomy of Task Allocation in Multi-Robot Systems. International Journal of Robotics Research 23(9), 939–954 (2004). https://doi.org/10.1177/0278364904045564

[2] W. Wiesemann, D. Kuhn and B. Rustem. Robust Markov Decision Processes. Mathematics of Operations Research 38(1), 153–183 (2013). https://doi.org/10.1287/moor.1120.0566
