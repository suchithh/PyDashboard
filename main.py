

'''
News GUI
News GUI is a clean, intuitive and functional GUI written in python. 
The module Tkinter is used to create a native GUI and several APIs are used to collect various data like the latest news, financial information, weather data and covid-19 statistics. 
The data is collected from the APIs using the python requests library in the json format and is then parsed by the json module. 
The parsed data is then organized in the GUI using the Tkinter widgets. The Tkinter widgets - buttons, labels, canvas and frame - are gridded into the GUI and the final layout is presented to the user.
Salient features include:
    Intuitive layout
    Automatic detection of the user's country and location using the network IP address
    Current weather information for the user's city
    Latest information about the value of user inputted stocks, neatly organized in a graph
    Top news in the user's country with related pictures and a short snippet of the article. When button or text is clicked, user is taken to the article in the default web browser
    Currency converter and Exachange rates 
    Calandar Manager with dynamic listing on the preference of the user.
    Automatic dark theme based on the time of the day to reduce strain on the eyes
'''
from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from time import strftime
import os
import sys
import json
import yfinance as yf
import Currency_Wigide_manager
import errno
import stock
import weather
import news
import location
from threading import Timer
# Create Nominatim object for geolocation


# Default stock ticker list
# tickerlist = ["MSFT", "AAPL", "TSLA", "GOOGL"]
def time():
    currenttime = strftime('%I:%M:%S %p')
    timeLabel.configure(text=currenttime)
    timeLabel.after(1000, time)


def greeting():
    currenthour = int(strftime('%H'))
    # Greeting based on the time of the day
    if 5 <= currenthour < 12:
        greetLabel.configure(text="Good morning")
    elif 12 <= currenthour < 17:
        greetLabel.configure(text="Good afternoon")
    elif 17 <= currenthour <= 23 or 0 <= currenthour < 5:
        greetLabel.configure(text="Good evening")


def date():
    # sets date
    currentdate = strftime('%A, %d %B %Y')
    dateLabel.configure(text=currentdate)


def mkdir_p(path):
    # creates path for assets and other important stuff
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def setstuff():
    ct_root = Toplevel()
    # ct_root.geometry('300x200')
    with open("user_custom.json", 'r') as setting:
        current_default = json.load(setting)

    ct_root.title("Settings")
    Label(ct_root, text='Settings', font="Algerian 20").grid(
        row=0, column=0, columnspan=2, pady=(12, 25), padx=20)

    Label(ct_root, text='Stocks  ').grid(row=1, column=0, sticky=W)
    stock_entry = Entry(ct_root, width=30)
    stock_entry.insert(END, current_default["tickerlist"])
    stock_entry.grid(row=1, column=1)

    Label(ct_root, text='Theme  ').grid(row=2, column=0, sticky=W)
    th_val = StringVar()

    th_val.set(str(current_default["colormode"]))

    print(th_val.get())
    th_menu = OptionMenu(ct_root, th_val, "Light", "Dark", "Auto")
    th_menu.grid(row=2, column=1)

    def save_changes():
        ans = messagebox.askokcancel("Confirmaton", "Confirm changes ?")
        if ans:

            print(current_default)
            current_default["tickerlist"] = stock_entry.get().split(" ")
            current_default["colormode"] = str(th_val.get())

            a = current_default['tickerlist']
            if len(a) > 5:
                s = messagebox.askokcancel(
                    "Interruption ", 'Accept only the first 5 stocks? ')
                if not (s):
                    return

                else:
                    b = a[0:5]

                    print(b)

                    current_default["tickerlist"] = b

            with open("user_custom.json", 'w') as setting:
                json.dump(current_default, setting, indent=4)
            print(current_default)
            ct_root.destroy()
            root.destroy()
            os.execl(sys.executable, 'python', __file__)

        else:
            return

    cb = Button(ct_root, text="Cancel", command=ct_root.destroy)
    cb.grid(row=4, column=0)
    sb = Button(ct_root, text="Save", command=save_changes)
    sb.grid(row=4, column=1)

    ct_root.mainloop()


stockdownloadlist = {}
flagdaynight = True
colormode = 1


