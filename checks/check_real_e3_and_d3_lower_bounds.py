#!/usr/bin/env python3
"""Exact F2 real E3 and exhibited R3*d3ku ranks, independent of c-lift claims."""
from functools import lru_cache
from itertools import product


def xor_into(d,key):
    if key in d:d.remove(key)
    else:d.add(key)


def monomial(c0,c1,l0=0,l1=0):
    return (c0[0],c1[0],c0[1]+l0,c1[1]+l1)


def chain(e,z):
    if z==0:
        assert e==1
        return (1,0),0
    return (e,z if z%2 else z-1),int(z%2==0)


def cdegree(c):return c[0]+2*c[1]


@lru_cache(None)
def chains(maximum):
    return ((1,0),)+tuple((e,z) for e in [0,1]
        for z in range(1,maximum//2+1,2) if e+2*z<=maximum)


@lru_cache(None)
def real_basis(n,s):
    if n<2 or s<0:return ()
    out=[]
    for c0,c1 in product(chains(n),repeat=2):
        if c0==c1==(1,0):continue
        for side in ([0,1] if c0[1] and c1[1] else [0]):
            d=cdegree(c0)+cdegree(c1)+2*side
            if n>=d and (n-d)%2==0:
                v=(n-d)//2
                if v<=s:out.append(('b',c0,c1,side,v,s-v))
    for m in range(n//8+1):
        for kind,d,f in [('m',2+8*m,4*m),('w',6+8*m,3+4*m)]:
            if n==d and s>=f:out.append(('c',kind,m,s-f))
        for kind,d,f in [('eta',3+8*m,1+4*m),('eta2',4+8*m,2+4*m)]:
            if (n,s)==(d,f):out.append(('c',kind,m,0))
    return tuple(out)


@lru_cache(None)
def ku_basis(n,s):
    if n<2 or s<0:return ()
    out=[]
    for v in range(s+1):
        ordinary=n-2*v
        for e0,e1 in product(range(2),repeat=2):
            remain=ordinary-e0-e1
            if remain<0 or remain%2:continue
            for z0 in range(remain//2+1):
                z1=remain//2-z0
                if e0+z0 and e1+z1:
                    out.append((s-v,v,e0,e1,z0,z1))
    return tuple(out)


def ku_d2(m):
    h,v,e0,e1,z0,z1=m
    out=set()
    if not e0 and z0:
        xor_into(out,(h+2,v,1,e1,z0-1,z1))
        if z0>=2:xor_into(out,(h+1,v+1,1,e1,z0-2,z1))
    if not e1 and z1:
        xor_into(out,(h+2,v,e0,1,z0,z1-1))
        if z1>=2:xor_into(out,(h+1,v+1,e0,1,z0,z1-2))
    return out


def R(m):
    h,v,e0,e1,z0,z1=m
    c0,l0=chain(e0,z0);c1,l1=chain(e1,z1)
    if c0==c1==(1,0):
        q,r=divmod(v,4)
        if r==0:return set()
        if r==1:return {('c','m',q,h+1)}
        if r==2:return {('c','eta2',q,0)} if h==0 else set()
        return {('c','w',q,h)}
    def bow(side,v,h):return ('b',c0,c1,side,v,h)
    out=set()
    if not(c0[1] and c1[1]):
        if l0+l1:
            out.add(bow(0,v,h))
        elif v%2:
            out.add(bow(0,v-1,h+1))
    else:
        if (l0,l1)==(0,0):
            if v%2:out.add(bow(0,v-1,h+1))
        elif (l0,l1)==(1,0):out.add(bow(0,v,h))
        elif (l0,l1)==(0,1):
            out.add(bow(0,v,h))
            if v%2:out.add(bow(1,v-1,h+1))
        else:out.add(bow(1,v,h))
    return out


def real_d2(key):
    if key[0]=='c':return set()
    _,c0,c1,side,v,h=key
    if c0[1] and c1[1]:
        levels=(1,side)
    else:levels=(int(bool(c0[1])),int(bool(c1[1])))
    preimage=(h,v,*monomial(c0,c1,*levels))
    out=set()
    for term in ku_d2(preimage):
        for image in R(term):xor_into(out,image)
    return out


def encode(terms,basis):
    index={m:i for i,m in enumerate(basis)}
    out=0
    for term in terms:out^=1<<index[term]
    return out


@lru_cache(None)
def columns(theory,n,s):
    basis=real_basis if theory=='r' else ku_basis
    differential=real_d2 if theory=='r' else ku_d2
    return tuple(encode(differential(m),basis(n-1,s+2)) for m in basis(n,s))


def elimination(vectors):
    pivots={}
    for i,vector in enumerate(vectors):
        provenance=1<<i
        for k in sorted(pivots,reverse=True):
            if vector>>k&1:
                v,p=pivots[k];vector^=v;provenance^=p
        if vector:pivots[vector.bit_length()-1]=(vector,provenance)
    return pivots


def kernel(vectors):
    pivots={};answer=[]
    for i,vector in enumerate(vectors):
        provenance=1<<i
        for k in sorted(pivots,reverse=True):
            if vector>>k&1:
                v,p=pivots[k];vector^=v;provenance^=p
        if vector:pivots[vector.bit_length()-1]=(vector,provenance)
        else:answer.append(provenance)
    return answer


@lru_cache(None)
def e3(theory,n,s):
    out=columns(theory,n,s)
    incoming=columns(theory,n+1,s-2) if s>=2 else ()
    for vector in incoming:
        check=0
        for i,column in enumerate(out):
            if vector>>i&1:check^=column
        assert check==0,('d2square',theory,n,s)
    pivots={}
    def reduce(vector):
        coordinate=0
        for k in sorted(pivots,reverse=True):
            if vector>>k&1:
                v,c=pivots[k];vector^=v;coordinate^=c
        return vector,coordinate
    for vector in incoming:
        vector,_=reduce(vector)
        if vector:pivots[vector.bit_length()-1]=(vector,0)
    representatives=[]
    for vector in kernel(out):
        residual,coordinate=reduce(vector)
        if residual:
            tag=1<<len(representatives)
            pivots[residual.bit_length()-1]=(residual,tag^coordinate)
            representatives.append(vector)
    def project(vector):
        residual,coordinate=reduce(vector)
        assert residual==0,('notcycle',theory,n,s)
        return coordinate
    return len(representatives),project


def gamma(a,b,v=0):
    terms={(1,v,1,0,a-1,b),(1,v,0,1,a,b-1)}
    if a>=2:xor_into(terms,(0,v+1,1,0,a-2,b))
    if b>=2:xor_into(terms,(0,v+1,0,1,a,b-2))
    return terms


def R_terms(terms):
    out=set()
    for term in terms:
        for image in R(term):xor_into(out,image)
    return out


@lru_cache(None)
def lower_rank(n,s):
    if s<=0 or n%2==0:return 0
    value=n-2*s+5
    if value%2:return 0
    total=value//2
    target_basis=real_basis(n-1,s+3)
    _,target_project=e3('r',n-1,s+3)
    _,source_project=e3('r',n,s)
    images=[];source_images=[]
    for a in range(1,total):
        b=total-a
        source=R_terms(gamma(a,b,s-1))
        source_images.append(source_project(encode(source,real_basis(n,s))))
        target=set()
        for j,k in [(a-2,b-4),(a-4,b-2)]:
            if min(j,k)>=0:xor_into(target,(0,s+3,1,1,j,k))
        image=R_terms(target)
        images.append(target_project(encode(image,target_basis)))
    for relation in kernel(source_images):
        image=0
        for i,column in enumerate(images):
            if relation>>i&1:image^=column
        assert image==0,('R3d3notwell-defined',n,s)
    return len(elimination(images))


def rho(n,s):
    if s<=0 or n%2==0:return 0
    if (n-2*s+3)%2:return 0
    A=(n-2*s+3)//2
    if A==5 and s%4==1:return 0
    if A>=5 and A%2:return (A-3)//2
    if A>=8 and A%2==0:return (A-6)//2
    return 0


for n in range(2,32):
    e3_total=0;lower_total=0
    for s in range(n//2+8):
        dimension,_=e3('r',n,s)
        e3_total+=dimension
        exhibited=lower_rank(n,s)
        old=rho(n,s)
        assert exhibited==old,('rank-mismatch',n,s,exhibited,old)
        lower_total+=exhibited
    print(f'n={n:2}: realE3bits={e3_total:3}; exhibitedR3d3-rank={lower_total:3}')
print('PASS: actual R2/d2 construction; d2 squared zero; exhibited ranks equal rho through stem31.')
