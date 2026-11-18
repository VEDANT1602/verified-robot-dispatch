# A delivery receipt for two-robot dispatch under uncertain package identity

**Vedant Thaker**  
Working paper · 18 November 2026

## Abstract

Both robots can reach the dock while the requested package stays on its shelf. Five planning strategies face the same routes on 1,800 generated layouts. A separate receipt check establishes which of two possible packages reaches the dock under each possible requested identity. Across three layout families, a visit-only strategy reaches the dock on 98.56% of layouts and delivers no packages. With equally likely identities, a planner using midpoint weights delivers the requested package with probability 55.00%. Maximizing the minimum utility on each layout lowers that probability to 36.64%. The latter planner takes fewer steps, achieves higher worst-case utility under its own criterion, and delivers both items wherever that is feasible. The delivery loss arises mainly on the remaining 1,213 layouts, where a single affordable delivery can still be worth attempting under shared population-level uncertainty. The unit over which the planner takes its minimum changes what reaches the dock.

## 1. Which event counts as success?

A dock beacon can confirm that a robot arrived. An inventory record can confirm that it unloaded parcel A. Neither event alone establishes that A was the parcel on the order. This distinction matters when checking a controller whose inputs contain an uncertain identity tag. It also permits an exact test. With only two candidate parcels, both possible outcomes of any route can be scored without sampling package identities.

Leike et al. used hidden performance functions to expose gaps between observed reward and intended behavior in small environments [1]. Skalse et al. characterized when optimizing a proxy can lower true return [2]. Liu, Sun and Zheng derived robust optimization over correlated proxy rewards and studied how known reward features change the optimization problem [3]. Their formulation estimates policies under a correlation constraint. The dispatch model here uses an explicit interval on one identity probability and searches a finite list of routes. This simpler setting makes a different comparison possible. Given the exact route chosen, how much of a change in delivery comes from the choice of proxy, and how much comes from the choice to protect each layout individually?

## 2. Dispatch model

Each map has two start cells, two package cells and one dock, all distinct. The robots move simultaneously by unit steps along open cells of a four-neighbor grid. Each robot may stay put, drive straight to the dock, or collect one package and deliver it. A pickup and an unload each cost one step. Two robots cannot claim the same package. Both may use the same cell at the same time, including the dock. Breadth-first search gives the shortest distance for each route. A joint plan is feasible if both routes meet the map's time limit. Total cost counts steps across the team, even when the robots move in parallel.

The open family uses an 8 by 8 grid with independent 10% obstacle probability and a 13-step limit. Clutter uses a 9 by 9 grid, 23% obstacles and 14 steps. Door uses a 10 by 10 grid, 8% obstacles and 15 steps. It also replaces the central column with a wall containing one open doorway. Each family contributes 600 independently seeded maps. Disconnected samples are redrawn until the five marked cells communicate. Holding out maps here means that no planner parameters are fitted on these maps. All policies receive the complete evaluation map at decision time. The three families change several properties together, so their differences describe operating conditions rather than isolated obstacle effects.

Let V indicate any dock visit, A and B indicate completed receipts at the dock, and S count total steps. The tag assigns probability p to A being the requested parcel. Receipts are deterministic route unloads. A separate replay walks the selected paths, loads the item present at the pickup cell and checks the dock inventory against the scored route. Evaluating both possible requested identities then gives expected receipt D(p) = pA + (1 - p)B. The planning utility is U(p) = 0.2V + 0.8D(p) - 0.025S. A direct visit earns a small service credit even when the order stays open. These weights define the decision problem. The results report V, D and S separately so that readers can apply a different valuation.

The visit policy maximizes V - 0.025S. The tag and midpoint policies maximize U at p = 0.9 and 0.5, respectively. The wide robust planner maximizes the minimum of U over p from 0.1 to 0.9. The narrow robust planner uses 0.3 to 0.7. Utility is affine in p, so checking the two endpoints is exact. Ties use lower team travel followed by a fixed route ordering. All decisions are deterministic. The verifier reports D under p = 0.1, 0.5 and 0.9. The false-success rate is V - D, expressed per assigned order. A nonvisit is never counted as a false success.

## 3. Does guarding both identities improve delivery?

Table 1 averages over all 1,800 layouts with equal weight. The three receipt columns use the same chosen routes. Worst utility means the mean across layouts of the lower endpoint utility on the wide interval. It includes travel and dock credit.

| Planner | Dock visit % | Receipt at .1 % | Receipt at .5 % | Receipt at .9 % | Steps | Worst utility |
| --- | --- | --- | --- | --- | --- | --- |
| Visit | 98.56 | 0.00 | 0.00 | 0.00 | 4.78 | 0.078 |
| Tag | 90.39 | 9.16 | 31.78 | 54.40 | 7.57 | 0.042 |
| Midpoint | 93.17 | 55.80 | 55.00 | 54.20 | 11.99 | 0.167 |
| Narrow robust | 93.17 | 53.36 | 52.81 | 52.25 | 11.68 | 0.187 |
| Wide robust | 86.61 | 37.11 | 36.64 | 36.17 | 9.26 | 0.209 |

