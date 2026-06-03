import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv("hotel_bookings.csv")

    df['arrival_date'] = pd.to_datetime(
        df['arrival_date_year'].astype(str) + '-' +
        df['arrival_date_month'] + '-' +
        df['arrival_date_day_of_month'].astype(str),
        format='%Y-%B-%d',
        errors='coerce'
    )

    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['revenue'] = df['adr'] * df['total_nights']
    df = df[df['is_canceled'] == 0]
    return df

DF = load_data()

def get_revpar_by_month():
    monthly = DF.groupby(DF['arrival_date'].dt.to_period('M')).agg(
        total_revenue=('revenue', 'sum'),
        total_nights=('total_nights', 'sum'),
        avg_adr=('adr', 'mean'),
        bookings=('adr', 'count')
    ).reset_index()

    monthly['revpar'] = monthly['total_revenue'] / monthly['bookings']
    monthly['arrival_date'] = monthly['arrival_date'].astype(str)
    return monthly.tail(12).to_string(index=False)

def get_occupancy_vs_rate():
    monthly = DF.groupby(DF['arrival_date'].dt.to_period('M')).agg(
        bookings=('adr', 'count'),
        avg_adr=('adr', 'mean')
    ).reset_index()

    monthly['arrival_date'] = monthly['arrival_date'].astype(str)
    avg_bookings = monthly['bookings'].mean()
    avg_adr = monthly['avg_adr'].mean()

    leaks = monthly[
        (monthly['bookings'] > avg_bookings) &
        (monthly['avg_adr'] < avg_adr)
    ]

    if leaks.empty:
        return "No significant revenue leaks found in current data."
    return f"REVENUE LEAK ALERT - High occupancy but low ADR periods:\n{leaks.to_string(index=False)}"

def get_cancellation_analysis():
    all_df = pd.read_csv("hotel_bookings.csv")
    cancel_rate = all_df['is_canceled'].mean() * 100
    by_segment = all_df.groupby('market_segment')['is_canceled'].mean() * 100
    return f"Overall cancellation rate: {cancel_rate:.1f}%\n\nBy market segment:\n{by_segment.to_string()}"

def get_top_performing_months():
    monthly_rev = DF.groupby(DF['arrival_date'].dt.month_name())['revenue'].sum().sort_values(ascending=False)
    return f"Revenue by month (best to worst):\n{monthly_rev.to_string()}"

def get_lead_time_analysis():
    avg_lead = DF['lead_time'].mean()
    by_segment = DF.groupby('market_segment')['lead_time'].mean().sort_values(ascending=False)
    return f"Average booking lead time: {avg_lead:.0f} days\n\nBy segment:\n{by_segment.to_string()}"

def get_adr_trend():
    monthly_adr = DF.groupby(DF['arrival_date'].dt.to_period('M'))['adr'].mean().reset_index()
    monthly_adr['arrival_date'] = monthly_adr['arrival_date'].astype(str)
    return f"Monthly Average Daily Rate trend:\n{monthly_adr.tail(12).to_string(index=False)}"

def get_summary_stats():
    total_rev = DF['revenue'].sum()
    avg_adr = DF['adr'].mean()
    avg_nights = DF['total_nights'].mean()
    total_bookings = len(DF)

    return (
        f"HOTEL PERFORMANCE SUMMARY:\n"
        f"Total Revenue: ${total_rev:,.0f}\n"
        f"Total Bookings (confirmed): {total_bookings:,}\n"
        f"Average Daily Rate (ADR): ${avg_adr:.2f}\n"
        f"Average Length of Stay: {avg_nights:.1f} nights\n"
    )

def get_revpar_by_month_df():
    monthly = DF.groupby(DF['arrival_date'].dt.to_period('M')).agg(
        total_revenue=('revenue', 'sum'),
        avg_adr=('adr', 'mean'),
        bookings=('adr', 'count'),
        total_nights=('total_nights', 'sum')
    ).reset_index()

    monthly['revpar'] = monthly['total_revenue'] / monthly['bookings']
    monthly['arrival_date'] = monthly['arrival_date'].astype(str)
    return monthly.tail(12)

def get_revenue_by_month_df(start=None, end=None):
    monthly = DF.groupby(DF['arrival_date'].dt.to_period('M')).agg(
        total_revenue=('revenue', 'sum')
    ).reset_index()

    monthly['arrival_date'] = monthly['arrival_date'].dt.to_timestamp()

    if start is not None:
        start = pd.to_datetime(start)
        monthly = monthly[monthly['arrival_date'] >= start]

    if end is not None:
        end = pd.to_datetime(end)
        monthly = monthly[monthly['arrival_date'] <= end]

    monthly['month_label'] = monthly['arrival_date'].dt.strftime('%B %Y')
    return monthly

def get_revenue_between_dates(start, end):
    df = get_revenue_by_month_df(start=start, end=end)
    if df.empty:
        return f"No revenue data found between {start} and {end}."
    return df[['month_label', 'total_revenue']].to_string(index=False)
