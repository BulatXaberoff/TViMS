import matplotlib.figure
import wx
import wx.grid
import wx.xrc
import random
import numpy as np
from sympy import *
import re
# import print_DSV as dsv
import matplotlib.pyplot as plt
from PIL import Image
import sympy
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.gridspec import GridSpec
import print_DSV as dsv

check = False


class MyFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(1000, 800), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.count = 0
        self.panel = wx.Panel(self)

        menubar = wx.MenuBar()
        DSV = wx.Menu()
        itemDSV = DSV.Append(wx.ID_ANY, "Пустая колонка")
        DSV.Append(wx.ID_ANY, "1 пример")
        DSV.Append(wx.ID_ANY, "2 пример")

        NSV = wx.Menu()
        itemNSV = NSV.Append(wx.ID_ANY, "Пустая колонка")
        NSV.Append(wx.ID_ANY, "1 пример")
        NSV.Append(wx.ID_ANY, "2 пример")

        menubar.Append(DSV, "&DSV")
        menubar.Append(NSV, "&NSV")

        self.Bind(wx.EVT_MENU, self.onDSV, itemDSV)
        self.Bind(wx.EVT_MENU, self.onNSV, itemNSV)

        self.SetMenuBar(menubar)
        self.panel.Layout()

    def onTxT(self, event):
        self.lbl = wx.StaticText(self.panel, pos=(0, 50))
        self.lbl.LabelText = event.GetString()
        self.Layout()

    def onEditFormul(self, event):
        childrens = self.bxSizer.GetChildren()
        s = ""
        for child in childrens:
            widget = child.GetWindow()
            s += widget.GetValue()
        print(s)

    def onRemoveWidget(self, event):
        childrens = self.bxSizer.GetChildren()
        self.s = self.Rem(self.s)
        self.Show_Res(self.s)
        if self.bxSizer.GetChildren():
            self.bxSizer.Hide(self.count - 1)
            self.bxSizer.Remove(self.count - 1)
            self.count -= 1
            self.bxSizer.Layout()
        if self.count == 0:
            children = self.grb.GetChildren()
            for child in children:
                wid = child.GetWindow()
                if isinstance(wid, wx.StaticBitmap):
                    wid.Hide()
        self.grb.Layout()

    def onAddWidget(self, event):
        # self.new_txtctrl = wx.TextCtrl(self.panel, name=f"label {self.count + 1}", style=wx.TE_PROCESS_ENTER)
        # new_txtctrl.LabelText=f"{self.count+1}"
        self.bxSizer.Add(
            wx.TextCtrl(self.panel, id=self.count + 1, name=f"label {self.count + 1}", style=wx.TE_PROCESS_ENTER))
        # self.new_txtctrl.Bind(wx.EVT_TEXT_ENTER,lambda evt:self.onEditFormul(evt),id=self.count)

        self.count += 1
        if self.count == 1:
            self.Show_Res(self.s)
            return
        self.s = self.Add(self.s)
        self.Show_Res(self.s)
        self.grb.Layout()
        self.bxSizer.Layout()

    def Rem(self, expr):
        count = self.count
        expr = self.delEnd(expr)
        fragment = rf"\\f_{count}(x), & x \vee x_{count}"
        exp = expr.replace(fragment, " ")
        exp += r' \end{cases}$'
        return exp

    def delEnd(self, expr):
        words = expr.split(' ')
        fragment = r'\end{cases}$'
        new_words = []
        for word in words:
            if fragment not in word:
                new_words.append(word)
        return ' '.join(new_words)

    def Add(self, expr, val1=0, val2=0, check=True):
        count = self.count
        expr = self.delEnd(expr)
        expr += rf"\\f_{count}(x), & x \vee x_{count} "
        expr += r'\end{cases}$'
        return expr

    def Show_Res(self, expr):
        r = self.res + expr
        preview(r, viewer='file', filename='output3.png')

        self.sb.Hide()
        self.sb.Destroy()
        self.sb = wx.StaticBitmap(self.panel, -1, wx.Bitmap("output3.png"))
        # self.grb.Hide(3)
        # self.grb.Remove(3)
        self.grb.Add(self.sb, pos=(0, 0), span=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.grb.Layout()

    def onDSV(self, event):
        global check
        if check:
            while len(self.gr.GetChildren()) != 0:
                self.gr.Hide(len(self.gr.GetChildren()))
                self.gr.Remove(len(self.gr.GetChildren()))
            check = True

        self.gr = wx.GridBagSizer(8, 8)

        text = wx.StaticText(self.panel, label="Введите кол-во переменных")
        self.gr.Add(text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        txctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.gr.Add(txctrl, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.figure = matplotlib.figure.Figure()
        self.gs = self.figure.add_gridspec(2, 2)
        self.axes = self.figure.add_subplot(self.gs[:, 0])
        self.axes1 = self.figure.add_subplot(self.gs[:, 1])

        self.canvas = FigureCanvasWxAgg(self.panel, -1, self.figure)

        self.grid = wx.grid.Grid(self.panel, style=wx.TE_PROCESS_ENTER)
        self.grid.CreateGrid(1, 10)
        self.grid.Hide()

        self.gr.Add(self.canvas, pos=(0, 8), span=(8, 8), border=5)

        self.gr.Add(self.grid, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.Bind(wx.EVT_TEXT_ENTER, self.onParam, txctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.onGrid, self.grid)
        self.panel.SetSizer(self.gr)
        self.panel.Layout()

    def onNSV(self, event):
        global check
        if check:
            # while len(self.gr.GetChildren()) != 0:
            #     self.gr.Hide(len(self.gr.GetChildren()))
            #     self.gr.Remove(len(self.gr.GetChildren()))
            self.panel.DestroyChildren()
            check = True
        # self.panel=wx.Panel(self)
        self.res = r"$F(x)=\begin{cases}"
        self.s = \
            rf"f_{self.count + 1}(x),&x\vee x_{self.count + 1} " \
            r"\end{cases}$"

        # self.tx = wx.TextCtrl(self.panel)
        # self.Bind(wx.EVT_TEXT,self.onTxT,self.tx)
        self.grb = wx.GridBagSizer(4, 4)

        self.addbutton = wx.Button(self.panel, label="Добавить условие")
        self.deletebutton = wx.Button(self.panel, label="Удалить условие")
        self.grb.Add(self.addbutton, pos=(0, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.grb.Add(self.deletebutton, pos=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.bxSizer = wx.BoxSizer(wx.VERTICAL)
        self.grb.Add(self.bxSizer, pos=(0, 3), span=(3, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        # img = wx.Image("output1.png", type=wx.BITMAP_TYPE_ANY, index=-1)
        self.sb = wx.StaticBitmap(self.panel, -1, wx.Bitmap("output.png"))
        self.grb.Add(self.sb, pos=(0, 0), span=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.button = wx.Button(self.panel, label="Добавить")
        self.grb.Add(self.button, pos=(2, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.addbutton.Bind(wx.EVT_BUTTON, self.onAddWidget)
        self.deletebutton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
        self.button.Bind(wx.EVT_BUTTON, self.onEditFormul)
        self.panel.SetSizer(self.grb)
        self.panel.Layout()

    def onGrid(self, event):
        print("!")

    def _drawGraph(self, xvals, yvals):
        # !!!
        # Удалим предыдущий график, если он есть
        self.axes.clear()

        self.axes.clear()
        # Нарисуем новый график
        self.axes.plot(xvals, yvals)

        # Включим сетку
        self.axes.grid()

        # self.axes.legend([u"Gaussian"])

        self.canvas.draw()

    def _drawGraph1(self, xvals, yvals):
        # !!!
        # Удалим предыдущий график, если он есть
        self.axes1.clear()

        self.axes1.clear()
        # Нарисуем новый график
        self.axes1.plot(xvals, yvals)

        # Включим сетку
        self.axes1.grid()

        self.axes1.legend([u"Gaussian"])

        self.canvas.draw()

    def onParam(self, event):
        num = int(event.GetString())
        print(len(self.gr.GetChildren()))
        while len(self.gr.GetChildren()) != 3:
            self.gr.Hide(len(self.gr.GetChildren()) - 1)
            self.gr.Remove(len(self.gr.GetChildren()) - 1)

        self.grid.Destroy()
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(2, num)
        self.grid.SetRowLabelValue(0, "x_i")
        self.grid.SetRowLabelValue(1, "p_i")
        for i in range(num):
            self.grid.SetColLabelValue(i, f"{i + 1}")
        self.gr.Add(self.grid, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        but1 = wx.Button(self.panel)
        but1.Label = "Заполнить величины"
        self.gr.Add(but1, pos=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        but2 = wx.Button(self.panel)
        but2.Label = "Вычислить"
        self.gr.Add(but2, pos=(4, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.panel.SetSizer(self.gr)
        self.panel.Layout()
        self.Bind(wx.EVT_BUTTON, self.onBut1, but1)
        self.Bind(wx.EVT_BUTTON, self.onBut2, but2)

    def onBut1(self, event):
        size = self.grid.GetNumberCols()
        arr_x = random.sample(range(10 + size), size)
        arr_x.sort()
        for i in range(size):
            self.grid.SetCellValue(0, i, str(arr_x[i]))
        for i in range(size):
            self.grid.SetCellValue(1, i, str(0))
        self.arr_x = np.array(arr_x)

    def onBut2(self, event):
        print(len(self.gr.GetChildren()))
        if len(self.gr.GetChildren()) == 9:
            self.gr.Hide(8)
            self.gr.Remove(8)
        if len(self.gr.GetChildren()) == 8:
            self.gr.Hide(7)
            self.gr.Remove(7)
            self.gr.Hide(6)
            self.gr.Remove(6)
            self.Layout()
        arr_p = list()
        self.arr_x = list()
        try:
            for i in range(self.grid.GetNumberCols()):
                self.arr_x.append(float(self.grid.GetCellValue(0, i)))
            for i in range(self.grid.GetNumberCols()):
                arr_p.append(float(self.grid.GetCellValue(1, i)))
        except:
            print("nope")
            return

        arr_p = np.array(arr_p)
        self.arr_p = arr_p
        if arr_p.sum() != 1:
            print("Неверно")
            return

        x, p = self.arr_x, arr_p
        # M_X = dsv.M_X(x, p)[1]
        # D_X = dsv.D_X(x, p)[1]
        # Std = dsv.S_X(x, p)[1]
        M_X = 1
        D_X = 2
        Std = 3
        stattxt = wx.StaticText(self.panel)
        stattxt.LabelText = f"{M_X}-мат.ожидание\n{D_X}-дисперсия\n{Std}-стандартное отклонение"
        self._drawGraph(self.arr_x, arr_p)

        # bmp = wx.Bitmap("why.jpg")
        # bmp = self.scale_bitmap(bmp, 40, 40)
        stb = wx.Button(self.panel, size=(50, 50), name="button")
        # stb.SetBitmap(bmp)

        arr_F = list()
        arr_F.append(0)
        for el in range(len(arr_p)):
            sum = 0
            if el == 0:
                continue
            for i in range(el):
                sum += arr_p[i]
            arr_F.append(sum)
        arr_F.append(1)
        x = self.arr_x.copy()
        y = arr_F.copy()
        x.append(x[-1] + 5)
        # f_x = dsv.F_X(x, p)[0]
        self._drawGraph1(x, x)
        fig = plt.figure(figsize=(15, 6))
        gs = GridSpec(ncols=2, nrows=2, figure=fig)
        ax1 = plt.subplot(gs[:, 0])
        ax1.step(x, y, 'r--o', linewidth=3)
        ax1.grid()
        ax1.spines['left'].set_position('center')
        ax1.spines['bottom'].set_position('center')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        ax2 = fig.add_subplot(gs[:, 1])
        ax2.plot(self.arr_x, arr_p, 'b--o', linewidth=3)
        ax2.grid()
        ax2.spines['left'].set_position('center')
        ax2.spines['bottom'].set_position('center')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        fig.show()

        img = wx.Image("output1.png", type=wx.BITMAP_TYPE_ANY, index=-1)
        sb = wx.StaticBitmap(self.panel, -1, wx.Bitmap(img))

        self.gr.Add(stattxt, pos=(5, 0), flag=wx.LEFT | wx.BOTTOM, border=5)
        self.gr.Add(stb, pos=(5, 1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.gr.Add(sb, pos=(6, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.gr.Layout()
        self.Bind(wx.EVT_BUTTON, self.onWhyButt, stb)

    def __del__(self):
        pass

    def scale_bitmap(self, bitmap, width, height):
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result

    def onWhyButt(self, event):
        print(len(self.gr.GetChildren()))
        while len(self.gr.GetChildren()) != 8:
            self.gr.Hide(len(self.gr.GetChildren()) - 1)
            self.gr.Remove(len(self.gr.GetChildren()) - 1)
        x = self.arr_x
        p = self.arr_p
        #
        # expr = rf"${M_X(x, p)[0]}" \
        #        r"\\" \
        #        rf"{D_X(x, p)[0]}" \
        #        r"\\\\" \
        #        rf"{S_X(x, p)[0]}$"
        # sympy.preview(expr, viewer='file', filename='output.png')
        dsv.Show(x, p)
        img = wx.Image("output.png", type=wx.BITMAP_TYPE_ANY, index=-1)
        sb = wx.StaticBitmap(self.panel, -1, wx.Bitmap(img))
        self.gr.Add(sb, pos=(6, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.gr.Layout()

    def resize_image(self, input_image_path,
                     output_image_path,
                     size):
        original_image = Image.open(input_image_path)
        resized_image = original_image.resize(size)
        return


# app = wx.App()
# wnd = MyFrame(None)
# wnd.Show()
# app.MainLoop()


#
def dropComm(formul):
    index = formul.index(',')
    s1 = formul[:index]
    s2 = formul[index + 1:]
    return s1, s2


def dropDot(formul):
    index = formul.index('.')
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
    parts = re.split(r"([<>]=?)", s2)
    eq1 = "".join(parts[:3])
    eq2 = "".join(parts[-3:])
    eq2 = latex(sympify(eq2))
    eq2 = eq2[1:]
    r = latex(sympify(s1)) + ", " + latex(sympify(eq1)) + eq2
    return r


# expr = r"$F(x)=\begin{cases}f_1(x) & x = 0\\f_2(x) & x >=0 \end{cases}$"
def build_func(s):
    st = s.split('.')
    first = st[0]
    last = st[-1]
    st.remove(first)
    st.remove(last)

    s = fr"{build_first_last(first)}\\"
    for phrase in st:
        s += build_phrase(phrase) + r"\\"
    s += fr"{build_first_last(last)}"

    print(st)
    expr = r"$F(x)=\begin{cases}" \
           fr"{s}\\" \
           r" \end{cases}$"

    preview(expr, viewer='file', filename='prim1.png')


s = "sin(x),x<1.e**x,1<x<4.3,5<x<6.1,x>10"
# build_func(s)

# x=sympy.Symbol('x')
# st = "sin(x)**2,1<x<10"

st = s.split('.')
pr = st[0]
s1 = dropComm(st[0])[0]
print(s1)

r = rf"$"
x = sympy.Symbol('x')
s = "x**2"
expr = eval(s)
integ_def = latex(Integral(eval(s), x))
r += rf"{integ_def} = "

res_i = sympy.integrate(expr, x)
res_i_l = latex(res_i)
r += res_i_l

r += "$"

preview(r, viewer='file', filename='prim.png')
