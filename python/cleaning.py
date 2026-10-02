import pandas as pd

def load_events_clean(path):
    df = pd.read_csv(path)

    df = df[df['is_test'] == False]

    revenue_usd_series = df['revenue_usd'].str.strip().str.replace(',', '.')
    revenue_usd_series = pd.to_numeric(revenue_usd_series, errors='coerce')
    unparseable_count = revenue_usd_series.isna().sum()
    revenue_usd_series = revenue_usd_series.fillna(0.0)

    df['revenue_usd'] = revenue_usd_series

    country_series = df['country'].str.strip().str.upper()
    country_series = country_series.where(country_series.str.fullmatch("[A-Z]{2}"), "XX")
    df['country'] = country_series

    df['event_time'] = pd.to_datetime(df['event_time'], utc=True, errors='coerce')
    df['ingested_at'] = pd.to_datetime(df['ingested_at'], utc=True, errors='coerce')

    bad = (df['event_id'].str.strip() == '') | df['event_id'].isna() | df['event_time'].isna() | df['ingested_at'].isna()
    quarantined_rows = df[bad]
    df = df[~bad]

    df = df.sort_values(by=['event_id', 'ingested_at'], kind='stable')
    df = df.drop_duplicates('event_id', keep='last')

    df = df.sort_index().reset_index(drop=True)

    return df, quarantined_rows, unparseable_count


df, quarantined_rows, unparseable_count = load_events_clean('data/events_raw.csv')

print(df)
print(quarantined_rows)
print(unparseable_count)