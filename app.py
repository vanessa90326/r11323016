import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import plotly.express as px
from webcrawler import webcrawler

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Hotel Data Dashboard"),
    
    dcc.Input(id='location-input', type='text', placeholder='Enter Location'),
    
    dcc.DatePickerRange(
        id='date-input',
        start_date= datetime.today().date(),
        end_date= datetime.today().date()+ timedelta(days=1)
    ),

    html.Button('ENTER', id='enter-button', n_clicks=0),
    
    dcc.Graph(id='scatter-plot'),
])

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('enter-button', 'n_clicks')],
    [Input('location-input', 'value'),
     Input('date-input', 'start_date'),
     Input('date-input', 'end_date')]
)
def update_scatter_plot(n_clicks, location, start_date, end_date):

    if n_clicks > 0:

        data = webcrawler(location, start_date, end_date)

        fig = px.scatter(data, x='price', y='distance', color='ratings',
                        title=f'Hotel Price and Distance Scatter Plot in {location} from {start_date} to {end_date}',
                        labels={'price': 'Price', 'distance': 'Distance', 'ratings': 'Ratings'})

        return fig
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
