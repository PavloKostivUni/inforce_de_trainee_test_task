# python -m a_small_pipeline --input ../data/ --output ../out/ --since 2026-01-01

import pandas as pd
import argparse
from pathlib import Path
import shutil


def load_events_clean(path, since):
    df = pd.read_csv(path)

    df['event_time'] = pd.to_datetime(df['event_time'], utc=True, errors='coerce')
    df['ingested_at'] = pd.to_datetime(df['ingested_at'], utc=True, errors='coerce')

    df = df[df['ingested_at'].isna() | (df['ingested_at'] >= since)]
    rows_in = len(df)

    bad = (df['event_id'].str.strip() == '') | df['event_id'].isna() | df['event_time'].isna() | df['ingested_at'].isna()
    quarantined_rows = df[bad]
    df = df[~bad]

    df = df[df['is_test'] == False]

    revenue_usd_series = df['revenue_usd'].str.strip().str.replace(',', '.')
    revenue_usd_series = pd.to_numeric(revenue_usd_series, errors='coerce')
    unparseable_count = revenue_usd_series.isna().sum()
    revenue_usd_series = revenue_usd_series.fillna(0.0)

    df['revenue_usd'] = revenue_usd_series

    country_series = df['country'].str.strip().str.upper()
    country_series = country_series.where(country_series.str.fullmatch("[A-Z]{2}"), "XX")
    df['country'] = country_series

    return df, quarantined_rows, unparseable_count, rows_in

def remove_duplicates(df):
    df = df.sort_values(by=['event_id', 'ingested_at'], kind='stable')
    return df.drop_duplicates('event_id', keep='last')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--since', required=True)
    args = parser.parse_args()

    since = pd.Timestamp(args.since, tz='UTC')
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    df, quarantined_rows, unparseable_count, rows_in = load_events_clean(Path(args.input) / 'events_raw.csv', since)
    rows_before_removing_duplicates = len(df)
    df = remove_duplicates(df)
    rows_out = len(df)

    events_out_path = out / 'events'
    if events_out_path.exists():
        old_df = pd.read_parquet(events_out_path)
        df = pd.concat([old_df, df], ignore_index=True)
        df = remove_duplicates(df)

    df['event_date'] = df['event_time'].dt.strftime('%Y-%m-%d')
    shutil.rmtree(events_out_path, ignore_errors=True)          # Delete old parquet files
    df.to_parquet(events_out_path, partition_cols=['event_date'])

    quarantined_rows.to_csv(out / 'quarantined.csv', index=False)

    print(f"rows in: {rows_in}, rows out: {rows_out}, duplicates removed: {rows_before_removing_duplicates - rows_out}, rows quarantined: {len(quarantined_rows)}")


if __name__ == '__main__':
    main()