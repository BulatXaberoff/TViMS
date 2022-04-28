import numpy as np
import sympy


def cdot(s):
    return f"\cdot{s}"


def M_X(x, p):
    res = 0
    str = "M(X)=\sum_{i=1}^{\infty} x_ip_i = "
    for i in range(len(x)):
        res += x[i] * p[i]
        str += f"{x[i]}{cdot(p[i])}+"
        if i == len(x) - 1:
            str = str[:-1]
            str += "= "
    str += f"{int(res * 1000) / 1000}"
    return str, res


def D_X(x, p):
    d_x = 0
    res = 0
    str = r"\\M(X^{2})=\sum_{i=1}^{\infty}x_1^2\cdot{p_1}+x_2^2\cdot{p_2}+...+x_n^2\cdot{p_n}=\\="
    for i in range(len(x)):
        res += np.power(x[i], 2) * p[i]
        if x[i] < 0:
            str += f"({x[i]})^2{cdot(p[i])}+"
        else:
            str += f"{x[i]}^2{cdot(p[i])}+"
        if i == len(x) - 1:
            str = str[:-1]
            str += "= "
    m_x = int(M_X(x, p)[1] * 1000) / 1000
    d_x = res - np.power(m_x, 2)
    if m_x < 0:
        str += f"{int(res * 1000) / 1000}" \
               r"\\" \
               r"D(X)=M(X^{2})-(M(X))^{2}=" \
               f"{res}-({m_x})^2={d_x}"

        return str, d_x

    str += f"{int(res * 1000) / 1000}" \
           r"\\" \
           r"D(X)=M(X^{2})-(M(X))^{2}=" \
           f"{res}-{m_x}^2={d_x}"
    return str, d_x


def S_X(x, p):
    s = "\sigma{(X)}=\sqrt{D(x)}="
    s_x = int(np.sqrt(D_X(x, p)[1]) * 1000) / 1000
    s += f"{s_x}"
    return s, s_x


def Show(x, p):
    expr = rf"${M_X(x, p)[0]}" \
           r"\\" \
           rf"{D_X(x, p)[0]}" \
           r"\\\\" \
           rf"{S_X(x, p)[0]}$"
    sympy.preview(expr, viewer='file', filename='output.png')


def F_X(x, p):
    s = r"F(x)=\begin{cases}" \
        rf"0, & x \leq {x[0]}\\"
    arr_F = list()
    arr_F.append(0)
    for el in range(len(p)):
        sum = 0
        if el == 0:
            continue
        for i in range(el):
            sum += p[i]
        arr_F.append(int(sum*1000)/1000)

        s += fr"{sum}, & {x[el - 1]}<x\leq{x[el]} \\"

    arr_F.append(1)
    s += fr"1, & x > {x[-1]} " \
         r"\end{cases}"
    expr = rf"${s}$\\"
    sympy.preview(expr, viewer='file', filename='output1.png')
    return arr_F, s


# x = [-2, 0, 3, 7]
# p = [0.4, 0.1, 0.3, 0.2]
# expr = r"$F(x)=\begin{cases}a & x \leq 0\\b & x > 0\end{cases}$"
# expr = rf"${F_X(x, p)[1]}$"
# sympy.preview(expr, viewer='file', filename='output1.png')
# arr_x=[12,9,8,14,15,11,10,15]
# arr_y=[42,107,100,60,78,79,90,54]
# Show(arr_x,arr_y)