if __name__ == '__main__':  # this is the main function of the program
    with open("user_custom.json", 'r') as setting:
        current_default = json.load(setting)
        tickerlist = current_default["tickerlist"]
        color = current_default["colormode"]
        if color.lower() == 'dark':
            colormode = 1
        elif color.lower() == 'light':
            colormode = -1
        else:
            colormode = 0

    print("Collecting data from the internet. Please Wait...")
    mkdir_p("assets")
    # gets information from the location file
    city_name, country_name, country_code = location.location()
    hour = int(strftime('%H'))

    # function to change between lightmode and dark mode depending upon user preferences and time
    if ((0 <= hour < 6 or 18 < hour <= 23) and colormode == 0) or colormode == 1:
        bgcol = "#303032"
        fgcol = "white"
        flagdaynight = False
    else:
        bgcol = "white"
        fgcol = "black"

    # Tkinter boilerplate shit
    root = Tk()
    # root.geometry("1700x870")
    root.title("Widget Panel")
    root.configure(bg=bgcol)
    #bgp = PhotoImage(file = "/Users/uchitnm/Workspace/GROUP_WORK/newspy/bgp.png")
    # Label(root,image=bgp).place(x=0,y=0)
    # Frames

    # frame for daytime
    framedaytime = Frame(root)
    framedaytime.grid(row=0, column=1, columnspan=2, padx=(5, 0), sticky="n")
    framedaytime.configure(bg=bgcol)

    # frame for weather
    frameweather = Frame(root)
    frameweather.grid(row=0, column=0, padx=(30, 0), sticky="n")
    frameweather.configure(bg=bgcol)

    # frame for calander
    framecal = Frame(master=root)
    framecal.grid(row=0, column=3, rowspan=9, pady=(0, 0), sticky='n')
    framecal.config(bg=bgcol)

    # frame for stocks
    framestock = Frame(root)
    framestock.grid(row=1, column=0, columnspan=1, sticky="n")
    framestock.configure(bg=bgcol)

    framenews = Frame(root)
    framenews.grid(row=1, column=1, padx=(30, 0), columnspan=2, sticky="n")
    framenews.configure(bg=bgcol)

    # Widgets

    # Greetings and date time
    greetLabel = Label(framedaytime, font=(
        "bahnschrift", 20), bg=bgcol, fg=fgcol)
    greeting()

    timeLabel = Label(framedaytime, font=(
        "century gothic", 40), bg=bgcol, fg=fgcol)
    time()

    dateLabel = Label(framedaytime, font=(
        "bahnscrift", 15), bg=bgcol, fg=fgcol)
    date()

    greetLabel.grid(row=0, column=4, padx=(0, 0), sticky='n')
    timeLabel.grid(row=1, column=4, padx=(0, 0), sticky='n')
    dateLabel.grid(row=2, column=4, padx=(0, 0), sticky='n')

    # Weather information is set in the next few lines of code using information from the weather file

    weathertextLabel = Label(frameweather, text="Weather", font=(
        "century gothic bold", 25), bg=bgcol, fg=fgcol)
    weatherLabel = Label(frameweather, font=(
        "century gothic", 20), bg=bgcol, fg=fgcol)
    weatherLabel.configure(text=weather.weather(city_name), compound="right")

    locLabel = Label(frameweather, text="%s, %s" % (
        city_name, country_name), font=("century gothic", 20), bg=bgcol, fg=fgcol)

    # loads the weather asset png
    weatherim = PhotoImage(file="assets/weather.png")
    weatherLabel.configure(image=weatherim)

    weathertextLabel.grid(row=1, column=1, sticky="n")
    weatherLabel.grid(row=2, column=1, sticky="nw")

    locLabel.grid(row=0, column=1, sticky="n", padx=(0, 0))

    # Stock information
    stockLabel = Label(framestock, text="Live Stock Info", font=(
        "century gothic bold", 20), bg=bgcol, fg=fgcol)
    stockLabel.grid(row=0, column=0, columnspan=2, sticky="n", pady=(30, 0))

    rownumgraph = 1
    print(f"Collecting data for {len(tickerlist)} stock ticker(s)...")

    # calls stock function within stock file to load stock data into the stock labels
    rownum = stock.stock(tickerlist, framestock, bgcol, fgcol, yf,
                         stockdownloadlist, flagdaynight, rownumgraph)+1

    # News data
    news.newsparse(framenews, bgcol, fgcol, country_code)

    # currency converter and exchange rates
    framecc = Frame(framestock, highlightbackground=fgcol,
                    highlightthickness=2, width=350)
    framecc.grid(row=rownum, column=0, columnspan=3, pady=(25, 0))
    framecc.configure(bg=bgcol, width=350)

    # Menu bar for options and help
    menuBar = Menu(root)
    MENU1 = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label='Settings & Help', menu=MENU1)
    MENU1.add_command(label='Settings',
                      command=setstuff)
    MENU1.add_command(label='Detailed Information (Exachange rates)',
                      command=Currency_Wigide_manager.DETAILS)
    MENU1.add_separator()
    MENU1.add_command(label="Exit", command=exit)
    MENU1.add_separator()
    MENU1.add_command(label="About", command=lambda: messagebox.showinfo(
        "About", "Project by :\n Suyog \n Uchit \n Varun"))
    root.config(menu=menuBar)
    root.config(menu=menuBar)

    # variable to hold input amount
    amount = StringVar()

    # variable to hold from country
    choice_from = StringVar()
    choice_from.set("INR")

    # variable to hold tp country
    choice_to = StringVar()
    choice_to.set("USD")

    # variable to hold converted amt

    final_amt = StringVar()
    final_amt.set("0")

    # opening the datafiles
    with open('data.json', 'r', encoding="utf8") as fileObj:
        choices = json.load(fileObj)

    # From country name label and dropdown
    Label(framecc, text="From: ", bg=bgcol, font='Banschrift 13',
          fg=fgcol).grid(row=rownum-1, column=0, padx=55, pady=(0, 0))
    MenuFrom = OptionMenu(framecc, choice_from, *choices)
    MenuFrom.grid(row=rownum, column=0, padx=(0, 35))

    # To country name label and dropdown
    Label(framecc, text="To: ", bg=bgcol, font='Banschrift 13', fg=fgcol).grid(
        row=rownum-1, column=1, pady=(0, 0), padx=55)
    MenuTo = OptionMenu(framecc, choice_to, *choices)
    MenuTo.grid(row=rownum, column=1, padx=(0, 0))

    # Input amount label and dropdown
    Label(framecc, text="Amount: ", bg=bgcol, fg=fgcol).grid(
        row=rownum+1, column=0, padx=(0, 35))

    # Click action on the entry box
    def click(event):
        if input_entry.get() == 'Currency value.':
            input_entry.config(state=NORMAL)
            input_entry.delete(0, END)
        else:
            input_entry.config(state=NORMAL)
    # Unclick action on the entry box

    def unclick(event):
        if input_entry.get() == '':
            input_entry.delete(0, END)
            input_entry.insert(0, 'Currency value.')
            input_entry.config(state=DISABLED)
        else:
            input_entry.config(state=DISABLED)

    # Entry box for the amount
    input_entry = Entry(framecc, textvariable=amount, width=15, bg=bgcol)
    input_entry.grid(row=rownum+1, column=0, columnspan=1, padx=(0, 35))

    input_entry.insert(0, 'Currency value.')
    input_entry.config(state=DISABLED)

    # Binding Click and Unclick to the Entry box
    input_entry.bind("<Button-1>", click)
    input_entry.bind('<Leave>', unclick)

    # Result output Label
    result_label = Label(framecc, bg=bgcol, font=('Banschrift', 13), fg=fgcol)
    result_label.grid(row=rownum+2, column=0, columnspan=2)

    # Convert action button
    Cal_button = Button(framecc, text="Convert", bg=bgcol, fg=fgcol, command=lambda: Currency_Wigide_manager.convert(
        amt=amount, result_L=result_label, toChoice=choice_to, fromChoice=choice_from, FG=fgcol, BG=bgcol))
    Cal_button.grid(row=rownum+1, column=1)

    # Calendar Widgets

    # Calendar functions

    def LISTevents(date):

        global rem
        E_Wid = Toplevel(master=root)
        E_Wid.title("Event listing.")
        Label(master=E_Wid, text="All Events ").grid(row=0, column=0)
        op_field = Text(master=E_Wid, font="Courier 14", width=30)
        with open('reminder.json', 'r', encoding="utf8") as f:
            rem = json.load(f)
        s = ""
        for j in sorted(rem):
            for i in rem[j]:
                s += f"{j}:{i}\n"

        op_field.insert(END, s)
        op_field.config(state=DISABLED)
        op_field.grid(row=1, column=0)
        Button(E_Wid, text="Close", command=E_Wid.destroy).grid(
            row=2, column=0, sticky=S)

        E_Wid.mainloop()
    res_l = Text(master=framecal, width=32, height=17,
                 font="Courier 14", bg=bgcol, fg=fgcol)
    res_l.grid(row=2, column=0, columnspan=3, sticky=W)

    def ADDevent(date):
        global rem
        E_Wid = Toplevel(master=root)
        E_Wid.title("Event Adding.")
        Label(master=E_Wid, text=f"Date of the event {date}.").pack()
        E_Name = Entry(master=E_Wid)
        E_Name.pack()
        date = str(date)
        print(date)

        def ADDER():

            if date not in rem:

                rem[date] = []
            rem[date].append(str(E_Name.get()))
            print(rem)
            with open('reminder.json', 'w', encoding="utf8") as f:
                json.dump(rem, f)
            ans = messagebox.showinfo(
                title="successfully Added", message="Event added successfully to the Plans.")
            print(ans)

            E_Wid.destroy()
        Button(E_Wid, text="Add Event", command=ADDER).pack()

        E_Wid.mainloop()

    def DELevent(date):
        MessageDIS = "Select the event no. \n"
        date = str(date)
        MessageDIS = {}
        print(rem)
        try:
            for i in range(len(rem[date])):
                MessageDIS[(f"{i+1 :>3} : {rem[date][i] :>15}\n")] = i

        except KeyError:
            messagebox.showerror("Event Error", "No Events on the day.")
            return
        E_Wid = Toplevel(master=root)
        E_Wid.title("Event Deletion.")
        Label(master=E_Wid, text="Event Deletion").grid(row=0, column=1)
        Label(master=E_Wid, text="Event Ids : ").grid(row=1, column=0)
        del_date = StringVar()
        MenuDate = OptionMenu(E_Wid, del_date, *MessageDIS.keys())
        MenuDate.grid(row=1, column=1)

        def del_confirm():
            question = messagebox.showwarning(
                "Please confirm", "please confirm")
            if question:
                rem[date].pop(int(MessageDIS[del_date.get()])-1)
                if not (rem[date]):
                    del (rem[date])
                with open('reminder.json', 'w', encoding="utf8") as f:
                    json.dump(rem, f)
                E_Wid.destroy()

        Button(master=E_Wid, text="Ok",
               command=del_confirm).grid(row=2, column=0)
        Button(master=E_Wid, text="Cancel",
               command=E_Wid.destroy).grid(row=2, column=2)

        E_Wid.mainloop()

    cal = Calendar(framecal, font="Courier 14")
    cal.grid(row=0, column=0, sticky=W, columnspan=3)

    def listing_SELDATE(date):
        try:
            date = str(date)
            res_l.config(state=NORMAL)
            res_l.delete("1.0", END)
            # print(date)
            with open('reminder.json', 'r', encoding="utf8") as f:
                rem = json.load(f)
            if (not (rem)) or (date not in rem) or (not (rem[date])):
                res_l.insert(END, "No Plans.")
            elif date in rem:
                s = ""
                for j in rem[date]:
                    s += f"{date}:{j}\n"

                res_l.insert(END, s)
                res_l.config(state=DISABLED)

            Timer(1, lambda: listing_SELDATE(cal.selection_get())).start()
        except Exception:
            pass

    listing_SELDATE(cal.selection_get())

    with open('reminder.json', 'r', encoding="utf8") as f:
        rem = json.load(f)
        print(rem)

    choice_what = StringVar()
    choice_what.set("Add Event")
    functions = {"Add Event": ADDevent.__name__,
                 "List all Events": LISTevents.__name__, "Delete Event": DELevent.__name__}
    Label(framecal, text="Chose the Action :").grid(row=1, column=0, sticky=W)
    MenuFrom = OptionMenu(framecal, choice_what, *functions.keys())
    MenuFrom.grid(column=1, row=1, sticky=W)
    event_caller = Button(framecal, text="OK", command=lambda: eval(
        f"{functions[choice_what.get()]}(cal.selection_get())"))
    event_caller.grid(row=1, column=2, sticky='e')

    # framecal.bind('<Return>', lambda _: eval(f"{functions[choice_what.get()]}(cal.selection_get())"))
    # root.bind('<Return>', lambda _: eval(f"{functions[choice_what.get()]}(cal.selection_get())"))

    root.mainloop()
