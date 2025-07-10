import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Sample mock data simulating Aggregated_user table
data = {
    'State': ['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu', 'Gujarat'],
    'Year': [2021, 2021, 2021, 2021, 2021],
    'Quarter': [1, 1, 1, 1, 1],
    'Brand': ['PhonePe', 'Google Pay', 'Paytm', 'PhonePe', 'Google Pay'],
    'Transaction_count': [150000, 120000, 95000, 140000, 110000],
    'Transaction_amount': [20000000, 18000000, 13000000, 19000000, 16000000],
}

# Create DataFrame
df = pd.DataFrame(data)

# Initialize Dash app
app = Dash(__name__)
app.title = "PhonePe Transaction Dashboard"

# App layout
app.layout = html.Div([
    html.H1("PhonePe Transactions - Aggregated User Data", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Brand:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='brand-dropdown',
            options=[{'label': b, 'value': b} for b in df['Brand'].unique()],
            value='PhonePe',
            clearable=False
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='transaction-graph'),

    html.Div(id='summary', style={'textAlign': 'center', 'marginTop': 20, 'fontSize': 18})
])

# Callback to update graph and summary
@app.callback(
    Output('transaction-graph', 'figure'),
    Output('summary', 'children'),
    Input('brand-dropdown', 'value')
)
def update_dashboard(selected_brand):
    # Filter based on selected brand
    filtered = df[df['Brand'] == selected_brand]

    # Bar plot
    fig = px.bar(
        filtered, x='State', y='Transaction_amount',
        color='State', title=f"Transaction Amount by State for {selected_brand}",
        labels={'Transaction_amount': 'Amount (INR)'},
        text_auto='.2s'
    )

    fig.update_layout(yaxis_title='Transaction Amount (INR)', xaxis_title='State')

    # Summary text
    total_amt = filtered['Transaction_amount'].sum()
    total_cnt = filtered['Transaction_count'].sum()
    summary = f"📊 Total Transactions: {total_cnt:,} | 💰 Total Amount: ₹{total_amt:,}"

    return fig, summary

# Run the app
if __name__ == '__main__':
   app.run(debug=True, use_reloader=False)


