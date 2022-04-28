from sympy import inverse_laplace_transform, exp
from re import split
# from sympy import latex,sympify,preview
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import sympy

def around_num(num, num_after):
    return int(num * num_after) / num_after

def dropComm(formul):
    index = formul.index(',')
    s1 = formul[:index]
    s2 = formul[index + 1:]
    return s1, s2


def dropDot(formul):
    index = formul.index('&')
    s1 = formul[:index]
    s2 = formul[index + 1:]
    return s1, s2


def build_first_last(st):
    x = sympy.Symbol('x')
    s1, s2 = dropComm(st)
    r = latex(sympify(s1)) + ", " + latex(sympify(s2))
    return r


def build_phrase(st):
    s1, s2 = dropComm(st)
    parts = split(r"([<>]=?)", s2)
    eq1 = "".join(parts[:3])
    eq2 = "".join(parts[-3:])
    eq2 = latex(sympify(eq2))
    eq2 = eq2[1:]
    r = latex(sympify(s1)) + ", " + latex(sympify(eq1)) + eq2
    return r


# expr = r"$F(x)=\begin{cases}f_1(x) & x = 0\\f_2(x) & x >=0 \end{cases}$"
def build_func(s, f):
    st = s.split('&')
    first = st[0]
    last = st[-1]
    st.remove(first)
    st.remove(last)

    s = fr"{build_first_last(first)}\\"
    for phrase in st:
        s += build_phrase(phrase) + r"\\"
    s += fr"{build_first_last(last)}"

    expr = fr"{f}(x)" \
           r"=\begin{cases}" \
           fr"{s}\\" \
           r" \end{cases}"
    return expr

    # preview(expr, viewer='file', filename='prim1.png')


def func_two_condition(st):
    func, con = dropComm(st[0])
    expr = eval(func)
    res_i = sympy.integrate(expr, x)
    res_i_l = res_i
    r = str(res_i_l) + ',' + con
    res = fr"{build_first_last(r)}\\"

    func, con = dropComm(st[1])
    expr = eval(func)
    res_i = sympy.integrate(expr, x)
    res_i_l = res_i
    r = str(res_i_l) + ',' + con
    res += fr"{build_first_last(r)}"
    expr = r"$f(x)=\begin{cases}" \
           fr"{res}\\" \
           r" \end{cases}$"

    preview(expr, viewer='file', filename='prim1.png')


def func_one_condition(st):
    func, con = dropComm(st[0])
    expr = eval(func)
    res_i = sympy.integrate(expr, x)
    res_i_l = res_i
    r = str(res_i_l) + ',' + con
    res = fr"{build_first_last(r)}"
    expr = r"$f(x)=\begin{cases}" \
           fr"{res}\\" \
           r" \end{cases}$"

    preview(expr, viewer='file', filename='prim1.png')


def work_input_F(s):
    Functions=list()

    functions = list()
    Values = list()
    st = s.split('&')
    if len(st) == 1:
        func_one_condition(st)
    if (len(st) == 2):
        func_two_condition(st)
    last = st[-1]
    st.remove(last)
    r = rf""
    for ph in st:
        func, con = dropComm(ph)

        functions.append(func)
        Values.append(con)

        expr = eval(func)
        res_i = sympy.integrate(expr, x)
        Functions.append(str(res_i))

        res_i_l = res_i
        r += str(res_i_l) + ',' + con + '&'
    func, con = dropComm(last)

    functions.append(func)
    Values.append(con)

    expr = eval(func)
    res_i = sympy.integrate(expr, x)
    Functions.append(str(res_i))

    res_i_l = res_i
    r += str(res_i_l) + ',' + con
    r += ""
    f = build_func(s, "f")
    F = build_func(r, "F")
    expr = "$" + f + "=>" + F + "$"
    preview(expr, viewer='file', filename='prim.png')
    return Functions,functions, Values

