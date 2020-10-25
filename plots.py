# contains plotting functions at the end which are called by visprompt
# plotting functions instantiate plot classes which display plot

import wx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class TimePlotPanel(wx.Panel):

    def __init__(self, parent, df):
        wx.Panel.__init__(self, parent=parent)

        self.temp_df = df.copy()
        self.temp_df = pd.DataFrame(data=self.temp_df["datetime"].value_counts().reset_index())
        self.temp_df = self.temp_df.rename(columns={"index": "date", "datetime": "count"})

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.ax = self.figure.add_subplot(111)

        sns.lineplot(data=self.temp_df, x="date", y="count", ax=self.ax, palette="coolwarm", lw=1, color="Purple")

        self.ax.set_xlabel("Date", fontsize=10)
        self.ax.set_ylabel("Number of connections", fontsize=10)
        self.ax.set_title("Connection count by date", fontsize=10)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.BOTTOM | wx.GROW, border=4)
        self.SetSizer(self.sizer)
        sns.despine(left=True)
        self.Fit()


class HostPlotPanel(wx.Panel):

    def __init__(self, parent, df):
        wx.Panel.__init__(self, parent=parent)

        self.temp_df = df.copy()

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.ax = self.figure.add_subplot(111)

        plot = sns.countplot(x=self.temp_df["host"], data=self.temp_df, ax=self.ax, palette="coolwarm", lw=1,
                             color="Purple")
        plot.set_xticklabels(plot.get_xticklabels(), rotation=45)

        self.ax.set_xlabel("Host", fontsize=14)
        self.ax.set_ylabel("Number of connections", fontsize=14)
        self.ax.set_title("Connection count by host", fontsize=14)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.BOTTOM | wx.GROW, border=4)
        self.SetSizer(self.sizer)
        sns.despine(left=True)
        self.Fit()


class HeatMap(wx.Panel):

    def __init__(self, parent, df):
        wx.Panel.__init__(self, parent=parent)

        self.temp_df = df.copy()

        # extract the month and day from the datetime column
        self.temp_df["Day"] = self.temp_df["datetime"].dt.day
        self.temp_df["Month"] = self.temp_df["datetime"].dt.month

        # create figure object, canvas and axes
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.ax = self.figure.add_subplot(111)

        data_pivot = self.temp_df.pivot_table(values='host', index='Month', columns='Day', aggfunc='count')
        sns.heatmap(data_pivot, cmap="BuGn", ax=self.ax)

        # self.ax.set_xlabel("Date", fontsize=10)
        # self.ax.set_ylabel("Number of connections", fontsize=10)
        self.ax.set_title("Heatmap Plot", fontsize=15)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.BOTTOM | wx.GROW, border=4)
        self.SetSizer(self.sizer)
        sns.despine(left=True)
        self.Fit()


class TopDPort(wx.Panel):

    def __init__(self, parent, df):
        wx.Panel.__init__(self, parent=parent)

        self.temp_df = df.copy()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.temp_df = df.copy()
        self.temp_df = pd.DataFrame(data=self.temp_df["dpt"].value_counts().reset_index())
        self.temp_df = self.temp_df.rename(columns={"index": "dpt", "dpt": "count"})
        self.temp_df = self.temp_df.sort_values(by="count", ascending=False)
        self.temp_df = self.temp_df.head(15)

        dpt_list = self.temp_df["dpt"].to_list()
        count_list = self.temp_df["count"].to_list()

        self.ax.pie(x=count_list, labels=dpt_list, autopct='%1.1f%%')

        self.ax.set_title("Top 15 Destination Ports in current search")
        self.ax.legend(bbox_to_anchor=(1.4, 1))

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.BOTTOM | wx.GROW, border=4)
        self.SetSizer(self.sizer)
        sns.despine(left=True)
        self.Fit()


class TopIP(wx.Panel):

    def __init__(self, parent, df):
        wx.Panel.__init__(self, parent=parent)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.temp_df = df.copy()
        self.temp_df = pd.DataFrame(data=self.temp_df["srcstr"].value_counts().reset_index())
        self.temp_df = self.temp_df.rename(columns={"index": "srcstr", "srcstr": "count"})
        self.temp_df = self.temp_df.sort_values(by="count", ascending=False)
        self.temp_df = self.temp_df.head(15)
        ip_list = self.temp_df["srcstr"].to_list()
        count_list = self.temp_df["count"].to_list()

        self.ax.barh(ip_list, count_list, align='center')

        self.ax.set_title("Top 15 IP addresses")
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        self.ax.tick_params(axis='both', which='minor', labelsize=12)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.BOTTOM | wx.GROW, border=4)
        self.SetSizer(self.sizer)
        sns.despine(left=True)
        self.Fit()


def time_count_plot(df):
    myApp = wx.App()
    myFrame = wx.Frame(parent=None, title="Plot", size=(800, 600))
    panel = TimePlotPanel(myFrame, df)
    myFrame.Maximize()
    myFrame.Show()
    myApp.MainLoop()


def host_count_plot(df):
    myApp = wx.App()
    myFrame = wx.Frame(parent=None, title="Plot", size=(800,600))
    panel = HostPlotPanel(myFrame, df)
    myFrame.Maximize()
    myFrame.Show()
    myApp.MainLoop()


def heatmap_plot(df):
    myApp = wx.App()
    myFrame = wx.Frame(parent=None, title="Plot", size=(800, 600))
    panel = HeatMap(myFrame, df)
    myFrame.Maximize()
    myFrame.Show()
    myApp.MainLoop()


def top_15_dpt(df):
    myApp = wx.App()
    myFrame = wx.Frame(parent=None, title="Plot", size=(800,600))
    panel = TopDPort(myFrame, df)
    myFrame.Maximize()
    myFrame.Show()
    myApp.MainLoop()


def top_15_ip(df):
    myApp = wx.App()
    myFrame = wx.Frame(parent=None, title="Plot", size=(800,600))
    panel = TopIP(myFrame, df)
    myFrame.Maximize()
    myFrame.Show()
    myApp.MainLoop()

