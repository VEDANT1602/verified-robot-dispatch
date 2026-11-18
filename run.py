"""Enumerate feasible two-robot dispatches and audit identity-aware receipt.

Run with Python 3.11 (standard library only): python run.py
"""
import csv
import itertools
import random
from collections import deque
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
REGIMES = {"open": (8, .10, 13), "clutter": (9, .23, 14), "door": (10, .08, 15)}
POLICIES = ("visit", "tag", "midpoint", "robust", "robust_narrow")
WORLD = (.1, .5, .9)
PRICE = .025


def distances(source, cells):
    frontier = deque([source])
    cost = {source: 0}
    while frontier:
        x, y = point = frontier.popleft()
        for nxt in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if nxt in cells and nxt not in cost:
                cost[nxt] = cost[point] + 1
                frontier.append(nxt)
    return cost


def layout(seed, name):
    n, density, horizon = REGIMES[name]
    rng = random.Random(seed)
    while True:
        cells = {(x, y) for x in range(n) for y in range(n) if rng.random() >= density}
        if name == "door":
            opening = rng.randrange(n)
            cells = {p for p in cells if p[0] != n//2 or p[1] == opening}
            cells.add((n//2, opening))
        s0, s1, a, b, goal = rng.sample(sorted(cells), 5)
        d = [distances(pos, cells) for pos in [s0, s1, goal]]
        if all(pos in d[2] for pos in (s0,s1,a,b)):
            break
    routes = []
    for robot in (0, 1):
        opts = [("idle", 0), ("direct", d[robot][goal])]
        opts += [(tag, d[robot][pickup]+1+d[2][pickup]+1) for tag,pickup in [("A",a),("B",b)]]
        routes.append([(act,steps) for act,steps in opts if steps <= horizon])
    candidates = []
    for (act0,c0),(act1,c1) in itertools.product(*routes):
        actions = (act0,act1)
        if act0 == act1 and act0 in ("A","B"):
            continue
        candidates.append((actions, c0+c1, int(actions != ("idle","idle")), int("A" in actions), int("B" in actions)))
    return candidates, (cells, (s0, s1), {"A":a, "B":b}, goal, horizon)


def replay(world, actions):
    """Walk the selected routes and maintain a dock inventory independent of plan flags."""
    cells, starts, depots, goal, horizon = world
    received, visited, total_steps = set(), False, 0
    for start, action in zip(starts, actions):
        if action == "idle":
            continue
        pos = start
        cargo = None
        steps = 0
        stops = [goal] if action == "direct" else [depots[action], goal]
        for dest in stops:
            to_dest = distances(dest, cells)
            while pos != dest:
                x,y = pos
                pos = next(q for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
                           if to_dest.get(q) == to_dest[pos]-1)
                steps += 1
            if pos == goal:
                visited = True
                if cargo is not None:
                    received.add(cargo)
                    steps += 1
            else:
                cargo = next(label for label,loc in depots.items() if loc == pos)
                steps += 1
        assert steps <= horizon
        total_steps += steps
    return total_steps, int(visited), int("A" in received), int("B" in received)


def utility(plan, p):
    _, steps, visit, a, b = plan
    return .2*visit + .8*(p*a + (1-p)*b) - PRICE*steps


def decide(candidates, policy):
    def key(plan):
        actions, steps, visit, a, b = plan
        if policy == "visit":
            value = visit - PRICE*steps
        elif policy in ("robust","robust_narrow"):
            lo, hi = (.1,.9) if policy == "robust" else (.3,.7)
            value = min(utility(plan, lo), utility(plan, hi))
        else:
            value = utility(plan, .9 if policy == "tag" else .5)
        return (round(value, 10), -steps, actions)
    return max(candidates, key=key)


def main():
    records = []
    for k, name in enumerate(REGIMES):
        for j in range(600):
            seed = 300000 + 10000*k + j
            candidates, world = layout(seed, name)
            both = int(any(a and b for _,_,_,a,b in candidates))
            possible_a = max(plan[3] for plan in candidates)
            possible_b = max(plan[4] for plan in candidates)
            robust_plan = decide(candidates, "robust")
            worst_utility = lambda plan: min(utility(plan, .1), utility(plan, .9))
            assert all(worst_utility(robust_plan) >= worst_utility(c) - 1e-10 for c in candidates)
            for policy in POLICIES:
                plan = decide(candidates, policy)
                actions, steps, visit, a, b = plan
                assert replay(world, actions) == (steps, visit, a, b)
                for p in WORLD:
                    verified = p*a+(1-p)*b
                    assert 0 <= verified <= visit
                    oracle = p*possible_a+(1-p)*possible_b
                    assert verified <= oracle + 1e-10
                    records.append((name, seed, policy, p, *actions, steps, visit, a, b, both, verified, visit-verified, worst_utility(plan), oracle))
    fields = ["layout","seed","policy","p_A","robot_0","robot_1","steps","goal_visit","A_receipt","B_receipt","both_feasible","verified","false_visit","worst_utility","id_oracle_bound"]
    with (HERE / "results.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(fields); w.writerows(records)
    for name in REGIMES:
        for policy in POLICIES:
            filtered = [r for r in records if r[0] == name and r[2]==policy]
            subset = [r for r in filtered if r[3] == .5]
            print(name, policy, "coverage/steps/P(both feasible)/receipts p=.1,.5,.9/false=.5",
                  *[round(mean(r[i] for r in subset),4) for i in (7,6,10)],
                  *[round(mean(r[11] for r in filtered if r[3] == p),4) for p in WORLD],
                  round(mean(r[12] for r in subset),4))


if __name__ == "__main__":
    main()
