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
# We use Model, Year, Mileage to predict Price
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
                html.H4("Global Filters", style={'color': '#638FEF', 'marginBottom': '10px'}),
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
    
    if dff.empty:
        return [html.P("No data for selected filters", style={'color': 'red'})]
        
    avg_price = dff['price'].mean()
    total_ads = len(dff)
    max_price = dff['price'].max()
    min_price = dff['price'].min()

    return [
        html.Div(className='kpi-card', children=[
            html.H3(f"{total_ads:,}"),
            html.P("Total Listings")
        ]),
        html.Div(className='kpi-card', children=[
            html.H3(f"£{avg_price:,.0f}"),
            html.P("Average Price")
        ]),
        html.Div(className='kpi-card', children=[
            html.H3(f"£{min_price:,}"),
            html.P("Cheapest Car")
        ]),
        html.Div(className='kpi-card', children=[
            html.H3(f"£{max_price:,}"),
            html.P("Most Expensive")
        ]),
    ]

# 3.2 Callback for tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-inline', 'value'),
    Input('global-model-filter', 'value'),
    Input('global-year-filter', 'value')
)
def render_content(tab, g_models, g_years):
    dff_global = get_filtered_df(g_models, g_years)
    
    if tab == 'tab-overview':
        available_trans = sorted(dff_global['transmission'].unique())
        return html.Div([
            html.H2('Market Overview: The Big Picture', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P([
                html.B('Ever wondered if that "low mileage" deal is actually a steal or just average? '),
                "This section gives you a bird's-eye view of the market. Filters on the left affect all data."
            ], style={'lineHeight': '1.6', 'fontSize': '16px', 'color': "#000000", 'marginBottom': '40px'}),
            
            html.Div(className='graph-card', children=[
                html.H3('1. 3D Market Surface', style={'marginBottom': '10px'}),
                html.P("Interact with Year, Mileage, and Price in 3D.", style={'fontSize': '14px', 'color': '#666'}),
                dcc.Graph(
                    figure=px.scatter_3d(
                        dff_global.head(1000), x='year', y='mileage', z='price', color='transmission', opacity=0.7,
                        color_discrete_sequence=['#638FEF', '#e71010', "#000000", '#28a745']
                    ).update_layout(margin=dict(l=0, r=0, b=0, t=0))
                )
            ], style={'marginBottom': '40px'}),
            
            html.Div(className='graph-card', children=[
                html.H3('2. Average Price Trend', style={'marginBottom': '10px'}),
                dcc.Graph(
                    figure=px.line(
                        dff_global.groupby('year')['price'].mean().reset_index(), 
                        x='year', y='price', markers=True,
                        color_discrete_sequence=['#e71010']
                    ).update_layout(yaxis_tickformat="£,")
                )
            ])
        ])
        
    elif tab == 'tab-efficiency':
        available_models = sorted(df['model'].unique())
        return html.Div([
            html.H2('Efficiency: Performance vs. Wallet', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P("Compare models across multiple metrics using the radar chart and distribution plots."),
            
            html.Div(className='graph-card', style={'marginBottom': '30px'}, children=[
                html.H3("Normalized spec battle"),
                html.Label("Select Models to Compare:"),
                dcc.Dropdown(id='radar-filter-model', options=[{'label': m, 'value': m} for m in available_models], value=available_models[:3], multi=True),
                dcc.Graph(id='efficiency-graph-tax')
            ]),

            html.Div(className='flex-responsive-row', style={'gap': '20px'}, children=[
                html.Div(className='graph-card', style={'flex': '1'}, children=[
                    html.H3('Economy vs. Engine Size'),
                    dcc.Graph(id='eff-scatter')
                ]),
                html.Div(className='graph-card', style={'flex': '1'}, children=[
                    html.H3('MPG Distribution'),
                    dcc.Graph(id='eff-box')
                ])
            ])
        ])

    elif tab == 'tab-compare':
        return html.Div([
            html.H2('Compare Series: The Ultimate Face-Off', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.Div(className='graph-card', children=[
                dcc.Graph(id='compare-graph-price')
            ])
        ])

    elif tab == 'tab-prediction':
        return html.Div([
            html.H2('Price Predictor: AI-Powered Appraisal', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P("Our Random Forest model estimates fair market value based on thousands of BMW listings.", style={'marginBottom': '30px'}),
            
            html.Div(className='graph-card', style={'maxWidth': '600px', 'margin': '0 auto'}, children=[
                html.Label("Car Model:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='pred-model', options=[{'label': m, 'value': m} for m in sorted(df['model'].unique())], value=df['model'].iloc[0]),
                html.Br(),
                html.Div(className='flex-responsive-row', style={'gap': '15px'}, children=[
                    html.Div(style={'flex': '1'}, children=[
                        html.Label("Year:", style={'fontWeight': 'bold'}),
                        dcc.Input(id='pred-year', type='number', value=2019, style={'width': '100%', 'padding': '8px', 'borderRadius': '4px', 'border': '1px solid #ddd'}),
                    ]),
                    html.Div(style={'flex': '1'}, children=[
                        html.Label("Mileage:", style={'fontWeight': 'bold'}),
                        dcc.Input(id='pred-mileage', type='number', value=25000, style={'width': '100%', 'padding': '8px', 'borderRadius': '4px', 'border': '1px solid #ddd'}),
                    ]),
                ]),
                html.Br(),
                html.Button('Calculate Fair Price', id='pred-button', n_clicks=0, className='predict-btn'),
                html.Hr(),
                html.Div(id='pred-output', style={'textAlign': 'center', 'marginTop': '20px'})
            ])
        ])

    elif tab == 'tab-selection':
        return html.Div([
            html.H2('Smart Choice: Data-Driven Finder', style={'color': '#638FEF', 'marginBottom': '20px'}),
            html.Div(className='graph-card', children=[
                dash_table.DataTable(
                    id='cars-table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=dff_global.head(100).to_dict('records'),
                    page_size=12,
                    row_selectable='single',
                    selected_rows=[],
                    sort_action='native',
                    style_table={'overflowX': 'auto'},
                    style_header={'backgroundColor': '#638FEF', 'color': 'white', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left', 'padding': '12px'},
                    style_data_conditional=[{'if': {'state': 'selected'}, 'backgroundColor': "#e6f2ff", 'border': '1px solid #638FEF'}]
                ),
            ]),
            html.Div(id='car-card-output', style={'marginTop': '20px'})
        ])
        
    elif tab == 'tab-about':
        return html.Div([
            html.H2('About the Project', style={'color': "#e71010"}),
            html.P("This dashboard helps BMW buyers evaluate second-hand cars using market data and ML."),
            html.H3('Details'),
            html.Ul([
                html.Li("Data: Kaggle BMW Dataset"),
                html.Li("Model: Random Forest Regressor"),
                html.Li("Framework: Plotly Dash")
            ]),
            html.H3('Developer'),
            html.P("Elizaveta Mishchanka, AI Student")
        ])

# 4. Prediction Logic
@app.callback(
    Output('pred-output', 'children'),
    Input('pred-button', 'n_clicks'),
    State('pred-model', 'value'),
    State('pred-year', 'value'),
    State('pred-mileage', 'value')
)
def predict_price(n_clicks, model_name, year, mileage):
    if n_clicks == 0: return ""
    try:
        model_encoded = le.transform([model_name])[0]
        prediction = model_rf.predict([[model_encoded, year, mileage]])[0]
        return html.Div([
            html.H2(f"Fair Price: £{prediction:,.0f}", style={'color': '#e71010'}),
            html.P("Estimated by AI based on market trends.")
        ])
    except Exception as e:
        return html.P(f"Error: {str(e)}", style={'color': 'red'})

if __name__ == '__main__':
    app.run(debug=True)
