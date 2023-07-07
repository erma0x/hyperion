import yfinance as yf


start_date = "2023-03-17"
end_date = "2023-04-16"

configurations = ('1',{'ticker': 'USDCHF=X', 'interval': '90m', 'tp': 0.00938302297660149, 'sl': 0.004719542238683867, 'ma_long': 162, 'ma_short': 17})

print(configurations[1]['ticker'])
print(configurations[1]['interval'])

# Set the start and end times for the data request
start_time = '2023-03-01'
end_time = '2023-04-15'

# Retrieve the data for USDCHF=X within the specified time range
data = yf.download('USDCHF=X', period="60d", interval='90m')
