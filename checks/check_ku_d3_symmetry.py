#!/usr/bin/env python3
"""Exact F2 action on the full BG primitive ku E3 source, not a d3 proof."""
from itertools import product


def xor_all(items):
    out = 0
    for x in items:
        out ^= x
    return out


# Tuple: coefficient (h0 or v), x coordinate, z0 power, z1 power.
basis = [(tag, x, i, total-i) for tag, total in [('h',5),('v',4)]
         for x in [0,1] for i in range(total+1)]
idx = {m:i for i,m in enumerate(basis)}


def vec(terms):
    return xor_all(1 << idx[m] for m in terms)


def gamma(a,b):
    terms=[('h',0,a-1,b), ('h',1,a,b-1)]
    if a>=2: terms.append(('v',0,a-2,b))
    if b>=2: terms.append(('v',1,a,b-2))
    return vec(terms)


generators=[gamma(a,6-a) for a in range(1,6)]
generators.append(vec([('v',0,i,4-i) for i in range(4)]
                      + [('v',1,i,4-i) for i in range(1,5)]))
generators += [vec([m]) for m in [('h',0,5,0),('h',1,0,5),
                                 ('v',0,4,0),('v',1,0,4)]]


def monomial_pullback(m,A):
    tag,x,a,b=m
    poly={(0,0):1}
    for power,row in [(a,A[0]),(b,A[1])]:
        for _ in range(power):
            out={}
            for (i,j),c in poly.items():
                for k,value in enumerate(row):
                    if value:
                        key=(i+(k==0),j+(k==1))
                        out[key]=out.get(key,0)^c
            poly={k:v for k,v in out.items() if v}
    terms=[]
    for y,value in enumerate(A[x]):
        if value:
            terms += [(tag,y,i,j) for (i,j),c in poly.items() if c]
    return vec(terms)


def pushforward(y,A):
    return vec([m for m in basis
                if (monomial_pullback(m,A)&y).bit_count()%2])


lookup={xor_all(generators[i] for i in range(10) if bits>>i&1):bits
        for bits in range(1<<10)}
assert len(lookup)==1024
actions=[]
for a,b,c,d in product(range(2),repeat=4):
    if (a*d+b*c)%2:
        A=((a,b),(c,d))
        columns=[lookup[pushforward(g,A)] for g in generators]
        actions.append((A,columns))

valid=[]
for lam in range(1<<5): # lambda kills Phi and four axis classes
    if all(((lam&(column^(1<<j))).bit_count()%2)==0
           for A,columns in actions for j,column in enumerate(columns)):
        valid.append(lam)
print('Invariant functionals killing cyclic axis classes and vPhi5:')
for lam in valid:
    print(tuple((lam>>j)&1 for j in range(5)))
print('Count:',len(valid))
assert valid==[0,10]


def e2_basis(n,s):
    """Full reduced BG E2 basis: h0 degree determined by s and v degree."""
    out=[]
    for v in range(s+1):
        ordinary=n-2*v
        for e0,e1 in product(range(2),repeat=2):
            remaining=ordinary-e0-e1
            if ordinary<=0 or remaining<0 or remaining%2:
                continue
            for z0 in range(remaining//2+1):
                out.append((s-v,v,e0,e1,z0,remaining//2-z0))
    return out


def differential(m):
    h,v,e0,e1,z0,z1=m
    terms=[]
    if e0==0 and z0:
        terms.append((h+2,v,1,e1,z0-1,z1))
        if z0>=2: terms.append((h+1,v+1,1,e1,z0-2,z1))
    if e1==0 and z1:
        terms.append((h+2,v,e0,1,z0,z1-1))
        if z1>=2: terms.append((h+1,v+1,e0,1,z0,z1-2))
    return terms


def rank(vectors):
    pivots={}
    for vector in vectors:
        for k in sorted(pivots,reverse=True):
            if vector>>k&1: vector^=pivots[k]
        if vector: pivots[vector.bit_length()-1]=vector
    return len(pivots)


def d2_columns(n,s):
    source=e2_basis(n,s)
    target=e2_basis(n-1,s+2)
    index={m:i for i,m in enumerate(target)}
    return [xor_all(1<<index[t] for t in differential(m)) for m in source]


def e3_dimension(n,s):
    return (len(e2_basis(n,s))-rank(d2_columns(n,s))
            -(rank(d2_columns(n+1,s-2)) if s>=2 else 0))


assert e3_dimension(11,0)==3
assert e3_dimension(11,1)==10
assert e3_dimension(10,4)==1

# The three proposed filtration-zero permanent cycles are independent.
src=e2_basis(11,0)
src_index={m:i for i,m in enumerate(src)}
cyclic=[1<<src_index[(0,0,1,0,5,0)],
        1<<src_index[(0,0,0,1,0,5)]]
phi=xor_all(1<<src_index[m] for m in src
            if m[2]+m[3]==1 and (m[2],m[3],m[4],m[5])
            not in [(1,0,5,0),(0,1,0,5)])
cyclic.append(phi)
assert rank(cyclic)==3
for vector in cyclic:
    assert xor_all(d2_columns(11,0)[i] for i in range(len(src))
                   if vector>>i&1)==0
print('PASS: source dimensions (11,0)=3, (11,1)=10; target (10,4)=1.')
print('PASS: primitive symmetry uniquely selects the nonzero functional.')
