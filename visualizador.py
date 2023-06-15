import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


pc_doc = pd.read_excel('consolidado_primer_curso_doctorado_2014_2021.xlsx')
info_docs = pd.read_excel('promedio_doctorados_dili.xlsx')
grad_df = pd.read_excel('graduados_doctorado_info.xlsx')
info_docs['puntaje_fig'] = info_docs['puntaje']+5
info_docs['total_pc'] = info_docs['programas']*info_docs['primer_curso_final']

fig1 = px.histogram(pc_doc, x = 'año_final', 
                   y = 'primer_curso_final', 
                   color = 'sector_final', 
                   barmode = 'group', 
                   title = 'Primer curso doctorados en Colombia',
                   labels={
                     "año_final": "Año",
                     "primer_curso_final": "matriculados primer curso",
                     "sector_final": "sector"
                   })
fig1.update_layout( yaxis_title="matriculados primer curso" )

mask = pc_doc['area_conocimiento_final']=='ingeniería, arquitectura, urbanismo y afines'

fig2 = px.histogram(pc_doc[mask], x = 'año_final', 
                   y = 'primer_curso_final', 
                   color = 'sector_final', 
                   barmode = 'group', 
                   title = 'Primer curso doctorados en Colombia - Ingeniería y afines',
                   labels={
                     "año_final": "Año",
                     "primer_curso_final": "matriculados primer curso",
                     "sector_final": "sector"
                   })
fig2.update_layout( yaxis_title="matriculados primer curso" )

fig3 = px.line(pc_doc.groupby(['area_conocimiento_final', 'año_final'])['primer_curso_final'].sum().reset_index(), 
               x = 'año_final', 
               y = 'primer_curso_final', 
               color = 'area_conocimiento_final',
               labels = {
                   "año_final": "Año",
                   "primer_curso_final": 'matriculados primer curso',
                   'area_conocimiento_final': 'Área de Conocimiento'
               },
               title = 'Primer curso doctorados por área de conocimiento'
              )

fig4 = px.histogram(pc_doc[mask].groupby(['sector_final', 'año_final'])['codigo_snies_final'].nunique().reset_index(),
                   x = 'año_final', 
                   y = 'codigo_snies_final', 
                   color = 'sector_final', 
                   barmode = 'group', 
                   title = 'Programas doctorales en ingeniería y afines',
                   labels={
                     "año_final": "Año",
                     "sector_final": "sector"
                   },
                   nbins=8)
fig4.update_layout( yaxis_title="número de programas doctorales" )


fig5 = px.histogram((pc_doc[mask].groupby(['sector_final', 'año_final'])['primer_curso_final'].sum()/pc_doc[mask].groupby(['sector_final', 'año_final'])['codigo_snies_final'].nunique()).reset_index().rename(columns = {0 : 'primer_curso'}),
                    x = 'año_final', 
                    y = 'primer_curso', 
                    color = 'sector_final', 
                    barmode = 'group', 
                    title = 'matriculados primer curso por programa - Ingeniería y afines',
                    labels={
                     "año_final": "Año",
                     "sector_final": "sector",
                     "primer_curso" : 'matriculados por programa'
                    },
                    nbins=8)
fig5.update_layout( yaxis_title="matriculas primer curso/programa" )

fig6 = px.scatter(info_docs, 
                  x = 'Valor Total', 
                  y = 'primer_curso_final', 
                  color = 'sector_final', 
                  size = 'puntaje_fig',
                  title = 'promedio de matriculas primer curso/programa (2018-2021) vs. costo total del programa a 2023',
                  labels = {
                      'primer_curso_final' : 'matriculas primer curso/programa',
                      'sector_final': 'sector'
                  },
                  hover_name='IES_final',
                  hover_data= ['Valor Total', 'puntaje', 'programas']
                 )
sabana_val = info_docs[info_docs['IES_final']=='universidad de la sabana']['Valor Total'].values[0]
sabana_pc = info_docs[info_docs['IES_final']=='universidad de la sabana']['primer_curso_final'].values[0]
fig6.add_hline(y=sabana_pc)
fig6.add_vline(x=sabana_val)


fig7 = make_subplots(rows=2, cols=2, horizontal_spacing = 0.15)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['ranking QS'], mode = 'markers'),
    row=1, col=2
)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['rnking sapiens'], mode = 'markers'),
    row=1, col=1
)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['scimago institutions rankings'], mode = 'markers'),
    row=2, col=1
)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['webometrics'], mode = 'markers'),
    row=2, col=2
)

# Update xaxis properties
fig7.update_xaxes(title_text="total graduados de doctorado", row=1, col=1)
fig7.update_xaxes(title_text="total graduados de doctorado", row=1, col=2)
fig7.update_xaxes(title_text="total graduados de doctorado", row=2, col=1)
fig7.update_xaxes(title_text="total graduados de doctorado", row=2, col=2)

fig7.update_yaxes(title_text="1/ranking QS", row=1, col=2)
fig7.update_yaxes(title_text="1/ranking Sapiens", row=1, col=1)
fig7.update_yaxes(title_text="1/ranking Scimago", row=2, col=1)
fig7.update_yaxes(title_text="1/ranking Webometrics", row=2, col=2)

fig7.update_layout(showlegend = False, title_text="Relación entre el total de graduados de doctorado (2018-2021) y diferentes rankings")


app = dash.Dash(__name__)
app.title = 'Doctorados en Colombia'

