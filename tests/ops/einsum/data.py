from __future__ import absolute_import, division, print_function

import itertools

# These test cases were adapted from opt_einsum
# https://github.com/dgasmith/opt_einsum/blob/master/opt_einsum/tests/test_contract.py
# Copyright (c) 2014 Daniel Smith
EQUATIONS = [
    # Test hadamard-like products
    'a,ab,abc->abc',
    'a,b,ab->ab',

    # Test index-transformations
    'ea,fb,gc,hd,abcd->efgh',
    'ea,fb,abcd,gc,hd->efgh',
    'abcd,ea,fb,gc,hd->efgh',

    # Test complex contractions
    'acdf,jbje,gihb,hfac,gfac,gifabc,hfac->',
    'acdf,jbje,gihb,hfac,gfac,gifabc,hfac->',
    'cd,bdhe,aidb,hgca,gc,hgibcd,hgac->',
    'abhe,hidj,jgba,hiab,gab->',
    'bde,cdh,agdb,hica,ibd,hgicd,hiac->',
    'chd,bde,agbc,hiad,hgc,hgi,hiad->',
    'chd,bde,agbc,hiad,bdi,cgh,agdb->',
    'bdhe,acad,hiab,agac,hibd->',

    # Test collapse
    'ab,ab,c->',
    'ab,ab,c->c',
    'ab,ab,cd,cd->',
    'ab,ab,cd,cd->ac',
    'ab,ab,cd,cd->cd',
    'ab,ab,cd,cd,ef,ef->',

    # Test outer prodcuts
    'ab,cd,ef->abcdef',
    'ab,cd,ef->acdf',
    'ab,cd,de->abcde',
    'ab,cd,de->be',
    'ab,bcd,cd->abcd',
    'ab,bcd,cd->abd',

    # Random test cases that have previously failed
    'eb,cb,fb->cef',
    'dd,fb,be,cdb->cef',
    'bca,cdb,dbf,afc->',
    'dcc,fce,ea,dbf->ab',
    'fdf,cdd,ccd,afe->ae',
    'abcd,ad->bc',
    'ed,fcd,ff,bcf->be',
    'baa,dcf,af,cde->be',
    'bd,db,eac->ace',
    'fff,fae,bef,def->abd',
    'efc,dbc,acf,fd->abe',

    # Inner products
    'ab,ab->',
    'ab,ba->',
    'abc,abc->',
    'abc,bac->',
    'abc,cba->',

    # GEMM test cases
    'ab,bc->ac',
    'ab,cb->ac',
    'ba,bc->ac',
    'ba,cb->ac',
    'abcd,cd->ac',
    'abcd,ab->cd',
    'abcd,cdef->abef',
    'abcd,cdef->feba',
    'abcd,efdc->abef',

    # Inner than dot
    'aab,bc->ac',
    'ab,bcc->ac',
    'aab,bcc->ac',
    'baa,bcc->ac',
    'aab,ccb->ac',

    # Randomly build test caes
    'aab,fa,df,ecc->bde',
    'ecb,fef,bad,ed->ac',
    'bcf,bbb,fbf,fc->',
    'bb,ff,be->e',
    'bcb,bb,fc,fff->',
    'fbb,dfd,fc,fc->',
    'afd,ba,cc,dc->bf',
    'adb,bc,fa,cfc->d',
    'bbd,bda,fc,db->acf',
    'dba,ead,cad->bce',
    'aef,fbc,dca->bde',
]

# These test cases were added for Pyro
EQUATIONS.extend([
    '->',
    ',,,,->',
    'a->',
    'a->a',
    'a,a->a',
    ',a,a->a',
    'ij,jk,kl->il',
    'ea,fb,abcd,gc,hd->efgh',
])

# These are intended to be used by make_sahpes() below.
SIZES = [
    [2],
    [2, 3],
    [3, 2],
    [2, 3, 4],
    [2, 4, 3],
    [3, 2, 4],
    [3, 4, 2],
    [4, 2, 3],
    [4, 3, 2],
]


def make_shapes(equation, sizes):
    inputs, output = equation.split('->')
    inputs = inputs.split(',')
    symbols = sorted(set(output).union(*inputs))
    sizes = {dim: size for dim, size in zip(symbols, itertools.cycle(sizes))}
    shapes = [tuple(sizes[dim] for dim in input_) for input_ in inputs]
    return shapes


