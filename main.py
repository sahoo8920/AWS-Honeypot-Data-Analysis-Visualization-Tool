import wx
from wx import adv
import wx.grid
import pandas as pd
import filters
import visdialog


def read_dataset():
    columnList = ['datetime', 'host', 'proto', 'spt', 'dpt', 'srcstr',
                  'cc', 'country', 'locale', 'latitude',
                  'longitude']  # columns to load from dataset
    dataframe = pd.read_csv("AWS_Honeypot_marx-geo.csv", usecols=columnList)
    dataframe["datetime"] = dataframe["datetime"].str.split(" ", expand=True)  # extract date from timestamps
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"], dayfirst=True)  # convert to datetime type
    dataframe["dpt"] = dataframe["dpt"].fillna(0).astype(int).astype(str)  # convert to str type
    dataframe["spt"] = dataframe["spt"].fillna(0).astype(int).astype(str)  # # convert to str type
    return dataframe


class AppFrame(wx.Frame):

    def __init__(self, parent, title, size):
        super().__init__(parent=parent, title=title, size=size)

        # create menubar
        appMenuBar = wx.MenuBar()

        # create file menu
        fileMenu = wx.Menu()

        # create file menu items
        fileMenuItemSave = fileMenu.Append(wx.ID_SAVE, 'Save as CSV', 'Save results as CSV')
        fileMenuItemQuit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        appMenuBar.Append(fileMenu, "&File")

        fileMenu.Bind(wx.EVT_MENU, self.on_save_as_csv, fileMenuItemSave)
        fileMenu.Bind(wx.EVT_MENU, self.on_quit, fileMenuItemQuit)

        # create help menu
        helpMenu = wx.Menu()

        # create help menu items
        helpMenuItemHelp = helpMenu.Append(wx.ID_ABOUT, 'About', 'About')
        helpMenuItemAbout = helpMenu.Append(wx.ID_HELP, 'Help', 'Help')
        appMenuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(appMenuBar)
        self.my_panel = AppPanel(self)

    def on_save_as_csv(self, event):
        """call the save_dataframe mwthod from AppPanel"""
        self.my_panel.save_dataframe()

    def on_quit(self, event):
        exit()


