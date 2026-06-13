import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 1. Load Data
df = pd.read_csv('bmw.csv')

# Clean data slightly (ensure numeric types)
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')
df = df.dropna(subset=['year', 'price', 'mileage', 'model'])

# 1.1 Simple ML Model for Price Prediction
le = LabelEncoder()
df_ml = df.copy()
df_ml['model_encoded'] = le.fit_transform(df_ml['model'])
X = df_ml[['model_encoded', 'year', 'mileage']]
y = df_ml['price']
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X, y)

# Initialize Dash application
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server
app.title = "The Best Cars — BMW"

# 2. Application Layout
app.layout = html.Div(className='app-container', children=[
    
    # Header
    html.Div(className='header', children=[
        html.Img(
            src=app.get_asset_url('logo.png'), 
            className='header-logo'
        ),
        html.Div(className='header-text', children=[
            html.H1("The Best Cars - BMW", style={'color': "#e71010", 'margin': '0', 'fontSize': '24px', 'fontFamily': 'Arial, sans-serif'}),
            html.P("Second-hand cars descriptor", style={'color': "#638FEF", 'margin': '0', 'fontFamily': 'Arial, sans-serif'})
        ])
    ]),

    # Main content with Sidebar
    html.Div(className='main-content', children=[
        
        # Sidebar
        html.Div(className='sidebar', children=[
            
            # Global Filters Section
            html.Div(className='global-filters', style={'padding': '20px', 'borderBottom': '1px solid #333'}, children=[
                html.H4("Global Filters", style={'color': 'white', 'marginBottom': '10px'}),
                html.Label("Model Selection:", style={'color': '#638FEF', 'fontSize': '12px'}),
                dcc.Dropdown(
                    id='global-model-filter', 
                    options=[{'label': m, 'value': m} for m in sorted(df['model'].unique())], 
                    multi=True, 
                    placeholder="All Models",
                    className='dark-dropdown'
                ),
                html.Br(),
                html.Label("Year Range:", style={'color': '#638FEF', 'fontSize': '12px'}),
                dcc.RangeSlider(
                    id='global-year-filter', 
                    min=int(df['year'].min()), 
                    max=int(df['year'].max()), 
                    value=[int(df['year'].min()), int(df['year'].max())],
                    marks={i: str(i) for i in range(int(df['year'].min()), int(df['year'].max())+1, 5)},
                    step=1
                ),
            ]),

            dcc.Tabs(id="tabs-inline", value='tab-overview', vertical=True, children=[
                dcc.Tab(label='Market Overview', value='tab-overview', className='custom-tab', selected_className='custom-tab--selected'),
                dcc.Tab(label='Efficiency', value='tab-efficiency', className='custom-tab', selected_className='custom-tab--selected'),
                dcc.Tab(label='Compare Series', value='tab-compare', className='custom-tab', selected_className='custom-tab--selected'),
                dcc.Tab(label='Price Predictor', value='tab-prediction', className='custom-tab', selected_className='custom-tab--selected'),
                dcc.Tab(label='Smart Choice', value='tab-selection', className='custom-tab', selected_className='custom-tab--selected'),
                dcc.Tab(label='About/Help', value='tab-about', className='custom-tab', selected_className='custom-tab--selected'),
            ], colors={"border": "transparent", "primary": "transparent", "background": "transparent"}),
        ]),
        
        # Content Area
        html.Div(className='content-area', children=[
            # KPI Cards Row
            html.Div(id='kpi-cards-container', className='flex-responsive-row', style={'gap': '20px', 'marginBottom': '30px'}),
            
            # Tab Content
            html.Div(id='tabs-content')
        ])
    ])
])

# 3. Helper for global filtering
def get_filtered_df(models, years):
    dff = df.copy()
    if models and len(models) > 0:
        dff = dff[dff['model'].isin(models)]
    if years:
        dff = dff[(dff['year'] >= years[0]) & (dff['year'] <= years[1])]
    return dff

# 3.1 Callback for KPI Cards
@app.callback(
    Output('kpi-cards-container', 'children'),
    Input('global-model-filter', 'value'),
    Input('global-year-filter', 'value')
)
def update_kpis(selected_models, selected_years):
    dff = get_filtered_df(selected_models, selected_years)
    if dff.empty: return [html.P("No data available", style={'color': 'red'})]
        
    avg_price = dff['price'].mean()
    total_ads = len(dff)
    max_price = dff['price'].max()
    min_price = dff['price'].min()

    return [
        html.Div(className='kpi-card', children=[html.H3(f"{total_ads:,}"), html.P("Listings")]),
        html.Div(className='kpi-card', children=[html.H3(f"£{avg_price:,.0f}"), html.P("Avg Price")]),
        html.Div(className='kpi-card', children=[html.H3(f"£{min_price:,}"), html.P("Min Price")]),
        html.Div(className='kpi-card', children=[html.H3(f"£{max_price:,}"), html.P("Max Price")]),
    ]

