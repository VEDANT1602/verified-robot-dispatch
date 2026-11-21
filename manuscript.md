# A two-station dispatch example with a shared ten-ticket batch

Vedant Thaker  
Independent Researcher, Jeffersonville, Indiana, USA  
vedant.thaker1602@gmail.com

Teaching note

**Research period (author-reported)** · August 2–13, 2026 &nbsp; | &nbsp; **Manuscript revised** · November 21, 2026

### Abstract

A pick station can receive an unknown mix of orders in two different ways. Tickets drawn from one randomly shuffled batch have the same marginal type probability at both stations. Separate queues can have different mixtures. For a fixed dispatch plan with affine receipt utility, the difference between the two worst-case scores is determined by cancellation of slopes across stations. In this teaching example the batch contains ten tickets. Each of two stations draws one ticket, and eight stay in the batch. The four available action pairs can be enumerated exactly. Blind draws from the same batch favor a delivery at each station. Separate station-specific queues favor empty dock visits under the same payoffs.

## Tickets from one batch

Order grouping and routing are distinct choices in warehouse picking. Grouping orders by nearby storage locations, for example, can give different zones different order mixes [1]. Consider a batch of ten tickets in a uniformly random order. Station 1 takes the first ticket and station 2 takes the second. The remaining eight play no part in the dispatch decision. Each ticket requests one of two distinct stock-keeping units, A or B. A controller prepositions one robot for each station before either ticket is revealed. It knows that at least one and at most nine tickets request A.

If k tickets request A, each station has marginal probability p = k/10 of receiving an A request. The assignments are dependent because sampling is without replacement. Linearity of expected mean utility only requires the marginals. The common p is justified by the random assignment mechanism. Routing tickets by product type, revealing the first ticket before choosing the second action, or drawing from separate queues changes that argument. Here p denotes request composition. A scanner’s accuracy would need its own observation model.

## What the two minima charge

Fix an action at each station i before its request is revealed. Let wᵢ > 0 be its weight, with sum one. Write its expected utility as Uᵢ(p) = Uᵢ(m) + bᵢ(p − m). The slope is the utility advantage of receiving an A request over a B request under that action. Suppose both endpoints m − h and m + h of the admissible set are possible, with h ≥ 0. Define M = ΣᵢwᵢUᵢ(m).

The worst-case weighted score with separate probabilities is L = M − hΣᵢwᵢ|bᵢ|. With one probability shared by every station, it is C = M − h|Σᵢwᵢbᵢ|. For separate queues, each affine function can take its worse endpoint. For the common batch, the weighted sum is a single affine function, so only its aggregate slope enters. The triangle inequality gives C ≥ L. For h > 0 the difference is positive exactly when two positive-weight stations have slopes of opposite signs. The same argument holds for a discrete set of batch compositions containing the endpoints.

This is the one-dimensional form of the established distinction between coupled and rectangular uncertainty sets [2]. A positive difference for one plan does not by itself reverse two plans. If X leads Y under separate queues by d > 0, Y wins under a common batch exactly when its gain C(Y) − L(Y) exceeds the gain for X by more than d.

## Two stations with opposite reachable stocks

In this restricted route menu, either robot can visit the dock in one step without a parcel. Station 1 can instead bring A in five steps, and station 2 can bring B in five. Assume a dock visit earns 0.2 utility units, delivery of the requested item earns a further 0.8, and each step costs 0.025. These values construct the reversal. An empty visit scores 0.175. A five-step delivery scores 0.075 + 0.8p at station 1 and 0.075 + 0.8(1 − p) at station 2. Their endpoint values are 0.155 and 0.795 in opposite orders.

When every queue needs its own guarantee, the smaller travel commitment wins. With tickets assigned blindly from the same batch, delivering A at one station and B at the other gives expected score 0.475 for every feasible batch composition. This guarantees the mean in expectation over ticket allocation. It does not guarantee a correct receipt on either realized ticket. The example illustrates why a dispatcher needs to know how tickets were allocated before choosing the uncertainty set.


| Station 1 | Station 2 | Separate queues L | One shuffled batch C |
| --- | --- | --- | --- |
| Empty | Empty | 0.175 | 0.175 |
| Bring A | Empty | 0.165 | 0.165 |
| Empty | Bring B | 0.165 | 0.165 |
| Bring A | Bring B | 0.155 | 0.475 |
Table 1. Worst expected utility per station for equal station weights and batch fractions from 1/10 to 9/10. Each column compares the same four plans.

## Data and code availability

dispatch_note.py in the companion supplement reproduces the example using Python’s standard library. The note uses no experimental data.

[Study files, software and source records](https://github.com/VEDANT1602/verified-robot-dispatch/tree/main/study)

## Author and disclosures

Vedant Thaker is the sole author and set the research question. OpenAI Codex assisted with checking the proof, enumerating the ticket assignments and drafting the theory note.

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The author declares no competing interests.

## References

[1] R. de Koster, T. Le-Duc and K. J. Roodbergen. Design and control of warehouse order picking: A literature review. European Journal of Operational Research 182, 481–501 (2007). <https://doi.org/10.1016/j.ejor.2006.07.009>

[2] W. Wiesemann, D. Kuhn and B. Rustem. Robust Markov Decision Processes. Mathematics of Operations Research 38, 153–183 (2013). <https://doi.org/10.1287/moor.1120.0566>
