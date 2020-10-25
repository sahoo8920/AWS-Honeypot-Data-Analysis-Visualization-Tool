# displays a diaglog containing lists of available plot types
# call the plotting functions from plot.py module based on user selection

import wx
import plots


class VPanel(wx.Panel):
    """Visulization prompt window on 'Visualize' button click"""

    def __init__(self, parent, dataframe):
        super().__init__(parent=parent)
        self.dataframe = dataframe
        # radio buttons
        self.rb1 = wx.RadioButton(self, wx.ID_ANY, label='Connections over time - Line Plot')
        self.rb2 = wx.RadioButton(self, wx.ID_ANY, label='Connection count by AWS Hosts - Bar Plot')
        self.rb3 = wx.RadioButton(self, wx.ID_ANY, label='Heatmap Plot')
        self.rb4 = wx.RadioButton(self, wx.ID_ANY, label='Top 15 Destination Ports - Pie Plot')
        self.rb5 = wx.RadioButton(self, wx.ID_ANY, label='Top 15 Source IP for current search - H.Bar Plot')

        self.okay_button = wx.Button(self, label="Plot")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(30)
        sizer.Add(self.rb1, 0, wx.LEFT | wx.TOP | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.rb2, 0, wx.LEFT | wx.TOP | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.rb3, 0, wx.LEFT | wx.TOP | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.rb4, 0, wx.LEFT | wx.TOP | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.rb5, 0, wx.LEFT | wx.TOP | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.okay_button, 0, wx.TOP | wx.ALIGN_CENTRE, border=30)
        self.SetSizer(sizer)

        self.okay_button.Bind(wx.EVT_BUTTON, self.on_okay)

    def on_okay(self, event):
        if self.rb1.GetValue():  # check count over time - heatmap
            plots.time_count_plot(self.dataframe)
        if self.rb2.GetValue():  # check count over time - lineplot
            plots.host_count_plot(self.dataframe)
        if self.rb3.GetValue():
            plots.heatmap_plot(self.dataframe)
        if self.rb4.GetValue():  # check count by suburb - barplot
            plots.top_15_dpt(self.dataframe)
        if self.rb5.GetValue():  # check geographical scatter map
            plots.top_15_ip(self.dataframe)


def select_visualization(dataframe):  # pass the dataframe
    app = wx.App()
    dialog = wx.Dialog(None, title="Select Plot Type for current search", size=(330, 330), pos=(480, 150))
    panel = VPanel(parent=dialog, dataframe=dataframe)
    dialog.Center()
    dialog.Show()
    app.MainLoop()

