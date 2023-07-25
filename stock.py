from matplotlib.figure import Figure 
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  

def plot(ticker, rownumgraph, stockdownloadlist, flagdaynight, fgcol,bgcol,framestock): 
    
    #The figure that will contain the plot 
    fig = Figure(figsize = (3, 1), dpi = 87) 
        
    #Download data points for each stock from API
    data = stockdownloadlist[ticker]
    changepercent = round(((list(dict(data["Close"]).items())[-1][1]-list(dict(data["Close"]).items())[0][1])/list(dict(data["Close"]).items())[0][1])*100,2)
    if changepercent>0: #sets graph color based on the percentage change
        graphcol = "green"
    else:
        graphcol = "red"
    plotgr = fig.add_subplot(111)
    plotgr.plot(data.Close, color=graphcol)  #function to plot graph based on data within matplotlb.figure module
    if flagdaynight==False: #sets colors within the labels according to color mode
        for spine in plotgr.spines:
            plotgr.spines[spine].set_color(fgcol)
        for axis in ('x', 'y'):
            plotgr.tick_params(axis=axis, color=fgcol)
        for tl in plotgr.get_yticklabels():
            tl.set_color(fgcol)
        for tl in plotgr.get_xticklabels():
            tl.set_color(fgcol)
    #creating the Tkinter canvas with matplotlib graph
    canvas = FigureCanvasTkAgg(fig, master = framestock)
    fig.patch.set_facecolor(bgcol) 
    plotgr.patch.set_facecolor(bgcol) 
    canvas.draw() 

    canvas.get_tk_widget().grid(row = rownumgraph, column=1, rowspan=3, pady=(10,0), padx = (10,0), sticky="n")

def stock(tickerlist,framestock,bgcol,fgcol,yf,stockdownloadlist,flagdaynight,rownumgraph): #iterates through stock tickers to get required information
    for tickername in tickerlist:
        try:
            tickerinfo = yf.Ticker(tickername)
        except:
            # print (f"Sorry, the ticker name ({tickername}) is invalid or data is unavailable.")
            # quit()
            ...
        print(tickerinfo)
        longname,symbol =tickername,tickername #tickerinfo.info["longName"],tickerinfo.info["symbol"]
        tickernameLabel = Label(framestock,text=longname, bg=bgcol, fg=fgcol)
        tickersymLabel = Label(framestock, text = "("+symbol+")", bg=bgcol, fg=fgcol)
        data = yf.download(tickers =symbol, period = "1mo") 
        stockdownloadlist[symbol] = data
        changepercent = round(((list(dict(data["Close"]).items())[-1][1]-list(dict(data["Close"]).items())[0][1])/list(dict(data["Close"]).items())[0][1])*100,2)
        if changepercent>0:
            changepercentLabel = Label(framestock,text="+"+str(changepercent), font=("bahnschrift bold",12),fg = "green", bg=bgcol)
        else:
            changepercentLabel = Label(framestock,text=changepercent, font=("bahnschrift bold",12), fg = "red", bg=bgcol)
        
        tickernameLabel.grid(pady=(20,0),padx=(10,0))
        tickersymLabel.grid()
        changepercentLabel.grid()

    for tickername in tickerlist: #iterates through tickers to plot the graph using the plot function 
        plot(tickername, rownumgraph,stockdownloadlist,flagdaynight,fgcol,bgcol,framestock)
        rownumgraph+=3
    return rownumgraph