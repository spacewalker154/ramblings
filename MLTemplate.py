import pandas as pd

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

from tkinter import *
from tkinter import colorchooser
from tkinter import ttk

from moneyed import Money
from moneyed.l10n import format_money
from currency_converter import CurrencyConverter

instructions = "This program predicts the price of houses. To get started go to the main menu\
and select either the house or loan function and the currency"

#default colour
bcolour = "white"

# Path of the files to read
house_file_path = 'C:/Users/KnanE/source/repos/PythonMLProj/Data/Iowa/IowaTrain.csv'
loan_file_path = 'C:/Users/KnanE/source/repos/PythonMLProj/Data/loan/loan_data_set.csv'

#Optimal max leaf nodes
house_leaf_nodes = 71

loan_leaf_nodes = 2

#create entry to only allow integers to be entered
class int_entry(Entry):
    def __init__(self, master=None, **kwargs):
        self.var = StringVar()
        Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        if self.get().isdigit() or self.get() == "": 
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            # there's non-digit characters in the input; reject this 
            self.set(self.old_value)

# initialise currency converter, fallback on linear interpolation for missing rates
converter = CurrencyConverter(fallback_on_missing_rate=True)

#function to convert float to string data type displaying money
def toMoney(value, currency):
    
    #convert from dollars
    moneyValue = converter.convert(value, 'USD', currency)
    round(moneyValue,2)
    #format as money, adds symbols for the specified currency
    moneyValue = format_money(Money(moneyValue, currency), locale='en_US')
    #convert to string so it can be handled easier
    moneyValue = str(moneyValue)
    return moneyValue


#make house prediction
def house_predict(LotArea, YearBuilt, FstFlrSF, ScndFlrSF, FullBath, BedroomAbvGr, TotRmsAbvGrd):
    global house_model
    global price_prediction
    global priceFloat
    user_features = [[LotArea, YearBuilt, FstFlrSF, ScndFlrSF, FullBath, BedroomAbvGr, TotRmsAbvGrd]]
    price_prediction = house_model.predict(user_features)
    round(price_prediction[0], 2) #price_prediction is an array
    print("Price prediction when specifying maximum leaf nodes (",house_leaf_nodes,"): ",price_prediction)
    priceFloat = float(price_prediction)
    return priceFloat

#make loan prediction
def loan_predict(Married, Dependents, Education, Self_Employed, ApplicantIncome,\
   CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area):
    global acceptAmount
    user_features = [[LotArea, YearBuilt, FstFlrSF, ScndFlrSF, FullBath, BedroomAbvGr, TotRmsAbvGrd]]
    accept_prediction = loan_model.predict(user_features)
    round(accept_prediction[0], 2) #accept_prediction is an array
    print("accept prediction when specifying maximum leaf nodes (",loan_leaf_nodes,"): ",accept_prediction)
    acceptAmount = float(accept_prediction)
    return acceptAmount
   
