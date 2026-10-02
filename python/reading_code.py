import pandas as pd

def load_daily(path, day):
    df = pd.read_csv(path)
    df = df[df['is_test'] == False]

    df['event_time'] = pd.to_datetime(df['event_time'], utc=True, errors='coerce')
    df['ingested_at'] = pd.to_datetime(df['ingested_at'], utc=True, errors='coerce')

    df = df.sort_values(by=['event_id', 'ingested_at'], kind='stable').drop_duplicates('event_id', keep='last')

    df = df[df['event_time'].dt.date == pd.to_datetime(day).date()]
    
    df["revenue_usd"] = pd.to_numeric(df['revenue_usd'].str.strip().str.replace(',', '.'), errors='coerce').fillna(0.0)

    return df.groupby(['app_id', 'media_source'])['revenue_usd'].sum().sort_values(ascending=False)


print(load_daily('data/events_raw.csv', "2026-08-11"))