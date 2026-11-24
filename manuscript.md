# A two-station dispatch example with a shared ten-ticket batch

Vedant Thaker  
Independent Researcher, Jeffersonville, Indiana, USA  
vedant.thaker1602@gmail.com

Teaching note · November 24, 2026

### Abstract

Two stations each choose whether to fetch a parcel before they see a ticket. The same four plans have different winners depending on how the tickets reach the stations. A blind, uniform shuffle of one batch makes fetching a different product at each station worthwhile. If separate queues allow the most unfavorable mix at both stations, two empty dock visits win. This example lets a reader select an uncertainty set from an assignment rule, calculate a worst-case expectation and distinguish that expectation from the chance of fulfilling both orders.

## Set the assignment rule before choosing the routes

A batch contains ten tickets. Between one and nine request stock-keeping unit A, and the rest request B. A controller prepositions one robot at each station before either sees a ticket. Station 1 can fetch A, station 2 can fetch B, and either can make an empty dock visit. An empty visit takes one step and a fetch takes five. Arrival pays 0.2 utility units, delivering the requested item pays another 0.8, and each step costs 0.025. These are classroom payoffs.

First suppose the tickets are uniformly shuffled. Station 1 takes the first ticket and station 2 the second. If the batch contains k tickets for A, either station draws A with marginal probability p = k/10. The two draws are dependent. Their expected utilities can still be added. Alternatively, suppose each station draws from a separate queue with its own unknown fraction between 1/10 and 9/10. A warehouse's order-batching rule can sort orders by location [1]. What matters here is whether that rule permits a low fraction of A at station 1 at the same time as a high fraction of A at station 2. All four plans are fixed before allocation.

## Score the four plans

An empty visit scores 0.175. Bringing A scores 0.075 + 0.8p in expectation at station 1. Bringing B scores 0.075 + 0.8(1 − p) at station 2. The possible endpoint scores for each fetch are 0.155 and 0.795. One shuffled batch forces these slopes to offset in the mean of the two fetches. Separate queues can put both fetches at 0.155.

| Station 1 | Station 2 | Separate queues | One shuffled batch |
| --- | --- | --- | --- |
| Empty | Empty | 0.175 | 0.175 |
| Bring A | Empty | 0.165 | 0.165 |
| Empty | Bring B | 0.165 | 0.165 |
| Bring A | Bring B | 0.155 | 0.475 |

Table 1. Worst expected utility per station. The score averages the two stations equally and takes the worst admissible composition for each plan.

## Extend the calculation

Let station i have weight wᵢ > 0, with weights summing to one. At the midpoint m of the admissible interval, let the weighted mean utility be M. For a fixed plan the utility of station i varies linearly with slope bᵢ. If both endpoints m − h and m + h are admissible, separate queue compositions yield the minimum L = M − hΣᵢwᵢ|bᵢ|. Each station can reach its own worse endpoint. With a single shared composition, the minimum is C = M − h|Σᵢwᵢbᵢ| because the weighted sum has only one slope. This also holds for our discrete batch compositions.

The triangle inequality gives C ≥ L. For h > 0 the gap is positive exactly when some station slopes have opposite signs. This is a one-stage example of coupled and rectangular uncertainty sets, an established distinction in robust optimization [2]. A gap for a plan changes the winner only if it makes up that plan's disadvantage relative to its competitors.

## Two exercises with solutions

**1. Vary the price of travel.** Keep the same credits and replace the cost per step with c ≥ 0. For which c does the best plan strictly change from two empty visits under separate queues to two fetches under a shared batch?

**Solution.** Under separate queues, a fetch adds 0.8 × 0.1 − 4c to the worst score of an empty visit. Both stations therefore strictly prefer an empty visit when c > 0.02. Under a shared batch, fetching at both stations earns 0.8 × 0.5 − 4c more per station than two empty visits. Fetching at just one station changes the mean by (0.08 − 4c)/2 compared with two empty visits, so it cannot improve on them for c > 0.02. The strict reversal holds throughout 0.02 < c < 0.10. At c = 0.02 all four plans tie under separate queues. At c = 0.10 the two symmetric plans tie under the shared batch.

**2. Change the success criterion.** If five tickets request each product, what is the chance that *both* promised deliveries are correct? For the plan (bring A, bring B), it is (5/10) × (5/9) = 5/18. Conditioning on station 1 receiving A leaves five B tickets among nine. The 0.475 in Table 1 is an expected utility in the assigned units. It cannot serve as a probability of joint fulfillment.

## Data and code availability

The companion file `study/dispatch_note.py` uses Python's standard library to enumerate all 90 ordered ticket allocations at each of nine compositions. Its four exact route scores are in `study/ticket_scores.csv`. [Public study repository](https://github.com/VEDANT1602/verified-robot-dispatch)

## Author and disclosures

Vedant Thaker is the sole author. He framed the dispatch question around a shared batch and chose to present it as a two-station teaching example. OpenAI Codex assisted with checking the proof, enumerating the ticket assignments and drafting the teaching note, including the worked exercises.

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The author declares no competing interests.

## References

[1] R. de Koster, T. Le-Duc and K. J. Roodbergen. Design and control of warehouse order picking: A literature review. European Journal of Operational Research 182, 481–501 (2007). <https://doi.org/10.1016/j.ejor.2006.07.009>

[2] W. Wiesemann, D. Kuhn and B. Rustem. Robust Markov Decision Processes. Mathematics of Operations Research 38, 153–183 (2013). <https://doi.org/10.1287/moor.1120.0566>