def house_window():
    #create window
    global house
    house = Tk()
    house.geometry("400x400")
    house.title("House Price Predictor entry")
    house.resizable (False, False)
    house.configure(background = bcolour)

    house.columnconfigure(0, weight=1)
    house.rowconfigure(1, weight=1)

    #when submit button pressed
    def submit():
        if len(UserLotArea.get())!= 0 and\
           len(UserYearBuilt.get())!= 0 and\
           len(UserFstFlrSF.get())!= 0 and\
           len(UserScndFlrSF.get())!= 0 and\
           len(UserFullBath.get())!= 0 and\
           len(UserBedroomAbvGr.get())!= 0 and\
           len(UserTotRmsAbvGrd.get()) != 0:
            
            global result
            result = house_predict(\
               UserLotArea.get(),\
               UserYearBuilt.get(),\
               UserFstFlrSF.get(),\
               UserScndFlrSF.get(),\
               UserFullBath.get(),\
               UserBedroomAbvGr.get(),\
               UserTotRmsAbvGrd.get())
            
            result_window()
            resultW.mainloop()

    #back function
    def back():
        house.destroy()
        main_window()
        return

    #frame to contain heading
    frame_heading = Frame(house)
    frame_heading.grid(row=0, column=0, columnspan=2, padx=30, pady=5)


    #frame to contain user entries
    frame_entry = Frame(house)
    frame_entry.grid(row=1, column=0, columnspan=2, padx=25, pady=10)
    frame_entry.configure(background = bcolour)

    for row_num in range(house.grid_size()[0]):
        for row_num in range(house.grid_size()[1]):
            house.rowconfigure(row_num,minsize = 60 ,weight = 3)
        house.rowconfigure(row_num, minsize = 60 ,weight = 1)


    #place form heading
    Label(frame_heading, text = "Enter details", font=('Arial',16)).grid(row=0, column=0, padx=0, pady=5)

    #place labels
    Label(frame_entry, text = "Lot Area").grid(row=0,column=0, padx=10, pady=5)
    Label(frame_entry, text = "Year built").grid(row=1, column=0, padx=10, pady=10)
    Label(frame_entry, text = "First floor square feet").grid(row = 2, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Second floor square feet").grid(row = 3, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Full bathrooms").grid(row = 4, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Bedrooms above ground").grid(row = 5, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Total rooms above ground").grid(row = 6, column=0, padx=10, pady=10)

    #place buttons

    submit_button = Button(house, text="Submit", width = 7, command=submit)
    submit_button.grid(row=8, column=0, padx=0, pady=5)
    back_button = Button(house, text="Back", width = 7, command=back)
    back_button.grid(row=8,column=1,padx=0,pady=5)

    #text entry
    UserLotArea = int_entry(frame_entry, width=15, bg = "white")
    UserLotArea.grid(row=0, column=1, padx=5, pady=5)

    UserYearBuilt = int_entry(frame_entry, width=15, bg = "white")
    UserYearBuilt.grid(row=1, column=1, padx=5, pady=5)

    UserFstFlrSF = int_entry(frame_entry, width=15, bg = "white")
    UserFstFlrSF.grid(row=2, column=1, padx=5, pady=5)

    UserScndFlrSF = int_entry(frame_entry, width=15, bg = "white")
    UserScndFlrSF.grid(row=3, column=1, padx=5, pady=5)

    UserFullBath = int_entry(frame_entry, width=15, bg = "white")
    UserFullBath.grid(row=4, column=1, padx=5, pady=5)

    UserBedroomAbvGr = int_entry(frame_entry, width=15, bg = "white")
    UserBedroomAbvGr.grid(row=5, column=1, padx=5, pady=5)

    UserTotRmsAbvGrd = int_entry(frame_entry, width=15, bg = "white")
    UserTotRmsAbvGrd.grid(row=6, column=1, padx=5, pady=5)