# This was recorded from running examples/hmm.py
LARGE = {
    'equation': (
        u'\xf0\xf1,\xef\xf0\xf1,\xee\xef\xf1,\xef\xf1,\xed\xee\xf1,\xee\xf1,'
        u'\xec\xed\xf1,\xed\xf1,\xeb\xec\xf1,\xec\xf1,\xea\xeb\xf1,\xeb\xf1,'
        u'\xe9\xea\xf1,\xea\xf1,\xe8\xe9\xf1,\xe9\xf1,\xe7\xe8\xf1,\xe8\xf1,'
        u'\xe6\xe7\xf1,\xe7\xf1,\xe5\xe6\xf1,\xe6\xf1,\xe4\xe5\xf1,\xe5\xf1,'
        u'\xe3\xe4\xf1,\xe4\xf1,\xe2\xe3\xf1,\xe3\xf1,\xe1\xe2\xf1,\xe2\xf1,'
        u'\xe0\xe1\xf1,\xe1\xf1,\xdf\xe0\xf1,\xe0\xf1,\xde\xdf\xf1,\xdf\xf1,'
        u'\xdd\xde\xf1,\xde\xf1,\xdc\xdd\xf1,\xdd\xf1,\xdb\xdc\xf1,\xdc\xf1,'
        u'\xda\xdb\xf1,\xdb\xf1,\xd9\xda\xf1,\xda\xf1,\xd8\xd9\xf1,\xd9\xf1,'
        u'\xd7\xd8\xf1,\xd8\xf1,\xd6\xd7\xf1,\xd7\xf1,\xd5\xd6\xf1,\xd6\xf1,'
        u'\xd4\xd5\xf1,\xd5\xf1,\xd3\xd4\xf1,\xd4\xf1,\xd2\xd3\xf1,\xd3\xf1,'
        u'\xd1\xd2\xf1,\xd2\xf1,\xd0\xd1\xf1,\xd1\xf1,\xcf\xd0\xf1,\xd0\xf1,'
        u'\xce\xcf\xf1,\xcf\xf1,\xcd\xce\xf1,\xce\xf1,\xcc\xcd\xf1,\xcd\xf1,'
        u'\xcb\xcc\xf1,\xcc\xf1,\xca\xcb\xf1,\xcb\xf1,\xc9\xca\xf1,\xca\xf1,'
        u'\xc8\xc9\xf1,\xc9\xf1,\xc7\xc8\xf1,\xc8\xf1,\xc6\xc7\xf1,\xc7\xf1,'
        u'\xc5\xc6\xf1,\xc6\xf1,\xc4\xc5\xf1,\xc5\xf1,\xc3\xc4\xf1,\xc4\xf1,'
        u'\xc2\xc3\xf1,\xc3\xf1,\xc1\xc2\xf1,\xc2\xf1,\xc0\xc1\xf1,\xc1\xf1,'
        u'Z\xc0\xf1,\xc0\xf1,YZ\xf1,Z\xf1,XY\xf1,Y\xf1,WX\xf1,X\xf1,VW\xf1,'
        u'W\xf1,UV\xf1,V\xf1,TU\xf1,U\xf1,ST\xf1,T\xf1,RS\xf1,S\xf1,QR\xf1,'
        u'R\xf1,PQ\xf1,Q\xf1,OP\xf1,P\xf1,NO\xf1,O\xf1,MN\xf1,N\xf1,LM\xf1,'
        u'M\xf1,KL\xf1,L\xf1,JK\xf1,K\xf1,IJ\xf1,J\xf1,HI\xf1,I\xf1,GH\xf1,'
        u'H\xf1,FG\xf1,G\xf1,EF\xf1,F\xf1,DE\xf1,E\xf1,CD\xf1,D\xf1,BC\xf1,'
        u'C\xf1,AB\xf1,B\xf1,zA\xf1,A\xf1,yz\xf1,z\xf1,xy\xf1,y\xf1,wx\xf1,'
        u'x\xf1,vw\xf1,w\xf1,uv\xf1,v\xf1,tu\xf1,u\xf1,st\xf1,t\xf1,rs\xf1,'
        u's\xf1,qr\xf1,r\xf1,pq\xf1,q\xf1,op\xf1,p\xf1,no\xf1,o\xf1,mn\xf1,'
        u'n\xf1,lm\xf1,m\xf1,kl\xf1,l\xf1,jk\xf1,k\xf1,ij\xf1,j\xf1,hi\xf1,'
        u'i\xf1,gh\xf1,h\xf1,fg\xf1,g\xf1,ef\xf1,f\xf1,de\xf1,e\xf1,cd\xf1,'
        u'd\xf1,bc\xf1,c\xf1,ab\xf1,b\xf1,a\xf1->\xf1'),
    'shapes': [
        (16, 8), (16, 16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 16, 8), (16, 8), (16, 16, 8), (16, 8),
        (16, 16, 8), (16, 8), (16, 8),
    ],
}
