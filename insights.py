import pandas as pd

def generate_customer_insights(df):
    insights = {}

    # Check if 'purchase_amount' column exists
    if 'purchase_amount' in df.columns:
        insights['Total Customers'] = len(df)
        insights['Average Purchase'] = round(df['purchase_amount'].mean(), 2)
        insights['High Spending Customers'] = df[df['purchase_amount'] > df['purchase_amount'].mean()].shape[0]
    else:
        insights['Total Customers'] = len(df)
        insights['Average Purchase'] = 'N/A'
        insights['High Spending Customers'] = 'N/A'

    # Check if 'category' column exists
    if 'category' in df.columns:
        insights['Top Category'] = df['category'].mode()[0]
    else:
        insights['Top Category'] = 'N/A'

    # Convert dictionary to DataFrame
    insights_df = pd.DataFrame([insights])  # ✅ Ensure it's a DataFrame

    return insights_df  # ✅ Always return DataFrame
