import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# 1. Load Data
df = pd.read_csv('bmw.csv')

# Initialize Dash application
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "The Best Cars — BMW"

# 2. Application Layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'height': '100vh', 'backgroundColor': "#d7f1fa", 'display': 'flex', 'flexDirection': 'column', 'margin': '-8px'}, children=[
    
    # Header
    html.Div(style={
        'display': 'flex', 
        'alignItems': 'center', 
        'borderBottom': '5px solid #638FEF', 
        'padding': '15px 25px', 
        'backgroundColor': "#0d0d0d"
    }, children=[
        html.Img(
            src=app.get_asset_url('logo.png'), 
            style={'height': '200px', 'marginRight': '30px'}
        ),
        html.Div(children=[
            html.H1("The Best Cars - BMW", style={'color': "#e71010", 'margin': '0', 'fontSize': '24px', 'fontFamily': 'Arial, sans-serif'}),
            html.P("Second-hand cars descriptor", style={'color': "#638FEF", 'margin': '0', 'fontFamily': 'Arial, sans-serif'})
        ])
    ]),

    # Main content with Sidebar
    html.Div(style={'display': 'flex', 'flex': '1', 'overflow': 'hidden'}, children=[
        
        # Sidebar
        html.Div(style={'width': '250px', 'backgroundColor': '#0d0d0d', 'padding': '20px 0', 'display': 'flex', 'flexDirection': 'column'}, children=[
            dcc.Tabs(id="tabs-inline", value='tab-overview', vertical=True, children=[
                dcc.Tab(label='Market Overview', value='tab-overview', 
                        style={'backgroundColor': '#0d0d0d', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'textAlign': 'left'},
                        selected_style={'backgroundColor': '#638FEF', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'fontWeight': 'bold'}),
                dcc.Tab(label='Efficiency', value='tab-efficiency', 
                        style={'backgroundColor': '#0d0d0d', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'textAlign': 'left'},
                        selected_style={'backgroundColor': '#638FEF', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'fontWeight': 'bold'}),
                dcc.Tab(label='Compare Series', value='tab-compare', 
                        style={'backgroundColor': '#0d0d0d', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'textAlign': 'left'},
                        selected_style={'backgroundColor': '#638FEF', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'fontWeight': 'bold'}),
                dcc.Tab(label='Smart Choice', value='tab-selection', 
                        style={'backgroundColor': '#0d0d0d', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'textAlign': 'left'},
                        selected_style={'backgroundColor': '#638FEF', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'fontWeight': 'bold'}),
                dcc.Tab(label='About/Help', value='tab-about', 
                        style={'backgroundColor': '#0d0d0d', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'textAlign': 'left'},
                        selected_style={'backgroundColor': '#638FEF', 'color': 'white', 'border': 'none', 'padding': '15px 20px', 'fontWeight': 'bold'}),
            ], colors={"border": "transparent", "primary": "transparent", "background": "transparent"}),
        ]),
        
        # Content Area
        html.Div(id='tabs-content', style={'flex': '1', 'padding': '30px', 'backgroundColor': 'white', 'overflowY': 'auto'})
    ])
])

