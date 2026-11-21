"""Exact arithmetic verification of the finite example and the panel's gap formula."""
import csv
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOW, HIGH = F(1,10), F(9,10)
MID, HALF = (LOW+HIGH)/2, (HIGH-LOW)/2


def route_value(steps, visit, a, b, p):
    return F(1,5)*visit + F(4,5)*(p*a+(1-p)*b) - F(1,40)*steps


def score(routes):
    u = [[route_value(*route, p) for p in (LOW,MID,HIGH)] for route in routes]
    slopes = [F(4,5)*(r[2]-r[3]) for r in routes]
    n = len(routes)
    indiv = sum(min(row[0],row[2]) for row in u)/n
    shared = min(sum(row[k] for row in u)/n for k in (0,2))
    meanmid = sum(row[1] for row in u)/n
    absmean = abs(sum(slopes)/n)
    meanabs = sum(abs(v) for v in slopes)/n
    assert indiv == meanmid - HALF * meanabs
    assert shared == meanmid - HALF * absmean
    assert shared >= indiv
    return indiv, shared, meanmid, meanabs, absmean


def main():
    records = []
    # The restricted example has two layouts. Each allows an empty direct visit or
    # one delivery (A-only on the first layout; B-only on the second).
    for x,y in product((0,1),repeat=2):
        routes=[(5,1,1,0) if x else (1,1,0,0), (5,1,0,1) if y else (1,1,0,0)]
        records.append(("two-layout", f"{x}{y}", *score(routes)))
    assert records[0][2:4] == (F(7,40),F(7,40))
    assert records[3][2:4] == (F(31,200),F(19,40))
    archived = {}
    with (ROOT/'results.csv').open() as stream:
        for r in csv.DictReader(stream):
            if r['p_A']=='0.5':
                archived.setdefault(r['policy'],[]).append(tuple(int(r[k]) for k in ('steps','goal_visit','A_receipt','B_receipt')))
    for policy,routes in archived.items():
        assert len(routes)==1800
        records.append(("seeded-panel",policy,*score(routes)))
    with (ROOT/'batch_optimum.csv').open() as stream:
        routes=[tuple(int(r[k]) for k in ('steps','visit','receipt_A','receipt_B')) for r in csv.DictReader(stream)]
    records.append(("seeded-panel","balanced",*score(routes)))
    with (ROOT/'theory_values.csv').open('w',newline='') as stream:
        w=csv.writer(stream)
        w.writerow(('panel','policy','layout_min','shared_min','midpoint_value','mean_abs_slope','abs_mean_slope'))
        for row in records: w.writerow([*row[:2],*(format(float(v),'.10f') for v in row[2:])])
    print('Exact endpoint identities verified for',len(records),'policies and finite panels.')

if __name__ == '__main__':
    main()