The visit policy's zero receipts follow from its objective and the two handling steps required for a parcel. This is a positive control for the audit. The tag policy provides a more informative baseline. When A is correct nine times in ten, its receipt rate is within 0.20 percentage points of the midpoint's. When A is correct once in ten, its receipt rate falls to 9.16%. Recording only visits would hide that difference entirely.

The wide robust planner improves on the optimistic tag policy when p is low. It also spends 2.73 fewer team steps per layout than the midpoint planner. Yet the midpoint scores higher on receipt at all three evaluation probabilities. At p = 0.5, 49.97% of all orders produce a false-success visit under wide robustness, compared with 38.17% under midpoint weights. The geometry imposes its own limit. An oracle given the true package identity, allowed to ignore travel cost but required to respect the deadline, can achieve at most 59.56% expected receipt at p = 0.5. This bound is computed separately for each item and layout.

## 4. Where does the loss occur?

Both parcels can be delivered together on 587 layouts. The wide robust planner always does so there. The midpoint planner's expected receipt in that stratum is 96.00%. On the other 1,213 layouts, the wide planner's expected receipt is 5.98%, against 35.16% for the midpoint. Consider one available package with no guarantee that the tag is right. Carrying that parcel adds at most 0.08 in worst-case receipt credit above the dock visit. Four extra steps cost 0.10. A short empty trip can therefore win an exact search. All candidate lists pass an independent inequality check that the selected wide plan attains at least the worst-case utility of every alternative on that layout.

The opportunity to hedge differs by family. Both parcels can arrive on 46.50% of open layouts, 31.33% of clutter layouts and 20.00% of door layouts. At p = 0.5 the wide planner's receipt rates in those families are 49.75%, 35.33% and 24.83%, respectively. The corresponding midpoint rates are 66.58%, 54.92% and 43.50%. These map-conditional comparisons avoid treating the three identity settings or five policies as independent trials. The supplied records retain each seed for paired reanalysis.

## 5. Interpretation and limits

There are two possible operational meanings for an uncertain tag. One system might suffer a different failure mechanism on every order. Another might use the same scanner throughout a shift, with a single unknown reliability over the batch. Taking the minimum separately on each layout permits the poorly matched identity distribution to change from order to order. Taking the minimum after averaging assumes a common p. Under that shared p, the minimum mean utility is 0.3202 for the midpoint planner and 0.2312 for the wide robust planner. Their ranking reverses when the minimum is taken per layout, as Table 1 shows. Roughly balanced package geometries give the midpoint planner nearly constant pooled delivery from one endpoint to the other. A shift-wide optimum was not fitted. The observed stability arises from the decisions on the sampled layouts.

The verifier assumes every completed unload identifies its physical parcel perfectly. Persistent scanner errors, delayed receipts and correlated tag failures remain open tests. Collision avoidance, handoffs and online travel delays would alter which plans can deliver both parcels. The benchmark isolates the decision to attempt an order when its identity is uncertain. It supplies no evidence about physical robot performance. A useful next evaluation would replay parcel-level event logs, estimate whether tag errors cluster by scanner or by shift, then choose the unit at which to apply robustness before scoring receipt.

## Reproducibility

Run `python run.py` with Python 3.11 and the standard library. The script regenerates the maps, enumerates routes, checks feasible-receipt bounds and writes 27,000 policy-by-identity records to `results.csv`. Seeds begin at 300000, 310000 and 320000 in the three families and advance by one per layout. Published percentages use exact expectations over two identities, then average over layouts. They are simulation results.

## Research and writing assistance

Vedant Thaker supplied the research brief and source materials. OpenAI Codex assisted with study design, implementation, execution, literature review and drafting. Clever Humanizer suggested edits to the abstract. The final wording was checked against the analysis.

## References

[1] J. Leike, M. Martic, V. Krakovna, P. A. Ortega, T. Everitt, A. Lefrancq, L. Orseau and S. Legg. AI Safety Gridworlds. 2017. https://arxiv.org/abs/1711.09883

[2] J. Skalse, N. H. R. Howe, D. Krasheninnikov and D. Krueger. Defining and Characterizing Reward Hacking. Revised preprint, 2025. https://arxiv.org/abs/2209.13085

[3] Z. Liu, X. Sun and Z. Zheng. Robust Optimization for Mitigating Reward Hacking with Correlated Proxies. ICLR, 2026. https://www.cs.tulane.edu/~zzheng3/publication/reward_hacking_iclr26.pdf
