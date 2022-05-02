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
from sympy import inverse_laplace_transform, exp
import convertStrFunc as convF
from matplotlib.ticker import MultipleLocator

check = False


class MyFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(1000, 800), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.count = 0
        self.panel = wx.Panel(self)
        self.boxS = wx.BoxSizer(wx.VERTICAL)
        self.checkBox = False
        self.panel.SetSizer(self.boxS)

        menubar = wx.MenuBar()
        DSV = wx.Menu()
        itemDSV = DSV.Append(wx.ID_ANY, "Пустая колонка")
        DSV.Append(3, "1 пример")
        DSV.Append(4, "2 пример")

        NSV = wx.Menu()
        itemNSV = NSV.Append(wx.ID_ANY, "Пустая колонка")
        NSV.Append(1, "1 пример")
        NSV.Append(2, "2 пример")
        NSV.Append(5, "3 пример")

        menubar.Append(DSV, "&DSV")
        menubar.Append(NSV, "&NSV")

        self.Bind(wx.EVT_MENU, self.onDSV, itemDSV)
        self.Bind(wx.EVT_MENU, self.onEx_1_DSV, id=3)
        self.Bind(wx.EVT_MENU, self.onEx_2_DSV, id=4)

        self.Bind(wx.EVT_MENU, self.onNSV, itemNSV)
        self.Bind(wx.EVT_MENU, self.onEx_1_NSV, id=1)
        self.Bind(wx.EVT_MENU, self.onEx_2_NSV, id=2)
        self.Bind(wx.EVT_MENU, self.onEx_3_NSV, id=5)

        self.SetMenuBar(menubar)
        self.panel.Layout()

    def onEx_1_DSV(self, event):
        self.create_DSV_Design()
        x = [-2,0,3,7]
        p = [0.4,0.1,0.3,0.2]
        self.create_example_DSV(p, x)

    def create_example_DSV(self, p, x):
        num = len(x)
        print(len(self.gr.GetChildren()))
        while len(self.gr.GetChildren()) != 3:
            self.gr.Hide(len(self.gr.GetChildren()) - 1)
            self.gr.Remove(len(self.gr.GetChildren()) - 1)
        self.txctrl.SetLabel(str(num))
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(2, num)
        self.grid.SetRowLabelValue(0, "x_i")
        self.grid.SetRowLabelValue(1, "p_i")
        for i in range(num):
            self.grid.SetColLabelValue(i, f"{i + 1}")
            self.grid.SetCellValue(0, i, str(x[i]))
            self.grid.SetCellValue(1, i, str(p[i]))
        self.gr.Add(self.grid, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        but1 = wx.Button(self.panel)
        but1.Label = "Заполнить величины"
        self.gr.Add(but1, pos=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        but2 = wx.Button(self.panel)
        but2.Label = "Вычислить"
        self.gr.Add(but2, pos=(4, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        # self.boxS.Add(self.gr)
        # self.panel.SetSizer(self.boxS)
        self.boxS.Layout()
        # self.panel.Layout()
        self.Bind(wx.EVT_BUTTON, self.onBut1, but1)
        self.Bind(wx.EVT_BUTTON, self.onBut2, but2)

    def onEx_2_DSV(self, event):
        self.create_DSV_Design()
        x = [12,16,21,26,30]
        p = [0.2,0.1,0.4,0.2,0.1]
        self.create_example_DSV(p,x)

    def onEx_1_NSV(self, event):
        if self.checkBox:
            print(len(self.boxS.GetChildren()))
            while len(self.boxS.GetChildren()) != 0:
                self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
                self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        self.checkBox = True

        s = '0,x<=-1&1/2+1/pi*asin(x),-1<=x<=1&1,x>=1'
        self.res = '$Func(x)=\\begin{cases}'
        self.s = 'f_1(x),&x\\vee x_1\\\\f_2(x), & x \\vee x_2\\\\f_3(x), & x \\vee x_3 \\end{cases}$'
        r = ['0,x<=-1&', '1/2+1/pi*asin(x),-1<=x<=1&', '1,x>=1']
        self.count = 3
        self.CreateNSVDesign()
        self.Show_Res(self.s)
        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()

        for i in range(self.count):
            txt = wx.TextCtrl(self.panel, id=i + 1,
                              name=f"label {i + 1}", style=wx.TE_PROCESS_ENTER)
            self.bxSizer.Add(txt)
            txt.Label = r[i]

        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()

    def onEx_2_NSV(self, event):
        if self.checkBox:
            print(len(self.boxS.GetChildren()))
            while len(self.boxS.GetChildren()) != 0:
                self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
                self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        self.checkBox = True
        s = '0,x<-pi/2&1/2*cos(x),-pi/2<x<pi/2&0,x>=pi/2'
        self.res = '$Func(x)=\\begin{cases}'
        self.s = 'f_1(x),&x\\vee x_1\\\\f_2(x), & x \\vee x_2\\\\f_3(x), & x \\vee x_3 \\end{cases}$'
        r = ['0,x<-pi/2&', '1/2*cos(x),-pi/2<x<pi/2&', '0,x>=pi/2']
        self.count = 3
        self.CreateNSVDesign()
        self.Show_Res(self.s)
        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()

        for i in range(self.count):
            txt = wx.TextCtrl(self.panel, id=i + 1,
                              name=f"label {i + 1}", style=wx.TE_PROCESS_ENTER)
            self.bxSizer.Add(txt)
            txt.Label = r[i]

        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()
    def onEx_3_NSV(self,event):
        if self.checkBox:
            print(len(self.boxS.GetChildren()))
            while len(self.boxS.GetChildren()) != 0:
                self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
                self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        self.checkBox = True
        s = '0,x<-1&3/(4-x**2),-1<=x<=1&0,x>1'
        self.res = '$Func(x)=\\begin{cases}'
        self.s = 'f_1(x),&x\\vee x_1\\\\f_2(x), & x \\vee x_2\\\\f_3(x), & x \\vee x_3 \\end{cases}$'
        r = ['0,x<-1&', '3/(4-x**2),-1<=x<=1&', '0,x>1']
        self.count = 3
        self.CreateNSVDesign()
        self.Show_Res(self.s)
        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()

        for i in range(self.count):
            txt = wx.TextCtrl(self.panel, id=i + 1,
                              name=f"label {i + 1}", style=wx.TE_PROCESS_ENTER)
            self.bxSizer.Add(txt)
            txt.Label = r[i]

        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()

    def onTxT(self, event):
        self.lbl = wx.StaticText(self.panel, pos=(0, 50))
        self.lbl.LabelText = event.GetString()
        self.Layout()

    def onEditFormul(self, event):
        print(len(self.boxS.GetChildren()))
        while len(self.boxS.GetChildren()) != 1:
            self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
            self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        childrens = self.bxSizer.GetChildren()
        s = ""
        info = event.GetString()
        if info == 'Задать как F(x) и найти f(x)':
            for child in childrens:
                widget = child.GetWindow()
                s += widget.GetValue()
            convF.work_input_f(s)
            self.btm = wx.StaticBitmap(self.panel, -1, wx.Bitmap("prim.png"))
            self.boxS.Add(self.btm, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            f, F, V = convF.work_input_f(s)
            x_1, y_1 = convF.generation_To_arr(F.copy(), V.copy())
            x_2, y_2 = convF.generation_To_arr(f.copy(), V.copy())
            convF.print_solvingMxDx(f.copy(), V)
            self.boxS.Add(wx.StaticBitmap(self.panel, -1, wx.Bitmap("p.png")),
                          0, wx.ALIGN_CENTER | wx.ALL, 5)
            # convF.build_plots(x_2, y_2, f, 'f(x)')
            self.boxS.Layout()
            self.Layout()
            self.panel.Layout()
            convF.build_plots(x_1, y_1, F.copy(), "F(x)", x_2, y_2, f.copy(), 'f(x)')

        if info == 'Задать как f(x) и найти F(x)':
            for child in childrens:
                widget = child.GetWindow()
                s += widget.GetValue()
            convF.work_input_F(s)
            self.btm = wx.StaticBitmap(self.panel, -1, wx.Bitmap("prim.png"))
            self.boxS.Add(self.btm, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            F, f, V = convF.work_input_F(s)
            x_1, y_1 = convF.generation_To_arr(F.copy(), V.copy())
            x_2, y_2 = convF.generation_To_arr(f.copy(), V.copy())
            # convF.build_plots(x_1, y_1, F, 'F(x)')
            # convF.build_plots(x_2, y_2, f, 'f(x)')
            convF.print_solvingMxDx(f.copy(), V)
            self.boxS.Add(wx.StaticBitmap(self.panel, -1, wx.Bitmap("p.png")),
                          0, wx.ALIGN_CENTER | wx.ALL, 5)
            self.boxS.Layout()
            self.Layout()
            self.panel.Layout()
            convF.build_plots(x_2, y_2, f.copy(), 'f(x)', x_1, y_1, F.copy(), "F(x)")

    def onRemoveWidget(self, event):
        while len(self.boxS.GetChildren()) != 1:
            self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
            self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
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
        while len(self.boxS.GetChildren()) != 1:
            self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
            self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        self.bxSizer.Add(
            wx.TextCtrl(self.panel, id=self.count + 1, name=f"label {self.count + 1}", style=wx.TE_PROCESS_ENTER))
        # self.new_txtctrl.Bind(wx.EVT_TEXT_ENTER,lambda evt:self.onEditFormul(evt),id=self.count)

        self.count += 1
        if self.count == 1:
            self.Show_Res(self.s)
            return
        self.s = self.Add(self.s)
        self.Show_Res(self.s)
        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()
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
        self.boxS.Layout()
        self.Layout()
        self.panel.Layout()
        self.bxSizer.Layout()

    def onDSV(self, event):
        self.create_DSV_Design()

    def create_DSV_Design(self):
        if self.checkBox:
            print(len(self.boxS.GetChildren()))
            while len(self.boxS.GetChildren()) != 0:
                self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
                self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        self.checkBox = True
        self.gr = wx.GridBagSizer(8, 8)
        self.boxS.Add(self.gr)
        text = wx.StaticText(self.panel, label="Введите кол-во переменных")
        self.gr.Add(text, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.txctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.gr.Add(self.txctrl, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.figure = matplotlib.figure.Figure(figsize=(8, 4))
        # self.axes1 = self.figure.add_subplot()
        self.gs = self.figure.add_gridspec(2, 2)
        self.axes = self.figure.add_subplot(self.gs[:, 0])
        self.axes1 = self.figure.add_subplot(self.gs[:, 1])
        # self.build_canvas1()
        # self.build_canvas2()
        self.canvas = FigureCanvasWxAgg(self.panel, -1, self.figure)
        self.grid = wx.grid.Grid(self.panel, style=wx.TE_PROCESS_ENTER)
        self.grid.CreateGrid(1, 10)
        self.grid.Hide()
        self.gr.Add(self.canvas, pos=(0, 8), span=(8, 8), border=5)
        self.gr.Add(self.grid, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.Bind(wx.EVT_TEXT_ENTER, self.onParam, self.txctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.onGrid, self.grid)
        self.panel.SetSizer(self.boxS)
        self.panel.Layout()

    def pos_arr(self, _x, first_el, last_el):
        m1 = [first_el]
        for e in _x:
            m1.append(e)
        m1.append(last_el)
        return m1

    def build_canvas1(self, arr_p, x, y):
        self.axes.clear()
        self.axes.clear()
        axes1 = np.linspace(-100, 100)
        axes2 = [0] * len(axes1)
        ax = self.axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.plot(axes1, axes2, color='k')
        ax.plot(axes2, axes1, color='k')
        x_ = x.copy()
        y_ = y.copy()
        x_ = self.pos_arr(x_, min(x) - 10, max(x) + 10)
        y_ = self.pos_arr(y_, min(y), max(y))
        ax.step(x_, y_, 'r--o', label='F(x)')
        ax.legend()
        ax.grid()
        ax.set_ylim(-0.1, 1.2)
        ax.set_xlim(min(x) - 2, max(x) + 2)
        self.axes = ax
        self.canvas.draw()

    def build_canvas2(self, arr_p, x, y):
        self.axes1.clear()
        self.axes1.clear()
        axes1 = np.linspace(-100, 100)
        axes2 = [0] * len(axes1)
        ax1 = self.axes1
        # ax1.xaxis.set_major_locator(MultipleLocator(base=1))
        ax1.set_xlabel('X')
        ax1.plot(axes1, axes2, color='k')
        ax1.plot(axes2, axes1, color='k')
        ax1.plot(self.arr_x, arr_p, 'b--o', label='f(x)')
        ax1.legend()
        ax1.grid()
        ax1.set_ylim(-0.1, 1.2)
        ax1.set_xlim(min(x) - 2, max(x) + 2)
        self.axes1 = ax1
        self.canvas.draw()

    def onNSV(self, event):
        if self.checkBox:
            while len(self.boxS.GetChildren()) != 0:
                self.boxS.Hide(len(self.boxS.GetChildren()) - 1)
                self.boxS.Remove(len(self.boxS.GetChildren()) - 1)
        self.checkBox = True
        global check
        if check:
            self.panel.DestroyChildren()
            check = True
        # self.panel=wx.Panel(self)
        self.CreateNSVDesign()
        self.res = r"$Func(x)=\begin{cases}"
        self.s = \
            rf"f_{self.count + 1}(x),&x\vee x_{self.count + 1} " \
            r"\end{cases}$"

    def CreateNSVDesign(self):
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
        self.sb.Hide()
        self.grb.Add(self.sb, pos=(0, 0), span=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        m_comboBox2Choices = ["Задать как F(x) и найти f(x)", "Задать как f(x) и найти F(x)"]
        self.m_comboBox2 = wx.ComboBox(self.panel, wx.ID_ANY, "Combo!", wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox2Choices, 0)
        self.grb.Add(self.m_comboBox2, pos=(2, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.addbutton.Bind(wx.EVT_BUTTON, self.onAddWidget)
        self.deletebutton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
        # self.button.Bind(wx.EVT_BUTTON, self.onEditFormul)
        self.Bind(wx.EVT_COMBOBOX, self.onEditFormul, self.m_comboBox2)
        self.boxS.Add(self.grb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        # self.boxS.Add(self.m_comboBox2, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.boxS.Layout()
        self.panel.Layout()

    def onGrid(self, event):
        print("!")

    def build_plot(self, arr_p, x, y):
        axes1 = np.linspace(-100, 100)
        axes2 = [0] * len(axes1)

        fig = plt.figure(figsize=(15, 6))
        ax = fig.add_subplot()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        ax1 = plt.subplot(1, 2, 1)
        plt.plot(axes1, axes2, color='k')
        plt.plot(axes2, axes1, color='k')
        x_ = x.copy()
        y_ = y.copy()
        x_ = self.pos_arr(x_, min(x) - 100, max(x) + 100)
        y_ = self.pos_arr(y_, min(y), max(y))
        ax1.step(x_, y_, 'r--o', linewidth=3, label='F(x)')
        ax1.legend()
        ax1.grid()
        ax1.set_ylim(-0.1, 1.2)
        ax1.set_xlim(min(x) - 5, max(x) + 5)

        ax2 = plt.subplot(1, 2, 2)
        plt.plot(axes1, axes2, color='k')
        plt.plot(axes2, axes1, color='k')
        ax2.plot(self.arr_x, arr_p, 'b--o', linewidth=3, label='f(x)')
        ax2.legend()
        ax2.grid()
        ax2.set_ylim(-0.1, 1.2)
        ax2.set_xlim(min(self.arr_x) - 5, max(self.arr_x) + 5)

        plt.show()

    def onParam(self, event):
        num = int(event.GetString())
        print(len(self.gr.GetChildren()))
        while len(self.gr.GetChildren()) != 3:
            self.gr.Hide(len(self.gr.GetChildren()) - 1)
            self.gr.Remove(len(self.gr.GetChildren()) - 1)

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

        # self.boxS.Add(self.gr)
        # self.panel.SetSizer(self.boxS)
        self.boxS.Layout()
        # self.panel.Layout()
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
        # if len(self.gr.GetChildren()) == 9:
        #     self.gr.Hide(8)
        #     self.gr.Remove(8)
        # if len(self.gr.GetChildren()) == 8:
        #     self.gr.Hide(7)
        #     self.gr.Remove(7)
        #     self.gr.Hide(6)
        #     self.gr.Remove(6)
        #     self.Layout()
        s=len(self.gr.GetChildren())
        while len(self.gr.GetChildren())>6:
            self.gr.Hide(len(self.gr.GetChildren()) - 1)
            self.gr.Remove(len(self.gr.GetChildren()) - 1)
        print(len(self.gr.GetChildren()))
        arr_p = list()
        self.arr_x = list()
        stattxt = wx.StaticText(self.panel)
        stattxt.SetForegroundColour((255, 0, 0))
        try:
            for i in range(self.grid.GetNumberCols()):
                self.arr_x.append(float(self.grid.GetCellValue(0, i)))
            for i in range(self.grid.GetNumberCols()):
                arr_p.append(float(self.grid.GetCellValue(1, i)))
        except:
            stattxt.LabelText="Ошибочка"
            self.gr.Add(stattxt, pos=(5, 0), flag=wx.LEFT | wx.BOTTOM, border=5)
            self.gr.Layout()
            return

        arr_p = np.array(arr_p)
        self.arr_p = arr_p
        if int(arr_p.sum()) != 1.0:
            stattxt.LabelText = "Сумма вероятностей должна быть равна единице"
            self.gr.Add(stattxt, pos=(5, 0), flag=wx.LEFT | wx.BOTTOM, border=5)
            self.gr.Layout()
            return
        for el in arr_p:
            if el<=0:
                stattxt.LabelText = "Одна из вероятностей отрицательная"
                self.gr.Add(stattxt, pos=(5, 0), flag=wx.LEFT | wx.BOTTOM, border=5)
                self.gr.Layout()
                return
            if el>=1:
                stattxt.LabelText = "Одна из вероятностей больше единицы"
                self.gr.Add(stattxt, pos=(5, 0), flag=wx.LEFT | wx.BOTTOM, border=5)
                self.gr.Layout()
                return


        x, p = self.arr_x.copy(), arr_p.copy()

        self.build_solve_DSV(p, x)

    def build_solve_DSV(self, p, x):

        M_X = dsv.M_X(x, p)[1]
        D_X = dsv.D_X(x, p)[1]
        Std = dsv.S_X(x, p)[1]
        stattxt = wx.StaticText(self.panel)
        stattxt.LabelText = f"{M_X}-мат.ожидание\n{D_X}-дисперсия\n{Std}-стандартное отклонение"
        bmp = wx.Bitmap("why.jpg")
        bmp = self.scale_bitmap(bmp, 40, 40)
        stb = wx.Button(self.panel, size=(50, 50), name="button")
        stb.SetBitmap(bmp)
        arr_F = list()
        arr_F.append(0)
        for el in range(len(p)):
            sum = 0
            if el == 0:
                continue
            for i in range(el):
                sum += p[i]
            arr_F.append(sum)
        arr_F.append(1)
        x = self.arr_x.copy()
        y = arr_F.copy()
        x.append(x[-1] + 5)
        f_x = dsv.F_X(x, p)[0]
        # self._drawGraph(self.arr_x, arr_p)
        # self._drawGraph1(f_x, x)
        self.build_canvas1(p, x, y)
        self.build_canvas2(p, x, y)
        img = wx.Image("output1.png", type=wx.BITMAP_TYPE_ANY, index=-1)
        sb = wx.StaticBitmap(self.panel, -1, wx.Bitmap(img))
        self.gr.Add(stattxt, pos=(5, 0), flag=wx.LEFT | wx.BOTTOM, border=5)
        self.gr.Add(stb, pos=(5, 1), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.gr.Add(sb, pos=(6, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        self.gr.Layout()
        self.Bind(wx.EVT_BUTTON, self.onWhyButt, stb)
        self.build_plot(p, x, y)

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


app = wx.App()
wnd = MyFrame(None)
wnd.Show()
app.MainLoop()
