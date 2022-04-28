import math
from sympy import inverse_laplace_transform, exp
from re import split
# from sympy import latex,sympify,preview
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import sympy


import sympy


def around_num(num, num_after):
    return int(num * num_after) / num_after

def contains(s):
    return s.__contains__('*', '/', '**', '+', '-')

def ret_nums(s):
    count = 0
    integ = []
    l = len(s)
    i = 0
    while i < l:
        s_int = ''
        a = s[i]
        oper = s[i + 1]
        if oper.__contains__('*', '/', '**', '+', '-'):
            b = s[i + 2]
            while '0' <= b <= '9':
                result=eval(a+oper+b)
                i += 1
                if i < l:
                    a = s[i]
                    count += 1
                else:
                    break

        i += 1
        if s_int != '':
            integ.append(int(s_int))
    return integ

def ret_nums_2(s):
    s=split('<=|<|=>|>',s)
    s.remove('x')
    x=[around_num(N(ph),1000) for ph in s]
    return x

def ret_nums_1(s):
    l = len(s)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = s[i]
        if a.__contains__('p'):
            i += 2
            integ.append(math.pi)


        if a.__contains__('E'):
            i += 1
            integ.append(math.e)

        while '0' <= a <= '9' :
            s_int += a
            i += 1
            if i < l:
                a = s[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    return integ

s = 'E**2<=x<=2*pi'
ret_nums_2(s)
