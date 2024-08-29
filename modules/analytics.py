import pandas as pd

def get_detailed_session_analytics(df):
    df['hour'] = df['start_time'].dt.hour
    session_distribution = df.groupby('hour')['duration'].sum().sort_values(ascending=False)

    df['week'] = df['start_time'].dt.isocalendar().week
    weekly_trends = df.groupby('week')['duration'].sum().sort_values(ascending=False)

    df['month'] = df['start_time'].dt.month
    monthly_trends = df.groupby('month')['duration'].sum().sort_values(ascending=False)

    return {
        'session_distribution': session_distribution,
        'weekly_trends': weekly_trends,
        'monthly_trends': monthly_trends
    }

def analyze_gaming_habits(df):
    df['hour'] = df['start_time'].dt.hour
    late_night_sessions = df[(df['hour'] >= 22) | (df['hour'] <= 6)]
    
    total_late_night_hours = late_night_sessions['duration'].sum()
    total_hours = df['duration'].sum()
    
    percentage_late_night = (total_late_night_hours / total_hours) * 100

    if percentage_late_night > 20:
        print("Consider taking breaks during late-night gaming sessions.")
    
    return percentage_late_night

# Example usage:
if __name__ == "__main__":
    conn = create_db_connection()
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    analytics = get_detailed_session_analytics(df)
    late_night_percentage = analyze_gaming_habits(df)
    print(f"Percentage of late-night gaming: {late_night_percentage:.2f}%")
    conn.close()
