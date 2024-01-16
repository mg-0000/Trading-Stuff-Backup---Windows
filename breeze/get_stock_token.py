# from breeze_import import breeze
import pandas as pd
import warnings 
    
# Settings the warnings to be ignored 
warnings.filterwarnings('ignore') 

# expiry = '28-Dec-2023
# right = 'CE'/'PE'
# strike = 49400
def get_token(expiry, strike, right):
    read_file = pd.read_csv('FONSEScripMaster.txt')
    token = read_file[read_file["InstrumentName"]=="OPTIDX"][read_file["ShortName"]=="CNXBAN"][read_file["Series"]=="OPTION"][read_file["ExpiryDate"]==expiry][read_file["StrikePrice"]==(strike)][read_file["OptionType"]==right]
    print(token["Token"].values[0])
    return token["Token"].values[0]
    # read_file.to_csv ('FONSEScripMaster.csv', index=None)

token = get_token("17-Jan-2024", 48100, "PE")
# print(token)