def loan_window():
    #create window
    global loan
    loan = Tk()
    loan.geometry("400x400")
    loan.title("loan Price Predictor entry")
    loan.resizable (False, False)
    loan.configure(background = bcolour)

    loan.columnconfigure(0, weight=1)
    loan.rowconfigure(1, weight=1)

    #when submit button pressed
    def submit():
        if len(UserLotArea.get())!= 0 and\
           len(UserYearBuilt.get())!= 0 and\
           len(UserFstFlrSF.get())!= 0 and\
           len(UserScndFlrSF.get())!= 0 and\
           len(UserFullBath.get())!= 0 and\
           len(UserBedroomAbvGr.get())!= 0 and\
           len(UserTotRmsAbvGrd.get()) != 0:

            global result
            result = loan_predict(\
               UserLotArea.get(),\
               UserYearBuilt.get(),\
               UserFstFlrSF.get(),\
               UserScndFlrSF.get(),\
               UserFullBath.get(),\
               UserBedroomAbvGr.get(),\
               UserTotRmsAbvGrd.get())
            
            result_window()
            resultW.mainloop()

    #back function
    def back():
        loan.destroy()
        main_window()
        return

    #frame to contain heading
    frame_heading = Frame(loan)
    frame_heading.grid(row=0, column=0, columnspan=2, padx=30, pady=5)


    #frame to contain user entries
    frame_entry = Frame(loan)
    frame_entry.grid(row=1, column=0, columnspan=2, padx=25, pady=10)
    frame_entry.configure(background = bcolour)

    for row_num in range(loan.grid_size()[0]):
        for row_num in range(loan.grid_size()[1]):
            loan.rowconfigure(row_num,minsize = 60 ,weight = 3)
        loan.rowconfigure(row_num, minsize = 60 ,weight = 1)


    #place form heading
    Label(frame_heading, text = "Enter details", font=('Arial',16)).grid(row=0, column=0, padx=0, pady=5)

    #place labels
    Label(frame_entry, text = "Lot Area").grid(row=0,column=0, padx=10, pady=5)
    Label(frame_entry, text = "Year built").grid(row=1, column=0, padx=10, pady=10)
    Label(frame_entry, text = "First floor square feet").grid(row = 2, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Second floor square feet").grid(row = 3, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Full bathrooms").grid(row = 4, column=0, padx=10, pady=10) # change
    Label(frame_entry, text = "Bedrooms above ground").grid(row = 5, column=0, padx=10, pady=10)
    Label(frame_entry, text = "Total rooms above ground").grid(row = 6, column=0, padx=10, pady=10)

    #place buttons

    submit_button = Button(loan, text="Submit", width = 7, command=submit)
    submit_button.grid(row=8, column=0, padx=0, pady=5)
    back_button = Button(loan, text="Back", width = 7, command=back)
    back_button.grid(row=8,column=1,padx=0,pady=5)

    #text entry
    UserLotArea = int_entry(frame_entry, width=15, bg = "white")
    UserLotArea.grid(row=0, column=1, padx=5, pady=5)

    UserYearBuilt = int_entry(frame_entry, width=15, bg = "white")
    UserYearBuilt.grid(row=1, column=1, padx=5, pady=5)

    UserFstFlrSF = int_entry(frame_entry, width=15, bg = "white") #these need changing
    UserFstFlrSF.grid(row=2, column=1, padx=5, pady=5)

    UserScndFlrSF = int_entry(frame_entry, width=15, bg = "white")
    UserScndFlrSF.grid(row=3, column=1, padx=5, pady=5)

    UserFullBath = int_entry(frame_entry, width=15, bg = "white")
    UserFullBath.grid(row=4, column=1, padx=5, pady=5)

    UserBedroomAbvGr = int_entry(frame_entry, width=15, bg = "white")
    UserBedroomAbvGr.grid(row=5, column=1, padx=5, pady=5)

    UserTotRmsAbvGrd = int_entry(frame_entry, width=15, bg = "white")
    UserTotRmsAbvGrd.grid(row=6, column=1, padx=5, pady=5)

def result_window():
    #create window
    global resultW
    resultW = Tk()
    resultW.geometry("400x400")
    resultW.title("Prediction Results")
    resultW.resizable (False, False)
    resultW.configure(background = bcolour)

    #format data in user friendly format
    display_mae = toMoney(val_mae,currency)
    display_pred = toMoney(priceFloat,currency)

    #labels
    Label(resultW, text = "mean absolute error: {0}".format(display_mae))\
        .grid(row=0,rowspan=1,column=0,columnspan = 4, padx=10, pady=5,)

    Label(resultW, text = "Price Prediction: {0}".format(display_pred))\
        .grid(row = 1,rowspan=1 ,column=0, columnspan=4, padx=10, pady=5,)

    result_box = Text(resultW, bg=bcolour, height=5, )  

#help screen

def help_window():
    #create window
    global help
    help = Tk()
    help.geometry("400x400")
    help.title("Help Menu")
    help.resizable (False, False)
    help.configure(background = bcolour)

    help.columnconfigure(0, weight=1)
    help.rowconfigure(1, weight=1)

    #instructions
    text = Text(help, height=8)
    text.grid(row=0, column = 0)

    text.insert('1.0', instructions)
    text['state'] = 'disabled'

    def choose_colour():
 
        # variable to store hexadecimal code of color
        colour_code = colorchooser.askcolor(title ="Choose colour")
        global bcolour
        bcolour= colour_code[1]
        help.configure(bg=colour_code[1])
 
    colour_button = Button(help, text = "Select colour", command = choose_colour)
    colour_button.grid(row=8,column=2,padx=0,pady=5)


    #back function
    def back():
        help.destroy()
        main_window()
        return

    #back button
    back_button = Button(help, text="Back", width = 7, command=back)
    back_button.grid(row=8,column=1,padx=0,pady=5)

#main menu