# 3. Server Logic: Tab switching and Graph rendering
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-inline', 'value')
)
def render_content(tab):
    if tab == 'tab-overview':
        available_trans = sorted(df['transmission'].unique()) if 'transmission' in df.columns else []
        return html.Div([
            html.H2('Market Overview: The Big Picture', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P([
                html.B('Ever wondered if that "low mileage" deal is actually a steal or just average? '),
                "This section gives you a bird's-eye view of the BMW second-hand market. Use the charts below to understand general trends and price dynamics."
            ], style={'lineHeight': '1.6', 'fontSize': '16px', 'color': '#2c3e50', 'marginBottom': '40px'}),
            
            # Graph 1: 3D Market Surface
            html.Div(style={'marginBottom': '60px'}, children=[
                html.H3('1. The 3D Market Surface', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("This 3D scatter plot visualizes the interaction between three critical factors: Production Year, Mileage, and Price. By spinning this graph, you can see how cars drop in value as they get older and drive more miles. It's the ultimate 'Value Map' to see where the best deals typically hide.", style={'marginBottom': '15px'}),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Filter 3D Scatter by Transmission:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='overview-trans-filter-scatter', options=[{'label': t, 'value': t} for t in available_trans], multi=True, placeholder="All Transmissions")
                ]),
                dcc.Graph(id='overview-graph-scatter')
            ]),
            
            # Graph 2: Price Trend
            html.Div(style={'marginBottom': '30px'}, children=[
                html.H3('2. Average Price Trend', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("This line chart simplifies the chaos. It shows the average market price for each production year. It helps you quickly spot 'sweet spots' in the market where a one-year difference in age results in a significant price drop (or jump).", style={'marginBottom': '15px'}),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Filter Year Line by Transmission:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='overview-trans-filter-year', options=[{'label': t, 'value': t} for t in available_trans], multi=True, placeholder="All Transmissions")
                ]),
                dcc.Graph(id='overview-graph-year')
            ])
        ])
    elif tab == 'tab-efficiency':
        available_fuel = sorted(df['fuelType'].unique()) if 'fuelType' in df.columns else []
        available_models = sorted(df['model'].unique()) if 'model' in df.columns else []
        available_trans = sorted(df['transmission'].unique()) if 'transmission' in df.columns else []
        return html.Div([
            html.H2('Efficiency: Performance vs. Wallet', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P([
                html.B('BMW is about performance, but your bank account cares about the MPG. '),
                "In this tab, we break down the running costs and technical efficiency of different models."
            ], style={'lineHeight': '1.6', 'fontSize': '16px', 'color': '#2c3e50', 'marginBottom': '30px'}),
            
            # Graph 1: Economy vs Engine Size
            html.Div(style={'marginBottom': '60px'}, children=[
                html.H3('1. Economy vs. Engine Size', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("Does a bigger engine always mean more gas? This scatter plot shows the trade-off between engine displacement and fuel efficiency (MPG). Higher points mean better efficiency, while points further to the right show more powerful engines. It helps you find models that punch above their weight in efficiency."),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Filter Scatter by Fuel Type:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='eff-filter-scatter', options=[{'label': f, 'value': f} for f in available_fuel], multi=True, placeholder="Fuel Types")
                ]),
                dcc.Graph(id='eff-scatter')
            ]),

            # Graph 2: Engine Size Distribution
            html.Div(style={'marginBottom': '60px'}, children=[
                html.H3('2. Engine Size Distribution', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("This histogram shows which engine sizes are most common in the second-hand market. It gives you an idea of what 'standard' performance looks like for BMW and helps you see if you're looking at a common mid-range model or a rare high-capacity beast."),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Filter Histogram by Fuel Type:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='eff-filter-hist', options=[{'label': f, 'value': f} for f in available_fuel], multi=True, placeholder="Fuel Types")
                ]),
                dcc.Graph(id='eff-hist')
            ]),

            # Graph 3: MPG Variability
            html.Div(style={'marginBottom': '60px'}, children=[
                html.H3('3. MPG Variability by Gearbox', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("This boxplot shows the range of fuel economy for different transmissions. The 'box' shows where most cars fall, while the lines (whiskers) show the outliers. It’s a great way to see if a specific gearbox type (like Manual vs Semi-Auto) consistently delivers better mileage."),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Filter Boxplot by Fuel Type:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='eff-filter-box', options=[{'label': f, 'value': f} for f in available_fuel], multi=True, placeholder="Fuel Types")
                ]),
                dcc.Graph(id='eff-box')
            ]),

            # Graph 4: Normalized Efficiency Profile
            html.Div(style={'marginBottom': '30px'}, children=[
                html.H3('4. The Normalized Efficiency Profile', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("This radar chart is the ultimate 'spec battle' tool. It compares selected models across four normalized metrics: Price, Mileage, Road Tax, and MPG. A larger covered area typically means a more well-rounded vehicle. It’s the best way to see which model gives you the most balanced profile for your money."),
                html.Div(style={'display': 'flex', 'gap': '10px', 'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Div(style={'flex': '1'}, children=[
                        html.Label("Filter by Transmission:", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='radar-filter-trans', options=[{'label': t, 'value': t} for t in available_trans], multi=True, placeholder="All")
                    ]),
                    html.Div(style={'flex': '1'}, children=[
                        html.Label("Select Models to Compare:", style={'fontWeight': 'bold'}),
                        dcc.Dropdown(id='radar-filter-model', options=[{'label': m, 'value': m} for m in available_models], value=available_models[:3], multi=True, placeholder="Models")
                    ])
                ]),
                dcc.Graph(id='efficiency-graph-tax')
            ])
        ])

    elif tab == 'tab-compare':
        available_models = sorted(df['model'].unique()) if 'model' in df.columns else []
        return html.Div([
            html.H2('Compare Series: The Ultimate Face-Off', style={'color': '#638FEF', 'marginBottom': '10px'}),
            html.P([
                html.B("Can't decide between a 3 Series and a 5 Series? Let's settle the debate. "),
                "This tab allows you to compare different series side-by-side using advanced visual metrics."
            ], style={'lineHeight': '1.6', 'fontSize': '16px', 'color': '#2c3e50', 'marginBottom': '30px'}),
            
            # Comparison 1: Price Density
            html.Div(style={'marginBottom': '60px'}, children=[
                html.H3('1. Price Density (Violin Plot)', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("While a standard chart shows averages, this violin plot shows the 'density' of prices. The wider the shape, the more cars are available at that price point. It helps you see if a model has a stable market value or if prices are highly unpredictable."),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Select Models to Compare Price Density:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='compare-models-filter-price', options=[{'label': m, 'value': m} for m in available_models], value=available_models[:5], multi=True, placeholder="Select Models")
                ]),
                dcc.Graph(id='compare-graph-price')
            ]),
            
            # Comparison 2: Market Hierarchy
            html.Div(style={'marginBottom': '30px'}, children=[
                html.H3('2. Market Hierarchy (Sunburst)', style={'color': '#0d0d0d', 'marginBottom': '10px'}),
                html.P("This interactive chart shows how models are distributed across transmissions and fuel types. Click on the segments to 'zoom in'. It’s an easy way to discover if a model you like is mostly available in a specific configuration (like Diesel-Automatic)."),
                html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}, children=[
                    html.Label("Select Models for Hierarchy Breakdown:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(id='compare-models-filter-pie', options=[{'label': m, 'value': m} for m in available_models], value=available_models[:5], multi=True, placeholder="Select Models")
                ]),
                dcc.Graph(id='compare-graph-pie')
            ])
        ])
        
    elif tab == 'tab-selection':
        # Collect unique data for filter dropdowns
        available_models = sorted(df['model'].unique()) if 'model' in df.columns else []
        available_trans = sorted(df['transmission'].unique()) if 'transmission' in df.columns else []
        available_fuel = sorted(df['fuelType'].unique()) if 'fuelType' in df.columns else []
        
        min_price = int(df['price'].min()) if 'price' in df.columns else 0
        max_price = int(df['price'].max()) if 'price' in df.columns else 100000

        # Selection Tab Layout
        return html.Div(children=[
            
            # Header and Description Section (Flex)
            html.Div(style={'display': 'flex', 'gap': '40px', 'alignItems': 'flex-start', 'marginBottom': '30px'}, children=[
                
                # Left: Image
                html.Img(
                    src=app.get_asset_url('smart.jpg'), 
                    style={
                        'width': '400px', 
                        'borderRadius': '15px', 
                        'boxShadow': '0 8px 20px rgba(0,0,0,0.15)',
                        'border': '3px solid #638FEF'
                    }
                ),

                # Right: Title and Description
                html.Div(style={'flex': '1', 'lineHeight': '1.6', 'fontSize': '16px', 'color': '#2c3e50'}, children=[
                    html.H2('Smart Choice: Your Data-Driven BMW Finder', style={'color': '#638FEF', 'marginBottom': '15px', 'marginTop': '0'}),
                    html.P([
                        html.B("Let’s be real — buying a used BMW is a bit of a gamble. "),
                        "Choosing a used BMW requires balancing many factors, including price, condition, mileage, and equipment. This tool is designed to simplify that process by helping you evaluate available vehicles using market data and objective criteria. Instead of reviewing numerous listings manually, you can filter, compare, and analyze vehicles to identify options that best match your requirements and budget."
                    ]),
                    
                    html.H4('How to find your perfect match:', style={'marginTop': '25px', 'color': '#0d0d0d', 'marginBottom': '10px'}),
                    html.Ul([
                        html.Li([html.B("Define Your Criteria: "), "Use the filters in the sidebar to refine the selection. You can choose specific BMW models, transmission types, fuel options, and other vehicle characteristics."]),
                        html.Li([html.B("Analyze Price Distribution: "), "The chart on the left provides an overview of the price distribution for the currently selected vehicles. This allows you to better understand market pricing and identify offers that may differ significantly from the average."]),
                        html.Li([html.B("Compare Available Vehicles: "), "The table displays all vehicles that meet your selected criteria. Columns can be sorted to quickly compare key parameters such as price, mileage, model year, power output, and other specifications."]),
                        html.Li([html.B("Review Vehicle Details: "), "To examine a vehicle in greater detail, select it using the checkbox in the table. A detailed profile card will be displayed, including a photograph and comprehensive technical information."]),
                        html.Li([html.B("Make an Informed Decision: "), "By combining filtering, market analysis, and detailed vehicle data, the tool helps you evaluate available options more efficiently and identify vehicles that best meet your needs."]),
                    ]),
                ])
            ]),

            # 2. Filters and Table in one row (Flex)
            html.Div(style={'display': 'flex', 'gap': '30px'}, children=[
                
                # Filters Sidebar
                html.Div(style={
                    'width': '280px', 'backgroundColor': '#f8f9fa', 'padding': '20px', 
                    'borderRadius': '8px', 'border': '1px solid #dee2e6', 'height': 'fit-content'
                }, children=[
                    html.H3("Search Filters", style={'color': "#000000", 'marginTop': '0', 'fontSize': '18px'}),
                    
                    html.Label("Model:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
                    dcc.Dropdown(id='filter-model', options=[{'label': m, 'value': m} for m in available_models], multi=True, placeholder="All Models"),
                    html.Br(),
                    
                    html.Label("Transmission:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
                    dcc.Dropdown(id='filter-trans', options=[{'label': t, 'value': t} for t in available_trans], multi=True, placeholder="All Transmissions"),
                    html.Br(),
                    
                    html.Label("Fuel Type:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
                    dcc.Dropdown(id='filter-fuel', options=[{'label': f, 'value': f} for f in available_fuel], multi=True, placeholder="All Fuel Types"),
                    html.Br(),
                    
                    html.Label("Max Price:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
                    dcc.Slider(id='filter-price', min=min_price, max=max_price, value=max_price, 
                               marks={min_price: f'£{min_price:,}', max_price: f'£{max_price:,}'}, step=1000),
                    html.Br(),
                    
                    # Mini price distribution graph
                    html.Hr(),
                    html.H4("Price Distribution", style={'fontSize': '16px', 'textAlign': 'center', 'margin': '10px 0'}),
                    dcc.Graph(id='price-dist-graph', config={'displayModeBar': False}, style={'height': '200px'})
                ]),
                
                # Table and Detail Card
                html.Div(style={'flex': '1'}, children=[
                    # DataTable with sorting
                    dash_table.DataTable(
                        id='cars-table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        page_size=10,
                        row_selectable='single', 
                        selected_rows=[],
                        sort_action='native',
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '8px'},
                        style_header={'backgroundColor': '#638FEF', 'color': 'white', 'fontWeight': 'bold'},
                        style_data_conditional=[{
                            'if': {'state': 'selected'}, 'backgroundColor': '#e6f2ff', 'border': '1px solid #638FEF'
                        }]
                    ),
                    
                    html.Br(),
                    
                    # Dynamic Car Card Container
                    html.Div(id='car-card-output')
                ])
            ])
        ])
        
    elif tab == 'tab-about':
        return html.Div([
            html.H2('Dashboard description', style={'color': "#e71010"}),
            html.P([
                "This dashboard was created by poor tired student which likes BMW from childhood, "
                "so it will be useful for people who want to choose second-hand BMW but don't know "
                "what exactly model will be better to choose. Data was scraped from ",
                html.A("Kaggle", href="https://www.kaggle.com/datasets/itszubi/bmw-car-sales-dataset", target="_blank"),
                "."
            ]),
            html.H3('Categories for description'),
            html.Ul([
                html.Li([html.B('model'), ' — full name of the car model']),
                html.Li([html.B('year'), ' — year of manufacture']),
                html.Li([html.B('price'), ' — price for the car in GBP']),
                html.Li([html.B('transmission'), ' — type of gearbox']),
                html.Li([html.B('mileage'), ' — total distance in miles driven by the car']),
                html.Li([html.B('fuelType'), ' — type of fuel used']),
                html.Li([html.B('tax'), ' — road tax associated with the vehicle']),
                html.Li([html.B('mpg'), ' — fuel efficiency measured in miles per gallon']),
                html.Li([html.B('engineSize'), ' — engine capacity in litres'])
            ]),
            html.H3('Use the navigation tabs to explore different aspects of the dataset'),
            html.Ul([
                html.Li([html.B('Market Overview: '), 'Analyze high-level price trends, mileage dependencies, and depreciation curves']),
                html.Li([html.B('Efficiency: '), 'Examine fuel economy versus annual road tax to optimize the total cost of ownership']),
                html.Li([html.B('Compare Series: '), 'Compare average market metrics across different BMW models and series']),
                html.Li([html.B('Smart Choice: '), 'Utilize the interactive datatable and dynamic profiles to find and evaluate specific vehicles']),
            ]),
            html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                html.H2('Help', style={'color': "#e71010", 'margin': '0'}),
                html.Img(src=app.get_asset_url('help.avif'), style={'height': '50px', 'marginRight': '10px'}),
            ]),
            html.P('Nobody and nothing will help you', style={'fontSize': '9px', 'color': "#e71010"}),
            html.P('You may contact me by:'),
            html.Ul([
                html.Li([html.B('elizaveta.mishchanka@student.put.poznan.pl'), ' — my mail']),
                html.Li([html.B(html.A("vaynly", href="https://www.instagram.com/vaynly?igsh=MTNiYTVwcWsyd3Nraw%3D%3D&utm_source=qr", target="_blank"),
                ), ' — my instagram']),
            ]),
            html.H4('Produced by Elizaveta Mishchanka, student of artificial intelligence'),
            html.Img(src=app.get_asset_url('logotyp.png'), style={'height': '50px', 'marginRight': '10px'}),
        ])

# 4.1 SERVER LOGIC: Dynamic table filtering and graph updates
@app.callback(
    Output('cars-table', 'data'),
    Output('price-dist-graph', 'figure'),
    Input('filter-model', 'value'),
    Input('filter-trans', 'value'),
    Input('filter-fuel', 'value'),
    Input('filter-price', 'value'),
    Input('tabs-inline', 'value')
)
def filter_data(selected_models, selected_trans, selected_fuel, max_price, active_tab):
    if active_tab != 'tab-selection':
        return [], {}
        
    dff = df.copy()
    
    if selected_models:
        dff = dff[dff['model'].isin(selected_models)]
    if selected_trans:
        dff = dff[dff['transmission'].isin(selected_trans)]
    if selected_fuel:
        dff = dff[dff['fuelType'].isin(selected_fuel)]
    if max_price:
        dff = dff[dff['price'] <= max_price]
        
    # Create price distribution histogram
    fig = px.histogram(
        dff, 
        x="price", 
        nbins=20, 
        title=None,
        color_discrete_sequence=['#638FEF']
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=200,
        xaxis_title="Price",
        yaxis_title="Amount of cars",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return dff.head(1000).to_dict('records'), fig

# 4.2 SERVER LOGIC: Car Card output (Select interaction)
@app.callback(
    Output('car-card-output', 'children'),
    Input('cars-table', 'selected_rows'),
    Input('cars-table', 'data')
)
def update_card(selected_rows, table_data):
    if not selected_rows or not table_data:
        return html.Div(style={
            'padding': '20px', 'border': '2px dashed #010101', 'borderRadius': '5px', 'backgroundColor': "#ffffff", 'marginTop': '15px'
        }, children=[
            html.H4("Please choose exact car for additional information", style={'color': "#010101", 'margin': '0'})
        ])
    
    try:
        selected_index = selected_rows[0]
        car_data = table_data[selected_index]
        model_name = car_data.get('model', '').strip()
        
        # Load real photo of the specific model from assets/cars/
        model_name_formatted = model_name.replace(' ', '_')
        img_url = f'/assets/cars/{model_name_formatted}.jpg'
        
        return html.Div(style={
            'padding': '20px', 'border': '2px dashed #638FEF', 'borderRadius': '5px', 'backgroundColor': '#e6f2ff', 'marginTop': '15px', 'display': 'flex', 'gap': '20px', 'alignItems': 'center'
        }, children=[
            html.Img(src=img_url, style={'width': '250px', 'height': '180px', 'borderRadius': '8px', 'objectFit': 'cover', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'}),
            html.Div(style={'flex': '1'}, children=[
                html.H3(f"Chosen car: BMW {model_name}", style={'color': '#638FEF', 'margin': '0 0 10px 0'}),
                html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}, children=[
                    html.P([html.B("Year of manufacture: "), car_data.get('year', 'N/A')]),
                    html.P([html.B("Price: "), f"£{int(car_data.get('price', 0)):,}"]),
                    html.P([html.B("Mileage: "), f"{int(car_data.get('mileage', 0)):,} miles"]),
                    html.P([html.B("Type of transmission: "), car_data.get('transmission', 'N/A')]),
                    html.P([html.B("Type of fuel: "), car_data.get('fuelType', 'N/A')]),
                    html.P([html.B("Engine displacement: "), f"{car_data.get('engineSize', 'N/A')} L"]),
                    html.P([html.B("Fuel consumption: "), f"{car_data.get('mpg', 'N/A')} MPG"]),
                    html.P([html.B("Road tax: "), f"£{car_data.get('tax', 'N/A')}"])
                ])
            ])
        ])
    except Exception as e:
        return html.H4(f"Error: {str(e)}", style={'color': 'red'})

# ==============================================================================
# DYNAMIC UPDATES FOR COMPLEX GRAPHS (Tabs 1-3)
# ==============================================================================

# 4.3 Market Overview Tab Graphs
@app.callback(
    Output('overview-graph-scatter', 'figure'),
    Input('overview-trans-filter-scatter', 'value')
)
def update_overview_scatter(selected_trans):
    dff = df.copy()
    if selected_trans and len(selected_trans) > 0:
        dff = dff[dff['transmission'].isin(selected_trans)]
        
    fig_scatter = px.scatter_3d(
        dff.head(1000), x='year', y='mileage', z='price', color='transmission', opacity=0.7,
        title='3D Market Surface: Price, Mileage & Year',
        color_discrete_sequence=['#638FEF', '#e71010', '#0d0d0d', '#28a745']
    )
    fig_scatter.update_layout(plot_bgcolor='#f8f9fa', paper_bgcolor='white', margin=dict(t=40, b=20, l=20, r=20), scene=dict(bgcolor='#f8f9fa'))
    return fig_scatter

@app.callback(
    Output('overview-graph-year', 'figure'),
    Input('overview-trans-filter-year', 'value')
)
def update_overview_year(selected_trans):
    dff = df.copy()
    if selected_trans and len(selected_trans) > 0:
        dff = dff[dff['transmission'].isin(selected_trans)]
        
    avg_price_year = dff.groupby('year')['price'].mean().reset_index().sort_values('year')
    
    fig_line = px.line(
        avg_price_year, x='year', y='price', markers=True,
        title='Average Price Trend by Production Year',
        color_discrete_sequence=['#e71010']
    )
    fig_line.update_layout(
        plot_bgcolor='#f8f9fa', 
        paper_bgcolor='white', 
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis_title="Production Year",
        yaxis_title="Average Price (£)",
        yaxis_tickformat="£,"
    )
    return fig_line

# 4.4 Efficiency Tab Graphs
@app.callback(
    Output('eff-scatter', 'figure'),
    Input('eff-filter-scatter', 'value')
)
def update_eff_scatter(selected_fuel):
    dff = df.copy()
    if selected_fuel and len(selected_fuel) > 0:
        dff = dff[dff['fuelType'].isin(selected_fuel)]
    if not dff.empty:
        fig = px.scatter(
            dff.head(1500), x='engineSize', y='mpg', color='transmission', opacity=0.7,
            title='Economy vs Engine Size', hover_name='model',
            color_discrete_sequence=['#638FEF', '#e71010', '#0d0d0d', '#28a745']
        )
        fig.update_layout(plot_bgcolor='#f8f9fa', paper_bgcolor='white', margin=dict(t=40, b=20, l=10, r=10))
        return fig
    return px.scatter(title="Not enough data")

@app.callback(
    Output('eff-hist', 'figure'),
    Input('eff-filter-hist', 'value')
)
def update_eff_hist(selected_fuel):
    dff = df.copy()
    if selected_fuel and len(selected_fuel) > 0:
        dff = dff[dff['fuelType'].isin(selected_fuel)]
    if not dff.empty:
        fig = px.histogram(
            dff, x='engineSize', color='transmission', title='Engine Size Dist', nbins=20,
            color_discrete_sequence=['#638FEF', '#e71010', '#0d0d0d', '#28a745']
        )
        fig.update_layout(plot_bgcolor='#f8f9fa', paper_bgcolor='white', margin=dict(t=40, b=20, l=10, r=10))
        return fig
    return px.scatter(title="Not enough data")

@app.callback(
    Output('eff-box', 'figure'),
    Input('eff-filter-box', 'value')
)
def update_eff_box(selected_fuel):
    dff = df.copy()
    if selected_fuel and len(selected_fuel) > 0:
        dff = dff[dff['fuelType'].isin(selected_fuel)]
    if not dff.empty:
        fig = px.box(
            dff, y='mpg', color='transmission', title='MPG Boxplot',
            color_discrete_sequence=['#638FEF', '#e71010', '#0d0d0d', '#28a745']
        )
        fig.update_layout(plot_bgcolor='#f8f9fa', paper_bgcolor='white', margin=dict(t=40, b=20, l=10, r=10))
        return fig
    return px.scatter(title="Not enough data")

@app.callback(
    Output('efficiency-graph-tax', 'figure'),
    Input('radar-filter-trans', 'value'),
    Input('radar-filter-model', 'value')
)
def update_efficiency_tax(selected_trans, selected_models):
    dff = df.copy()
    if selected_trans and len(selected_trans) > 0:
        dff = dff[dff['transmission'].isin(selected_trans)]
        
    if not selected_models:
        selected_models = sorted(dff['model'].unique())[:3] if 'model' in dff.columns else []
        
    dff = dff[dff['model'].isin(selected_models)]
        
    if not dff.empty and len(selected_models) > 0:
        radar_data = []
        metrics = ['price', 'mileage', 'tax', 'mpg']
        
        for m in selected_models:
            model_data = dff[dff['model'] == m]
            if not model_data.empty:
                for metric in metrics:
                    if metric in model_data.columns:
                        val = model_data[metric].mean()
                        max_val = df[metric].max() if df[metric].max() > 0 else 1
                        radar_data.append({'model': m, 'metric': metric, 'value': val/max_val})
                
        radar_df = pd.DataFrame(radar_data)
        if not radar_df.empty:
            fig_radar = px.line_polar(radar_df, r='value', theta='metric', color='model', line_close=True,
                                      title='Models Normalized Efficiency Profile',
                                      color_discrete_sequence=px.colors.qualitative.Safe)
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), plot_bgcolor='#f8f9fa', paper_bgcolor='white', margin=dict(t=60, b=20, l=20, r=20))
            return fig_radar
            
    return px.scatter(title="Not enough data")

