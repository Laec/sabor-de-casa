from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

app = Dash(__name__)

# Datos ficticios
df = pd.read_csv("Publicaciones_topicos.csv")

pages = ['LA LUCHA SANGUCHERIA CRIOLLA', 'DesayunosFit Peru',
       'PATRIO SANGUCHERIA CRIOLLA', 'El Chinito Sanguchería',
       'Deli Desayunos Delivery - Cusco', 'Desayuno Delivery',
       'El Jardín De Jazmín', 'Paradero V', 'El Chino Vegano',
       'Seitan Urban Bistro', 'Asianica Street Food',
       'Carnívoro La Hamburguesería', 'Lima 141 Sangucheria',
       'Sandwich Palermo Café', 'Sándwiches Monstruos',
       'Maztika Sanguches Urbanos','']

reactions= ['likes', 'comments', 'shares', 'likes_standar','comments_standar', 'shares_standar']

app.layout = html.Div(style={'background-color': '#FFFFFF', 'padding': '2% 8% 0 8%',}, children=[
    html.Div(style={'display': 'inline-block', 'width': '33%', 'text-align': 'center'}, children=[
        html.H1(style={'color': '#190E08','font-size':'35px','margin':'0'}, children='Web Scraping'),
        html.Div(style={'display': 'inline-block','width': '80%', 'text-align': 'center'},id='output'),
    ]),
    html.Div(style={'display': 'inline-block', 'width': '32%', 'text-align': 'center'}, children=[
        dcc.Dropdown(
            id='page-dropdown',
            options=[{'label': page, 'value': page} for page in pages],
            value=''
        ),
    ]),
    html.Div(style={'display': 'inline-block', 'width': '2%'}),
    html.Div(style={'display': 'inline-block', 'width': '32%', 'text-align': 'center'}, children=[
        dcc.Dropdown(
            id='reaction-dropdown',
            options=[{'label': reaction, 'value': reaction} for reaction in reactions],
            value='likes_standar'
        ),
    ]),

    
    html.Div(style={'display': 'inline-block', 'width': '2%'}),
    html.Div(style={'margin': '20px'}, children=[
        dcc.Graph(id='scatter-plot')
    ]),
    html.Div(style={'display': 'inline-block', 'width': '2%'}),
    html.Div(style={'margin': '20px'}, children=[
        dcc.Graph(id='bar-plot')
    ]),
])

# Función de devolución para actualizar el gráfico de dispersión
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('page-dropdown', 'value'),
     Input('reaction-dropdown', 'value')]
)
def update_scatter_plot(selected_page, selected_reaction):
    #filtered_df = df[(df['Página'] == selected_page) & (df['Reacción'] == selected_reaction)]
    if bool(selected_page):
        likes_horas_mean = df[df.username == selected_page].groupby('hora').mean()[selected_reaction]
    else:
        likes_horas_mean = df.groupby('hora').mean()[selected_reaction]
      
    x_data = likes_horas_mean.index
    y_data = likes_horas_mean.values

    val_maximo = y_data.max()
    index_maximo = x_data[y_data.argmax()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines',
        name='Horas',
        line=dict(color='crimson', width=2),
        connectgaps=True,
    ))

    # Puntos iniciales y finales
    fig.add_trace(go.Scatter(
        x=[x_data[0], index_maximo, x_data[-1]],
        y=[y_data[0], val_maximo, y_data[-1]],
        mode='markers',
        marker=dict(color='rgb(115,115,115)', size=8)
    ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=100,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Añadir etiquetas


    # Etiqueta izquierda
    annotations.append(dict(xref='paper', x=0.05, y=y_data[0],
                                    xanchor='right', yanchor='middle',
                                    text=selected_reaction + ' - {:.3f}'.format(y_data[0]),
                                    font=dict(family='Arial',
                                            size=13),
                                    showarrow=False))
    # Etiqueta derecha
    annotations.append(dict(xref='paper', x=0.95, y=y_data[-1],
                                    xanchor='left', yanchor='middle',
                                    text='{:.3f}'.format(y_data[-1]),
                                    font=dict(family='Arial',
                                            size=13),
                                    showarrow=False))
    # Etiqueta maximo
    annotations.append(dict(xref='x', x=index_maximo + 0.2, y=val_maximo,
                                    xanchor='left', yanchor='middle',
                                    text='{:.3f}'.format(val_maximo),
                                    font=dict(family='Arial',
                                            size=13),
                                    showarrow=False))
    # Titulo
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.05,
                                xanchor='center', yanchor='bottom',
                                text='Promedio de <b>' + selected_reaction + '</b> según<br><b>hora de publicación</b>',
                                font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig
# Función de devolución para actualizar el gráfico de barras
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('page-dropdown', 'value'),
     Input('reaction-dropdown', 'value')]
)
def update_bar_plot(selected_page, selected_reaction):
    #filtered_df = df[(df['Página'] == selected_page) & (df['Reacción'] == selected_reaction)]
    if bool(selected_page):
        likes_dias_mean = df[df.username == selected_page].groupby('dia').mean()[selected_reaction]
    else:
        likes_dias_mean = df.groupby('dia').mean()[selected_reaction]
        
    x_data = likes_dias_mean.index
    y_data = likes_dias_mean.values

    val_maximo = y_data.max()
    index_maximo = y_data.argmax()

    colores = ['rgb(115,115,115)']*len(x_data)
    colores[index_maximo] = 'crimson'
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        marker_color=colores
    ))

    fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
        ),
        yaxis=dict(
            showgrid=True,
            showline=False,
            gridcolor='rgb(204, 204, 204)'
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=200,
            r=200,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Titulo
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.05,
                                xanchor='center', yanchor='bottom',
                                text='Promedio de <b>' + selected_reaction + '</b> por <b>Día</b>',
                                font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                showarrow=False))
        
    fig.update_layout(barmode='group', xaxis_tickangle=-45,annotations=annotations,)
    return fig

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='page-dropdown', component_property='value')]
)
def update_output(selected_page):
    if bool(selected_page):
        textos = df[df.username == selected_page].text
        palabras = [len(texto.split()) for texto in textos if pd.isna(texto) == False]
        mean_palabras = sum(palabras)/len(palabras)
        return '{} tiene en promedio {:.2f} palabras por publicación'.format(selected_page, mean_palabras)
    else:
        textos = df.text
        palabras = [len(texto.split()) for texto in textos if pd.isna(texto) == False]
        mean_palabras = sum(palabras)/len(palabras)
        return 'El promedio de palabras por publicación es {:.2f}'.format( mean_palabras)

    

if __name__ == '__main__':
    app.run_server(debug=True)