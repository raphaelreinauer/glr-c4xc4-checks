#!/usr/bin/env python3
"""Exact spin-index/Gysin ku images for actual double-lens geometries.

Unlike the discarded Laurent experiment, this computes ALL coefficients
from the ordinary twisted spin Dirac index.  The mathematical identification
of these coefficients with the circle-Gysin image is proved in the TeX.
"""
from fractions import Fraction as Q
from math import comb,factorial
from itertools import product
from functools import lru_cache
from flint import fmpz_mat


def convolution(a,b,m):
    out=[Q(0)]*(m+1)
    for i,c in enumerate(a):
        if c:
            for j,d in enumerate(b[:m+1-i]):
                if d:out[i+j]+=c*d
    return out


def power(a,n,m):
    out=[Q(1)]+[Q(0)]*m
    for _ in range(n):out=convolution(out,a,m)
    return out


@lru_cache(None)
def ahat(m):
    assert m<=10
    out=[Q(0)]*(m+1)
    for i,c in [(0,Q(1)),(2,Q(-1,24)),(4,Q(7,5760)),
                (6,Q(-31,967680)),(8,Q(127,154828800)),
                (10,Q(-73,3503554560))]:
        if i<=m:out[i]=c
    return out


@lru_cache(None)
def spin_indices(a,b,t):
    m=a+b
    assert (a+1+t)%2==0 and (b+1)%2==0
    if t==0:assert a%2==1 or a==0
    Ax=power(ahat(m),a+1,m)
    Ay=power(ahat(m),b+1-t,m)
    Af=power(ahat(m),t,m)
    characteristic={}
    for p,c in enumerate(Ax):
        for q,d in enumerate(Ay[:m+1-p]):
            if not(c and d):continue
            for k,e in enumerate(Af[:m+1-p-q]):
                if not e:continue
                for ell in range(k+1):
                    key=(p+ell,q+k-ell)
                    characteristic[key]=characteristic.get(key,Q(0))+c*d*e*comb(k,ell)
    E=[Q(0)]+[Q(1,factorial(k)) for k in range(1,m+1)]
    Ep=[power(E,i,m) for i in range(m+1)]
    def I(i):
        if i>a:return 0
        if t==0:return int(i==a)
        return (-1)**(a-i)*comb(t+a-i-1,a-i)
    result={}
    for i in range(m+1):
        for j in range(m+1-i):
            value=Q(0)
            for (p,q),c in characteristic.items():
                for k,ek in enumerate(Ep[i]):
                    ell=m-p-q-k
                    if 0<=ell<=m and ek and Ep[j][ell]:
                        value+=c*ek*Ep[j][ell]*I(p+k)
            assert value.denominator==1,(a,b,t,i,j,value)
            if value:result[i,j]=int(value)
    assert result.get((0,0),0)==0 # positive projective fibers imply PSC
    return result


def shift_unit(poly,axis,exponent):
    for _ in range(exponent):
        out=poly.copy()
        for ij,c in poly.items():
            if ij[axis]:
                key=list(ij);key[axis]-=1;key=tuple(key)
                out[key]=out.get(key,0)+c
        poly=out
    return poly


def all_spins(poly,index):
    out=[]
    for s0,s1 in product([0,2],repeat=2):
        p=shift_unit(shift_unit(poly,0,s0),1,s1)
        row=[0]*len(index)
        for ij,c in p.items():row[index[ij]]+=c
        out.append(row)
    return out


def bits(rows,number):
    diagonal=fmpz_mat([[r[i] for r in rows] for i in range(number)]).snf()
    values=[abs(int(diagonal[i,i])) for i in range(number)]
    assert all(v and not(v&(v-1)) for v in values)
    return sum(v.bit_length()-1 for v in values)


for N in range(1,6):
    m=2*N
    generators=[(i,j) for i in range(m+1) for j in range(m+1-i)]
    index={ij:k for k,ij in enumerate(generators)}
    relations=[]
    for i,j in generators:
        for axis in [0,1]:
            row=[0]*len(index)
            for shift,c in [(0,4),(1,6),(2,4),(3,1)]:
                ij=(i-shift,j) if axis==0 else (i,j-shift)
                if ij in index:row[index[ij]]+=c
            relations.append(row)
    geometry=[]
    for j in range(N):
        geometry+=all_spins(spin_indices(2*j+1,m-2*j-1,0),index)
    for r in range(N):
        raw=spin_indices(2*r+1,m-2*r-1,2)
        geometry+=all_spins(raw,index)
        # Include the factor swap, which supplies the opposite endpoint.
        geometry+=all_spins({(j,i):c for (i,j),c in raw.items()},index)
        # Independently verify the first two diagonals used in the proof.
        for i in range(m+1):
            expected=(-1)**(2*r+1-i)*(2*r+2-i) if i<=2*r+1 else 0
            assert raw.get((i,m-i),0)==expected
        for j in range(r+1):
            assert raw.get((2*j,m-1-2*j),0)%2==(r+1)%2
            assert raw.get((2*j+1,m-2-2*j),0)%2==(r+1-N)%2
    ambient=bits(relations,len(index))
    quotient=bits(relations+geometry,len(index))
    image=ambient-quotient
    print(f'N={N}, dimension={4*N+2}: ku ambient {ambient} bits, geometric image {image} bits')
    assert image==(4 if N==1 else 5*N),(N,image)
print('PASS: actual spin-index/Gysin images attain the expected complex kernel size through dimension22.')
