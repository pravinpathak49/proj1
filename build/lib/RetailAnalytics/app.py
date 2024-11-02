from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import json
import plotly
import pkg_resources

app = Flask(__name__, template_folder=pkg_resources.resource_filename(__name__, 'templates'))

def load_data():
    data_path = pkg_resources.resource_filename(__name__, 'sales_data.csv')
    return pd.read_csv(data_path, parse_dates=['Date'])

@app.route('/')
def index():
    data = load_data()

    # Highest selling item
    highest_selling_item = data['Item'].value_counts().idxmax()

    # Highest profit generating item
    highest_profit_item = data.groupby('Item')['Profit'].sum().idxmax()

    # Best selling months
    best_selling_months = data['Date'].dt.to_period('M').value_counts().idxmax()

    # Transaction count month basis
    transaction_count_month = data['Date'].dt.to_period('M').value_counts()
    transaction_count_month = {str(k): v for k, v in transaction_count_month.items()}

    # Plotly charts
    item_counts = data['Item'].value_counts().reset_index()
    item_counts.columns = ['Item', 'Count']
    fig1 = px.bar(item_counts, x='Item', y='Count', title='Highest Selling Items')
    
    profit_by_item = data.groupby('Item')['Profit'].sum().reset_index()
    fig2 = px.bar(profit_by_item, x='Item', y='Profit', title='Highest Profit Generating Items')
    
    transaction_counts = data['Date'].dt.to_period('M').value_counts().reset_index()
    transaction_counts.columns = ['Month', 'Count']
    transaction_counts['Month'] = transaction_counts['Month'].astype(str)
    fig3 = px.bar(transaction_counts, x='Month', y='Count', title='Transaction Count by Month')

    # Convert Plotly figures to JSON for rendering in the template
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', 
                           highest_selling_item=highest_selling_item, 
                           highest_profit_item=highest_profit_item,
                           best_selling_months=str(best_selling_months),
                           transaction_count_month=transaction_count_month,
                           graph1JSON=graph1JSON,
                           graph2JSON=graph2JSON,
                           graph3JSON=graph3JSON)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()