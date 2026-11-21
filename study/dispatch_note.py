"""Enumerate dispatch menus and ticket allocations exactly. Python standard library."""
import csv
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TEN=10
ENDPOINTS=(Q(1,10),Q(9,10))
def score(serve,correct):
    return Q(1,5)+Q(4,5)*serve*correct-Q(1+4*serve,40)

def main():
    cases=[]
    for first,second in product([False,True],repeat=2):
        separate=(min(score(first,p) for p in ENDPOINTS)+min(score(second,1-p) for p in ENDPOINTS))/2
        by_k=[]
        for count in range(1,TEN):
            ids=range(TEN)
            tickets=permutations(ids,2)
            outcomes=[(score(first,i<count)+score(second,j>=count))/2 for i,j in tickets]
            mean=sum(outcomes)/len(outcomes)
            p=Q(count,TEN)
            assert mean==(score(first,p)+score(second,1-p))/2
            by_k.append(mean)
        common=min(by_k)
        slopes=(Q(4,5)*first,-Q(4,5)*second)
        assert common-separate==Q(2,5)*(sum(map(abs,slopes))/2-abs(sum(slopes)/2))
        cases.append([int(first),int(second),str(separate),str(common),f'{float(separate):.3f}',f'{float(common):.3f}'])
    assert [c[2:4] for c in cases]==[['7/40','7/40'],['33/200','33/200'],['33/200','33/200'],['31/200','19/40']]
    with (ROOT/'ticket_scores.csv').open('w',newline='') as f:
        rows=csv.writer(f)
        rows.writerow(['station_1_A','station_2_B','separate_exact','shared_exact','separate_decimal','shared_decimal'])
        rows.writerows(cases)
    print('Four route combinations, nine batch compositions, 90 ordered allocations per composition verified.')
if __name__=='__main__':main()
