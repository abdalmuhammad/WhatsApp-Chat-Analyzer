import re
import pandas as pd
def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2}\s?[AP]M)\s-\s([^:]+?):\s(.*)'

    matches = re.findall(pattern, data)
    df = pd.DataFrame(matches, columns=['Date', 'Time', 'User', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'])

    df['Year'] = df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Day_name'] = df['Date'].dt.day_name()
    busy_day = df['Day_name'].value_counts()
    busy_month = df['Month'].value_counts()
    df['Hour'] = df['Datetime'].dt.hour
    df['Minute'] = df['Datetime'].dt.minute

    return df