# 4.5 Compare Series Tab Graphs
@app.callback(
    Output('compare-graph-price', 'figure'),
    Input('compare-models-filter-price', 'value')
)
def update_compare_price(selected_models):
    if not selected_models:
        selected_models = sorted(df['model'].unique())[:5] if 'model' in df.columns else []
        
    dff = df[df['model'].isin(selected_models)]
    
    if not dff.empty:
        fig_violin = px.violin(
            dff, x='model', y='price', color='model', box=True, points="all",
            title='Price Distribution with Density (Violin Plot)',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_violin.update_layout(plot_bgcolor='#f8f9fa', paper_bgcolor='white', showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
        return fig_violin
    return px.scatter(title="Not enough data")

@app.callback(
    Output('compare-graph-pie', 'figure'),
    Input('compare-models-filter-pie', 'value')
)
def update_compare_pie(selected_models):
    if not selected_models:
        selected_models = sorted(df['model'].unique())[:5] if 'model' in df.columns else []
        
    dff = df[df['model'].isin(selected_models)]
    
    if not dff.empty:
        fig_sunburst = px.sunburst(
            dff, path=['transmission', 'fuelType', 'model'],
            title='Market Hierarchy: Gearbox -> Fuel -> Model',
            color_discrete_sequence=['#638FEF', '#0d0d0d', '#e71010', '#28a745']
        )
        fig_sunburst.update_traces(hovertemplate='<b>%{label}</b><br>Amount of cars: %{value}<extra></extra>')
        fig_sunburst.update_layout(margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor='white')
        return fig_sunburst
    return px.scatter(title="Not enough data")

if __name__ == '__main__':
    app.run(
        debug=True,
        dev_tools_ui=False,      
        dev_tools_props_check=False  
    )