app.layout = html.Div([
    html.Div([
        html.H1(children="Estado de los Doctorados en Colombia"),
        html.P(
            children="Elaboración: Miguel Ángel Uribe Laverde"),
        html.P(
            children="Fuente: SNIES")
        ]
    ),
    html.Div(
        [
            html.H2(children = "Evolución general de matrículas en primer curso para los doctorados del país"),
            html.Div([
                dcc.Graph(id="fig1", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig1),
                html.P(children="Como se evidencia en la gráfica, el número de matriculados en primer curso de doctorado en Colombia viene en aumento. En 2014, el total de matrículas nuevas en doctorado fue de 1051, mientras que en 2021 este valor ascendió a 2066, casi el doble. La figura también evidencia un cambio de tendencia importante, en la distribución de las matrículas entre universidades públicas y privadas. Aunque en 2014 había una clara preferencia por los programas doctorales realizados en las universidades públicas, en los años siguientes la brecha se ha reducido. En 2021, por primera vez, el número de matriculados en primer curso para doctorado fue mayor en las universidades privadas.",
                    style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                    ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '50vh'}
                ),
            html.Div(
                [
                    dcc.Graph(
                        id="fig3", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig3
                        ),
                    html.P(
                        children="El área de ingeniería es de la que más absorbe estudiantes de doctorado,  junto con las ciencias sociales y las ciencias de la educación lideran la absorción de doctorados en el país. En 2014, el total de matriculados en primer curso en doctorados de ingeniería fue de 246. En 2021, este número creció a 406. El máximo de doctorantes matriculados en primer curso en doctorados del área de ingeniería fue en 2020 con 437.",
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'}
                        )            
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '50vh'}
                ),
            html.H2(children = "Evolución de matrículas y programas de doctorado en el área de Ingeniería"),
            html.Div(
                [
                    dcc.Graph(
                        id="fig2", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig2),
                    html.P(
                        children="Aparte del aumento en el número de matriculados en primer curso que ya se mencióno (de 246 en 2014 a 406 en 2021), en el área de ingeniería se nota un cierre más significativo en la brecha de matrículas entre universidades públicas y universidades privadas. Mientras en 2014, el 73% de los matriculados de primer curso para un doctorado en ingeniería lo hacían en una universidad pública, en 2021 este parámetro se había reducido al 50%. Así, actualmente en Colombia la distribución de nuevos doctorantes en ingeniería está equilibrada entre universidades públicas y privadas.",
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '50vh'}
                ),
            html.Div(
                [
                    dcc.Graph(
                        id="fig4", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig4),
                    html.P(
                        children="El número de programas doctorales ofertados en ingeniería también viene en aumento. Para 2014 en Colombia se ofrecían 36 programas, en 2021 esa cifra se había duplicado para un total de 72 programas ofrecidos. Sin embargo, la proporción de estos programas en universidades públicas y privadas se ha mantenido estable. En todo el periodo analizado, aproximadamente 2/3 de los programas doctorales ofrecidos en áreas de ingeniería está en universidades públicas.",
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '50vh'}
                ),
             html.Div(
                [
                    dcc.Graph(
                        id="fig5", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig5),
                    html.P(
                        children="Un parámetro que refleja mejor el estado de los programas doctorales en ingeniería es el del número de matriculados anuales en primer curso por programa. Como se muestra en la gráfica, aunque las variaciones son pequeñas, este parámetro tiene una tendencia diferente en las universidades públicas y privadas. Mientras en las universidades públicas la tendencia es decreciente, en las privadas la tendencia es creciente y desde hace varios años, el número de matriculados en primer curso en las universidades privadas es mayor. En 2021, este parámetro alcanzó 7.73 matriculados en primer curso por programa por año.",
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '50vh'}
                ),
            html.H2(children = "¿Cómo se compara la Universidad de La Sabana con otros Doctorados en el Área de Ingeniería?"),
            html.Div(
                [
                    dcc.Graph(
                        id="fig6", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig6),
                    html.P(
                        children="La gráfica muestra la relación existente entre el número de matrículas en primer curso por programa (eval), y el valor promedio de un programa doctoral. Se observa una distinción clara entre los costos doctorales en universidades públicas y privadas. La gran mayoría de las universidades están en el rango entre 5 y 10 estudiantes anuales por programa. Sólo la Universidad de los Andes y la Universidad Santiago de Cali tienen promedios superiores, ambas en el rango más barato entre las privadas. La Universidad de La Sabana se encuentra en el rango por debajo de 5 estudiantes en primer curso por programa con 4.08, al mismo tiempo, está en el extremo más caro de la distribución. El tamaño de las burbujas está relacionado con el puntaje de la institución en el ranking Sapiens. Los puntos más pequeños corresponden a instituciones sin puntaje.",
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '50vh'}
                ),
            html.H2(children = "¿Cuál es el impacto de atraer estudiantes doctorales?"),
            html.Div(
                [
                    dcc.Graph(
                        id="fig7", 
                        style={'width': '100%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig7),
                    html.P(
                        children="Como se observa, existe una clara correlación entre la cantidad de estudiantes doctorales graduados en los últimos 4 años en cada institución, y su posición en los diferentes rankings universitarios nacionales e internacionales. La creación de doctorados y de programas de financiamiento que permitan atraer a los mejores investigadores del país es necesaria para que la Universidad mejore aún más su posición en estos rankings y mejore su absorción en pregrados y maestrías.",
                        style={'width': '100%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '70vh'}
                ),
        ])
])
  

if __name__ == "__main__":
    app.run_server(debug=True)