# 3.2 Callback for Tab Content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-inline', 'value')
)
def render_tab_content(tab):
    if tab == 'tab-overview':
        return html.Div([
            html.H2('Market Overview: The Big Picture', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P("Global filters on the left panel will update all graphs automatically."),
            html.Div(className='graph-card', style={'marginBottom': '30px'}, children=[
                html.H3('1. 3D Market Surface'),
                dcc.Graph(id='overview-graph-scatter')
            ]),
            html.Div(className='graph-card', children=[
                html.H3('2. Average Price Trend'),
                dcc.Graph(id='overview-graph-year')
            ])
        ])
    elif tab == 'tab-efficiency':
        available_models = sorted(df['model'].unique())
        return html.Div([
            html.H2('Efficiency & Spec Battle', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.Div(className='graph-card', style={'marginBottom': '30px'}, children=[
                html.H3("Normalized Spec Comparison"),
                dcc.Dropdown(id='radar-filter-model', options=[{'label': m, 'value': m} for m in available_models], value=available_models[:3], multi=True),
                dcc.Graph(id='efficiency-graph-radar')
            ]),
            html.Div(className='flex-responsive-row', style={'gap': '20px', 'marginBottom': '20px'}, children=[
                html.Div(className='graph-card', style={'flex': '1'}, children=[html.H3('MPG Distribution'), dcc.Graph(id='eff-box')]),
                html.Div(className='graph-card', style={'flex': '1'}, children=[html.H3('Engine Size Distribution'), dcc.Graph(id='eff-hist')])
            ]),
            html.Div(className='graph-card', children=[
                html.H3('Economy vs. Engine Size'),
                dcc.Graph(id='eff-scatter')
            ])
        ])
    elif tab == 'tab-compare':
        return html.Div([
            html.H2('Series Comparison', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.Div(className='graph-card', style={'marginBottom': '20px'}, children=[
                html.H3('Price Distribution by Model'),
                dcc.Graph(id='compare-graph-price')
            ]),
            html.Div(className='graph-card', children=[
                html.H3('Market Hierarchy (Gearbox -> Fuel -> Model)'),
                dcc.Graph(id='compare-graph-pie')
            ])
        ])
    elif tab == 'tab-prediction':
        return html.Div([
            html.H2('AI Price Predictor', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.Div(className='graph-card', style={'maxWidth': '600px', 'margin': '0 auto'}, children=[
                html.Label("Car Model:"), dcc.Dropdown(id='pred-model', options=[{'label': m, 'value': m} for m in sorted(df['model'].unique())], value=df['model'].iloc[0]),
                html.Br(),
                html.Div(className='flex-responsive-row', style={'gap': '15px'}, children=[
                    html.Div(style={'flex': '1'}, children=[html.Label("Year:"), dcc.Input(id='pred-year', type='number', value=2019, style={'width': '100%'})]),
                    html.Div(style={'flex': '1'}, children=[html.Label("Mileage:"), dcc.Input(id='pred-mileage', type='number', value=30000, style={'width': '100%'})])
                ]),
                html.Br(), html.Button('Calculate fair price', id='pred-button', n_clicks=0, className='predict-btn'),
                html.Hr(), html.Div(id='pred-output', style={'textAlign': 'center'})
            ])
        ])
    elif tab == 'tab-selection':
        return html.Div([
            html.H2('Smart Choice Finder', style={'color': '#638FEF', 'marginBottom': '20px'}),
            html.Div(className='graph-card', children=[
                dash_table.DataTable(
                    id='cars-table', columns=[{"name": i, "id": i} for i in df.columns],
                    row_selectable='single', selected_rows=[], sort_action='native', page_size=10,
                    style_header={'backgroundColor': '#638FEF', 'color': 'white', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_data_conditional=[{'if': {'state': 'selected'}, 'backgroundColor': "#e6f2ff"}]
                )
            ]),
            html.Div(id='car-card-output', style={'marginTop': '20px'})
        ])
    elif tab == 'tab-about':
        return html.Div([
            html.H2('About the Project', style={'color': "#e71010"}),
            html.P("This dashboard helps BMW buyers evaluate second-hand cars using market data and Random Forest regression."),
            html.H3('Credits'), html.P("Developer: Elizaveta Mishchanka | Data: Kaggle BMW Dataset")
        ])

# 4. Graph Update Callbacks (Global filter responsive)
@app.callback(
    Output('overview-graph-scatter', 'figure'),
    [Input('global-model-filter', 'value'), Input('global-year-filter', 'value')]
)
def update_scatter(models, years):
    dff = get_filtered_df(models, years)
    fig = px.scatter_3d(dff.head(1000), x='year', y='mileage', z='price', color='transmission', opacity=0.7)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(bgcolor='white'))
    return fig

@app.callback(
    Output('overview-graph-year', 'figure'),
    [Input('global-model-filter', 'value'), Input('global-year-filter', 'value')]
)
def update_year_trend(models, years):
    dff = get_filtered_df(models, years)
    avg_price = dff.groupby('year')['price'].mean().reset_index()
    fig = px.line(avg_price, x='year', y='price', markers=True, color_discrete_sequence=['#e71010'])
    fig.update_layout(yaxis_tickformat="£,", plot_bgcolor='white')
    return fig

@app.callback(
    Output('efficiency-graph-radar', 'figure'),
    [Input('radar-filter-model', 'value'), Input('global-year-filter', 'value')]
)
def update_radar(models_to_comp, years):
    if not models_to_comp: return px.scatter(title="Select models")
    dff = df[df['year'].between(years[0], years[1])]
    radar_data = []
    for m in models_to_comp:
        m_df = dff[dff['model'] == m]
        if not m_df.empty:
            for metric in ['price', 'mileage', 'mpg', 'tax']:
                val = m_df[metric].mean()
                radar_data.append({'model': m, 'metric': metric, 'value': val / df[metric].max()})
    return px.line_polar(pd.DataFrame(radar_data), r='value', theta='metric', color='model', line_close=True)

@app.callback(
    Output('eff-box', 'figure'),
    [Input('global-model-filter', 'value'), Input('global-year-filter', 'value')]
)
def update_eff_box(models, years):
    dff = get_filtered_df(models, years)
    return px.box(dff, y='mpg', color='transmission')

@app.callback(
    Output('eff-scatter', 'figure'),
    [Input('global-model-filter', 'value'), Input('global-year-filter', 'value')]
)
def update_eff_scatter(models, years):
    dff = get_filtered_df(models, years)
    return px.scatter(dff.head(1000), x='engineSize', y='mpg', color='transmission')

@app.callback(
    Output('compare-graph-price', 'figure'),
    [Input('global-model-filter', 'value'), Input('global-year-filter', 'value')]
)
def update_compare_violin(models, years):
    dff = get_filtered_df(models, years)
    return px.violin(dff, x='model', y='price', color='model', box=True)

@app.callback(
    Output('cars-table', 'data'),
    [Input('global-model-filter', 'value'), Input('global-year-filter', 'value')]
)
def update_table(models, years):
    return get_filtered_df(models, years).head(200).to_dict('records')

@app.callback(
    Output('car-card-output', 'children'),
    [Input('cars-table', 'selected_rows'), State('cars-table', 'data')]
)
def update_car_card(selected_rows, table_data):
    if not selected_rows: return html.Div("Select a car to see photo and specs", className='car-card-placeholder')
    car = table_data[selected_rows[0]]
    img_url = f"/assets/cars/{car['model'].replace(' ', '_')}.jpg"
    return html.Div(className='car-card', children=[
        html.Img(src=img_url, className='car-card-img'),
        html.Div(className='car-card-details', children=[
            html.H3(f"BMW {car['model']}"),
            html.P(f"Year: {car['year']} | Price: £{car['price']:,} | Mileage: {car['mileage']:,}")
        ])
    ])

@app.callback(
    Output('pred-output', 'children'),
    Input('pred-button', 'n_clicks'),
    [State('pred-model', 'value'), State('pred-year', 'value'), State('pred-mileage', 'value')]
)
def predict_price(n_clicks, model_name, year, mileage):
    if n_clicks == 0: return ""
    try:
        model_encoded = le.transform([model_name])[0]
        prediction = model_rf.predict([[model_encoded, year, mileage]])[0]
        return html.H2(f"Fair Price: £{prediction:,.0f}", style={'color': '#e71010'})
    except: return "Error calculating price"

if __name__ == '__main__':
    app.run(debug=True)
