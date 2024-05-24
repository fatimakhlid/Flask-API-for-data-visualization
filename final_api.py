from flask import Flask, request, jsonify
import pandas as pd
import plotly.express as px

app = Flask(__name__)

df = pd.read_csv("dubai_real_estate_data.csv")
df['Price'] = pd.to_numeric(df['Price'].replace({'[AED\.]': ''}, regex=True), errors='coerce')
df.dropna(subset=['Price'], inplace=True)

def generate_max_price_per_location(df, data):
    year = data.get('year')
    start_month = data.get('start_month', 1)
    end_month = data.get('end_month', 12)
    location = data.get('location', None)

    if year:
        df = df[df['Date'].str.contains(str(year))] 
    if location:
        df = df[df['Location'] == location]

    df['Month'] = pd.to_datetime(df['Date']).dt.month
    df = df[(df['Month'] >= start_month) & (df['Month'] <= end_month)]
    
    grouped = df.groupby(['Location', 'Date', 'Month'])['Price'].max().reset_index()

    fig = px.bar(grouped, x='Month', y='Price', color='Location',
                 title="Maximum Price Trends",
                 labels={'Location': 'Location', 'Price': 'Maximum Price (AED)'},
                 hover_data={'Location': True, 'Price': True, 'Date': True, 'Month': True},
                 text='Price', barmode='group')
    return fig.to_html()

@app.route('/api/max_price', methods=['POST'])
def max_price_api():
    data = request.json
    result_html = generate_max_price_per_location(df, data)
    print(result_html)
    return result_html

if __name__ == '__main__':
    app.run()