def work_input_f(s):
    Functions=list()
    functions = list()
    Values = list()
    st = s.split('&')
    if len(st) == 1:
        func_one_condition(st)
    if (len(st) == 2):
        func_two_condition(st)
    last = st[-1]
    st.remove(last)
    r = rf""
    for ph in st:
        func, con = dropComm(ph)

        functions.append(func)
        Values.append(con)

        expr = eval(func)
        res_i = sympy.diff(expr, x)
        Functions.append(str(res_i))

        res_i_l = res_i
        r += str(res_i_l) + ',' + con + '&'
    func, con = dropComm(last)

    functions.append(func)
    Values.append(con)

    expr = eval(func)
    res_i = sympy.diff(expr, x)
    Functions.append(str(res_i))

    res_i_l = res_i
    r += str(res_i_l) + ',' + con
    r += ""
    f = build_func(s, "F")
    F = build_func(r, "f(x)=F'")
    expr = "$" + f + "=>" + F + "$"
    preview(expr, viewer='file', filename='prim.png')
    return Functions,functions, Values


def ret_xy(s, begin=100, end=100, ):
    arr_x = np.linspace(begin+0.000001, end-0.000001)
    arr_y = list()
    for x in arr_x:
        arr_y.append(eval(s))
    arr_y = np.array(arr_y)
    return arr_x, arr_y


def ret_nums(s):
    # l = len(s)
    # integ = []
    # i = 0
    # while i < l:
    #     s_int = ''
    #     a = s[i]
    #     while '0' <= a <= '9':
    #         s_int += a
    #         i += 1
    #         if i < l:
    #             a = s[i]
    #         else:
    #             break
    #     i += 1
    #     if s_int != '':
    #         integ.append(int(s_int))
    # return integ
    s = split('<=|<|>=|>', s)
    s.remove('x')
    x = [around_num(N(ph), 1000) for ph in s]
    return x


# s = "0,x<1&1,x>1"
def createFirstx(F, v, check):
    x = ret_nums(v)[0]
    if check:
        x, y = ret_xy(F, begin=x - 100, end=x-0.00001)
    else:
        x, y = ret_xy(F, begin=x+0.00001, end=x + 100)
    return x, y

def create_xy(f,v):
    x1,x2=ret_nums(v)
    x,y=ret_xy(f,x1,x2)
    return x,y

def generation_To_arr(F, V):
    arr_x = list()
    arr_y = list()

    first_F, first_V = F[0], V[0]
    F.remove(first_F)
    V.remove(first_V)
    result = createFirstx(first_F,first_V, True)
    arr_x.append(result[0]), arr_y.append(result[1])

    last_F, last_V = F[-1], V[-1]
    F.remove(last_F)
    V.remove(last_V)

    for i in range(len(F)):
        F_,V_=F[i],V[i]
        result=create_xy(F_,V_)
        arr_x.append(result[0]),arr_y.append(result[1])


    result = createFirstx(last_F,last_V, False)
    arr_x.append(result[0]), arr_y.append(result[1])

    return arr_x,arr_y
    # for i in range(len(F)):

def build_plots(x,y,x_name,sname=''):
    axes1 = np.linspace(-100, 100)
    axes2 = [0] * len(axes1)
    plt.plot(axes1, axes2, color='k')
    plt.plot(axes2, axes1, color='k')
    plt.suptitle(sname)
    for i in range(len(x)):
        plt.plot(x[i],y[i],label=x_name[i])
    plt.legend()

    plt.grid()
    # plt.minorticks_on()
    # plt.grid(which='major')
    # plt.grid(which='minor')

    plt.show()


x = sympy.Symbol('x')
# s = "sin(x),x<1&pi**x/E,1<x<4&3,5<x<6&1,x>10"
#
# s1='0,x<=pi&-cos(x),pi<x<2*pi&0,x>2*pi'
# F, f,V = work_input_F(s1)
# x_1,y_1=generation_To_arr(F.copy(), V.copy())
# x_2,y_2=generation_To_arr(f.copy(),V.copy())
# build_plots(x_1,y_1,F,'F(x)')
# build_plots(x_2,y_2,f,'f(x)')
# #


# s = "0,x<=-pi/2&1/2*cos(x),-pi/2<x<pi/2&0,x>=pi/2"
