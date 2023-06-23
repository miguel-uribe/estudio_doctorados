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
ies_df = pd.read_excel('consolidado_ies_doc.xlsx')
info_docs['puntaje_fig'] = info_docs['puntaje']+5
info_docs['total_pc'] = info_docs['programas']*info_docs['primer_curso_final']
docs_df = pd.read_excel('base_programas_doctorado.xlsx')
docs_df['sabana'] = False
docs_df.loc[docs_df['IES_final']=='universidad de la sabana','sabana'] = True


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

fig2.write_image("primer_curso_doctorados.jpeg", scale = 10, width = 800, height = 600)


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
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['ranking QS'], mode = 'markers',  marker=dict(
                size=10,
            )),
    row=1, col=2
)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['rnking sapiens'], mode = 'markers',  marker=dict(
                size=10,
            )),
    row=1, col=1
)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['scimago institutions rankings'], mode = 'markers',  marker=dict(
                size=10,
            )),
    row=2, col=1
)

fig7.add_trace(
    go.Scatter(x=grad_df['graduados_final'], y=1/grad_df['webometrics'], mode = 'markers',  marker=dict(
                size=10,
            )),
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


fig8 = px.bar(ies_df.sort_values(by=['sector_final','primer_curso_final'], ascending = False), 
              x = 'ies_municipio', 
              y = 'primer_curso_final', 
              color = 'sector_final', 
              hover_name='ies_municipio', 
              hover_data = ['años'],
              labels = {
                      'primer_curso_final' : 'matriculados primer curso',
                      'sector_final': 'sector'
                  },
             )
v_sabana = ies_df[ies_df['ies_municipio']=='universidad de la sabana - chia']['primer_curso_final'].values[0]
fig8.add_hline(y=v_sabana)

fig8.update_layout(
    title="promedio de matriculados en primer curso (2018-2021)",
    xaxis_title=""
    )

fig8.write_image("matriculas_primer_curso_institucion.jpeg", scale = 10, width = 800, height = 800)


fig9 = px.bar(ies_df.sort_values(by=['sector_final','primer_curso_programa'], ascending = False), 
              x = 'ies_municipio', 
              y = 'primer_curso_programa', 
              color = 'sector_final', 
              hover_name='ies_municipio', 
              hover_data = ['años'],
              labels = {
                      'primer_curso_final' : 'matriculados primer curso',
                      'sector_final': 'sector',
                      'primer_curso_programa' : 'matriculas primer curso/programa'
                  },
             )
v_sabana = ies_df[ies_df['ies_municipio']=='universidad de la sabana - chia']['primer_curso_programa'].values[0]
fig9.add_hline(y=v_sabana)

fig9.update_layout(
    title="promedio de matriculados en primer curso por programa (2018-2021)",
    xaxis_title=""
    )

fig9.write_image("matriculas_primer_curso_por_programa_institucion.jpeg", scale = 10, width = 800, height = 800)

fig10 = px.scatter(docs_df, x = 'Valor Total', y = 'primer_curso_final', size = 'años_reportados', color = 'sector_final',  symbol = 'sabana',
                  hover_name='programa_academico_final', 
                  hover_data = ['IES_final', 'Valor Semestral', 'Semestres'],
                  title = 'promedio de matriculados primer curso por programa (2018-2021)',
                  labels = {
                      'primer_curso_final' : 'matriculados primer curso',
                      'sector_final': 'sector',
                      'primer_curso_programa' : 'matriculas primer curso/programa',
                      'IES_final': 'IES',
                      'años_reportados': 'años reportados',
                      'Valor Total': 'valor total'
                  },
                 )

fig10.update_traces(marker={'sizeref': 0.03})


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
            html.H2(children = "¿Cómo se distribuyen las matrículas de Doctorado en el país?"),
            html.Div(
                [
                    dcc.Graph(
                        id="fig8", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig8),
                    dcc.Graph(
                        id="fig9", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig9),
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '100vh'}
            ),
            html.P(
                        children="En términos del total de matrículas del doctorado, la Universidad de la Sabana es quinta entre las universidades privadas, con alrededor de 12 doctorandos al año. Al tener en cuenta las universidades privadas, cae al puesto 12. Sin embargo, al considerar el número de estudiantes por programa, la tendencia cambia, y la Universidad de La Sabana cae el 9 lugar entre las privadas y al puesto 19 si se tienen en cuenta las universidades públicas. En general, estos datos evidencian que la absorción de estudiantes doctorales por parte de la Universidad podría mejorar y acercarse a la absorción de los competidores directos.",
                        style={'width': '100%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'}),
            html.H2(children = "¿Cómo se comportan individualmente los programas de Doctorado en el área de Ingeniería en el País?"),
            html.Div(
                [
                    dcc.Graph(
                        id="fig10", 
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block'},
                        figure = fig10),
                    html.P(
                        children="La gráfica muestra la relación entre el valor del programa y promedio de matriculados en primer curso por año, en los últimos cuatro años. El tamaño del símbolo representa la cantidad de años reportados. Los programas de la Universidad de La Sabana aparecen representados por rombos. Sobresalen entre todos los programas los de Doctorado en Ingeniería de la Universidad de los Andes y de la Universidad del Valle, también el programa de Doctorado en Ciencias Aplicadas de la Universidad Santiago de Cali (abierto en 2021). La distribución de estudiantes en universidades públicas y privadas es similar. En el caso de la Universidad de La Sabana, sólo el programa de Biociencias supera el umbral de 5 estudiantes por año en promedio. Nuestros programas de Doctorado en Biociencias y en Ingenieríaestán en el espectro más caro de la formación.",
                        style={'width': '50%', 'height': '100%',  'display': 'inline-block', 'verticalAlign': 'middle'})
                ],
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '70vh'}
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
                style={'width': '100%',  'display': 'inline-block', 'horizontal-align': 'middle', 'verticalAlign': 'top', 'height': '80vh'}
                ),
        ])
])
  

if __name__ == "__main__":
    app.run_server(debug=True)