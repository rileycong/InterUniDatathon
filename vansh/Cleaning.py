import pandas as pd

df = pd.read_csv('../data/train.csv')

print(df.info())

# long & lati: cleaning all the data from it

print(df.isnull().sum())

df_cleaned_latlon = df.dropna(subset=['Latitude', 'Longitude'])

print(df_cleaned_latlon.isnull().sum())


#formatting date in 24hrs


def standard_time(time_str):
    try:
        if 'AM' in time_str or 'PM' in time_str:
            return pd.to_datetime(time_str, format='%I:%M:%S %p').strftime('%H:%M:%S')
        
        return pd.to_datetime(time_str, format='%H:%M:%S').strftime('%H:%M:%S')
    
    except (ValueError, TypeError):
        try:
            parts = time_str.split('/')
            corrected_time = f'{parts[0]}:{parts[1]}:{parts[2]}'
            return pd.to_datetime(corrected_time, format='%H:%M:%S').strftime('%H:%M:%S')
        except Exception:
            return 'NOPES'

df_cleaned_latlon['TransactionTime'] = df_cleaned_latlon['TransactionTime'].apply(standard_time)
print(df_cleaned_latlon.isnull().sum())


#spliting month and date and adding weekday

df_cleaned_latlon['TransactionDate'] = pd.to_datetime(df_cleaned_latlon['TransactionDate'], dayfirst=True)

df_cleaned_latlon['date'] = df_cleaned_latlon['TransactionDate'].dt.day   
df_cleaned_latlon['Month'] = df_cleaned_latlon['TransactionDate'].dt.month  

df_cleaned_latlon['weekday'] = df_cleaned_latlon['TransactionDate'].dt.day_name()


#standard form genders

gender_mapping = {
    'fem': 'Female',
    'Female': 'Female',
    'she': 'Female',
    'woman': 'Female',
    'he': 'Male',
    'man': 'Male',
    'Male': 'Male',
    'isnotfemale': 'Male',
    'isnotmale': 'Female',
}

df_cleaned_latlon['Gender'] = df_cleaned_latlon['Gender'].map(gender_mapping).fillna('Other')