class AppPanel(wx.Panel):
    # set globals for grid pagination
    pageLength = 100
    currentPage = 0

    # read the dataset and create second copy for manipulation
    df = read_dataset()
    temp_df = df.copy()

    def __init__(self, parent):
        super().__init__(parent=parent)

        # input control widgets
        self.queryInput = wx.SearchCtrl(self, size=(223, 25))
        self.startDatePicker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)
        self.endDatePicker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)

        self.defaultStartDate = wx.DateTime(day=1, month=0, year=2013, hour=0, minute=0, second=0, millisec=0)
        self.defaultEndDate = wx.DateTime(day=31, month=11, year=2013, hour=0, minute=0, second=0, millisec=0)

        self.startDatePicker.SetValue(self.defaultStartDate)
        self.endDatePicker.SetValue(self.defaultEndDate)

        # button widgets
        self.visualizeButton = wx.Button(self, label="Visualize")
        self.searchButton = wx.Button(self, label="Search")
        self.clearButton = wx.Button(self, label="Clear")
        self.nextButton = wx.Button(self, label="Next")
        self.previousButton = wx.Button(self, label="Previous")

        # create button handlers
        self.visualizeButton.Bind(wx.EVT_BUTTON, self.onVisualizeButton)
        self.searchButton.Bind(wx.EVT_BUTTON, self.onSearchButton)
        self.clearButton.Bind(wx.EVT_BUTTON, self.onClear)
        self.nextButton.Bind(wx.EVT_BUTTON, self.nextPage)
        self.previousButton.Bind(wx.EVT_BUTTON, self.prevPage)

        # create the label widgets
        searchButtonLabel = wx.StaticText(self, label="Enter Query")
        startDatePickerLabel = wx.StaticText(self, label="From Date")
        endDatePickerLabel = wx.StaticText(self, label="To Date")
        self.rowsRetrieved = wx.StaticText(self, label=f"Rows retrieved: {len(self.temp_df)}")

        page_str = "Page " + str(self.currentPage + 1) + " of " + str(len(self.temp_df) // self.pageLength + 1)
        self.page_number_text = wx.StaticText(self, label=page_str)

        # create grid
        self.appGrid = wx.grid.Grid(parent=self, size=(100, 100))
        self.appGrid.CreateGrid(0, len(self.df.columns) - 2)
        for i in range(len(self.df.columns) - 2):  # exclude longitude and lattiude column
            self.appGrid.SetColLabelValue(col=i, value=self.df.columns[i])
        self.appGrid.SetDefaultColSize(width=131)  # default column width
        self.populate_grid()

        # sizers
        vSizer = wx.BoxSizer(wx.VERTICAL)  # for main panel
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)  # for input widgets
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)  # for search, visualize and clear buttons
        hSizer3 = wx.BoxSizer(wx.HORIZONTAL)  # for grid

        # add widgets to sizers
        hSizer1.Add(searchButtonLabel, proportion=0, flag=wx.LEFT, border=60)
        hSizer1.Add(self.queryInput, proportion=0, flag=wx.LEFT, border=10)
        hSizer1.Add(startDatePickerLabel, proportion=0, flag=wx.LEFT, border=60)
        hSizer1.Add(self.startDatePicker, proportion=0, flag=wx.LEFT, border=10)
        hSizer1.Add(endDatePickerLabel, proportion=0, flag=wx.LEFT, border=60)
        hSizer1.Add(self.endDatePicker, proportion=0, flag=wx.LEFT, border=10)

        hSizer2.Add(self.previousButton, proportion=0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        hSizer2.Add(self.nextButton, proportion=0, flag=wx.LEFT | wx.ALIGN_LEFT, border=10)
        hSizer2.Add(self.page_number_text, proportion=0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        hSizer2.Add(self.rowsRetrieved, proportion=0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        hSizer2.Add(600, 0, 1)
        hSizer2.Add(self.visualizeButton, proportion=0, flag=wx.RIGHT, border=20)
        hSizer2.Add(self.searchButton, proportion=0, flag=wx.RIGHT, border=20)
        hSizer2.Add(self.clearButton, proportion=0, flag=wx.RIGHT, border=20)

        vSizer.Add(hSizer1, 0, wx.ALL, border=20)
        vSizer.Add(hSizer2, 0, wx.ALL | wx.ALIGN_RIGHT, border=20)
        vSizer.Add(hSizer3, 0, wx.ALL | wx.ALIGN_CENTER, border=20)
        vSizer.Add(self.appGrid, proportion=1, flag=wx.EXPAND)

        # set sizer
        self.SetSizer(vSizer)

    def populate_grid(self):
        # for pagination, set the correct start and end index
        startIndex = self.currentPage * self.pageLength
        endIndex = startIndex + self.pageLength

        # read results from dataframe based on start and end index
        dfDisplay = self.temp_df.iloc[startIndex: endIndex]

        # convert the retreived data to list
        data = dfDisplay.values.tolist()

        # clear the pervious page before populating new page
        if self.appGrid.GetNumberRows() > 0:
            self.appGrid.DeleteRows(numRows=self.appGrid.GetNumberRows())

        # populate the new page
        for row in range(len(dfDisplay)):
            self.appGrid.AppendRows(numRows=1, updateLabels=True)
            for col in range(len(dfDisplay.columns) - 2):
                self.appGrid.SetCellValue(row, col, str(data[row][col]))

    def nextPage(self, event):
        # update self.page and re populate grid
        if self.currentPage >= len(self.temp_df) // self.pageLength:
            pass
        else:
            self.currentPage += 1
            self.populate_grid()
            self.updatePageNum()

    def prevPage(self, event):
        # update self.page and re populate grid
        if self.currentPage <= 0:
            pass
        else:
            self.currentPage -= 1
            self.populate_grid()
            self.updatePageNum()

    def updatePageNum(self):
        page_str = "Page " + str(self.currentPage + 1) + " of " + str(len(self.temp_df) // self.pageLength + 1)
        self.page_number_text.SetLabel(page_str)

    def onSearchButton(self, event):
        # get the query from the input
        query = self.queryInput.GetValue()

        # format the dates
        start_date = self.startDatePicker.GetValue().FormatISODate()
        end_date = self.endDatePicker.GetValue().FormatISODate()

        self.temp_df = filters.search_period(self.temp_df, start_date, end_date)
        self.populate_grid()
        self.updatePageNum()

        if query != "":  # check if not blank
            # validate input query
            if self.query_input_validation(query) != -1:
                self.temp_df = self.df.copy()
                self.temp_df = filters.search_query(self.temp_df, query)
                self.populate_grid()
                self.updatePageNum()
            else:
                self.display_invalid_query_dialog()
        else:  # if blank
            self.populate_grid()
            self.updatePageNum()

        self.rowsRetrieved.SetLabel(f"Rows retrieved: {len(self.temp_df)}")
        self.temp_df = self.df.copy()  # reset temp dataframe from original dataframe

    def onVisualizeButton(self, event):
        # get the query from the input
        query = self.queryInput.GetValue()

        # format the dates
        start_date = self.startDatePicker.GetValue().FormatISODate()
        end_date = self.endDatePicker.GetValue().FormatISODate()

        self.temp_df = filters.search_period(self.temp_df, start_date, end_date)
        self.populate_grid()
        self.updatePageNum()

        valid = True
        if query != "":  # check if not blank
            # validate input query
            if self.query_input_validation(query) != -1:
                self.temp_df = self.df.copy()
                self.temp_df = filters.search_query(self.temp_df, query)
                self.populate_grid()
                self.updatePageNum()
            else:
                self.display_invalid_query_dialog()
                valid = False  # set the valid variable to false
        else:  # if blank
            self.populate_grid()
            self.updatePageNum()

        if valid:  # show visualisation prompt only if valid variable is true
            visdialog.select_visualization(self.temp_df)

        self.temp_df = self.df.copy()  # reset temp dataframe from original dataframe

    def onClear(self, event):
        self.queryInput.SetValue("")
        self.startDatePicker.SetValue(self.defaultStartDate)
        self.endDatePicker.SetValue(self.defaultEndDate)

    def query_input_validation(self, query):
        key_value_list = query.split(",")
        for key_value in key_value_list:
            if key_value.split(":")[0] not in ["host", "proto", "spt", "dpt", "srcstr", "country"]:
                return -1

    def display_invalid_query_dialog(self):
        error_msg = wx.Dialog(None, title="Invalid syntax", size=(500, 160), pos=(400, 250))
        instructions = "Use key:value pairs\nAllowed keys: host, proto, spt, dpt, srcstr, country.\neg: host:groucho-oregon,dpt:1433|80"
        help_text = wx.StaticText(error_msg, label=instructions)
        font = wx.Font(11, family=wx.FONTFAMILY_MODERN, style=0, weight=90,
                       underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        help_text.SetFont(font)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(help_text, 1, wx.ALL | wx.ALIGN_CENTER, border=10)
        error_msg.SetSizer(sizer)
        error_msg.Show()
        return False

    def save_dataframe(self):
        """file save dialog"""
        with wx.FileDialog(self, "Save results", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                print(pathname)
                self.temp_df.to_csv(pathname)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)


def main():
    mainApp = wx.App()
    mainAppFrame = AppFrame(None, title="AWS Honeypot Data Analysis Tool", size=(1000, 600))
    mainAppFrame.Show()
    mainAppFrame.Maximize()
    mainApp.MainLoop()


if __name__ == "__main__":
    main()