def main_window():

    global main
    main = Tk()
    main.geometry("400x400")
    main.title("House Price Predictor")
    main.resizable(False,False)
    main.configure(background = bcolour)

    #frame to contain heading
    frame_heading = Frame(main)
    frame_heading.grid(row=0, column=0, columnspan=2, padx=30, pady=5)

    #frame to contain user entries
    frame_select = Frame(main)
    frame_select.grid(row=1, column=0, columnspan=2, padx=25, pady=10)
    frame_select.configure(background = bcolour)

    

    #button commands
    def start():
        global currency
        currency = mOption.get()
        current_var = Combo.get()
        if current_var == "House" and currency != "Pick a currency":
 

            main.destroy()
            house_window()
          
        elif current_var == "Loan":
            print("hello")
        else:
            return


    def help_open():
        main.destroy()
        help_window()
        help.mainloop()
    def exit():
        main.destroy()
        return

    #List of program functions
    vlist = ["House", "Loan"]

    #list of accepted currencies
    mlist = ["USD",	"JPY",	"BGN",	"CZK",	"DKK",  "EUR",	"GBP", "HUF", "PLN",\
    "ROL",  "RON",	"SEK",	"CHF",	"ISK",	"NOK",	"HRK",  "TRY",	"AUD",	"BRL",\
    "CAD",	"CNY",  "HKD",	"IDR",	"ILS",	"INR",	"KRW",  "MXN", "MYR",	"NZD",\
    "PHP",	"SGD",	"THB",	"ZAR"]

    mlist.sort()

    #dropdown menu for selecting function
    Combo = ttk.Combobox(frame_select, values = vlist)
    Combo['state'] = 'readonly'
    Combo.set("Pick an Option")
    Combo.grid(row = 4,column = 2, columnspan = 3, padx = 5, pady = 5)

    #dropdown menu for selecting currency
    mOption = ttk.Combobox(frame_select, values = mlist)
    mOption['state'] = 'readonly'
    mOption.set("Pick a currency")
    mOption.grid(row = 4,column = 6, columnspan = 3, padx = 5, pady = 5)

    

    image=PhotoImage(file="C:/Users/KnanE/source/repos/PythonMLProj/house400.png")

    #Label(main,image=image).grid(row = 0, column = 0)

    #menu
    mainmenu = Menu(main)
    mainmenu.add_command(label = "Start", command= start)  
    mainmenu.add_command(label = "Help", command= help_open)
    mainmenu.add_command(label = "Exit", command= main.destroy)
    
    main.config(menu = mainmenu)
    main.mainloop()

#train house model for use


#house prediction

house_data = pd.read_csv(house_file_path)

# Create target object and call it y
y = house_data.SalePrice

# Create X
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr',
            'TotRmsAbvGrd']
X = house_data[features]

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Specify Model
house_model = DecisionTreeRegressor(random_state=1)
# Fit Model
house_model.fit(train_X, train_y)

# Using best value for max_leaf_nodes make predictions and calculate mean absolute error
house_model = DecisionTreeRegressor(max_leaf_nodes= house_leaf_nodes , random_state=1)
house_model.fit(train_X, train_y)
val_predictions = house_model.predict(val_X)
global val_mae
val_mae = mean_absolute_error(val_predictions, val_y)

print("Validation mean absolute error for best value of max_leaf_nodes: {:,.0f}".format(val_mae))


global accept_prediction



#second function
#loan prediction

loan_data = pd.read_csv(loan_file_path)

# Create target object and call it y
y = loan_data.Loan_Status

# Create X
loan_attributes = ['Married','Dependents','Education','Self_Employed','ApplicantIncome','CoapplicantIncome',
            'LoanAmount','Loan_Amount_Term','Credit_History',]

X = loan_data[loan_attributes]

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Specify Model
loan_model = DecisionTreeRegressor(random_state=1)
# Fit Model
loan_model.fit(train_X, train_y)

# Using best value for max_leaf_nodes make predictions and calculate mean absolute error
loan_model = DecisionTreeRegressor(max_leaf_nodes= loan_leaf_nodes , random_state=1)
loan_model.fit(train_X, train_y)
val_predictions = loan_model.predict(val_X)
loan_mae = mean_absolute_error(val_predictions, val_y)
print(loan_mae)
percentage_error = (loan_mae*100)
print("Validation mean absolute error for best value of max_leaf_nodes: {:,.0f}%".format(percentage_error))


main_window()

#test values
#11622, 1961, 896, 0, 1, 2, 5

