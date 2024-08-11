
# This is a sample Python script.
import Load_tables
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


#Definir variables
etiquetas=["1 Día","1 Semana","1 Mes","1 Año"]
visibilidad=[True,False,False,False]
dias=[1,5,21,126,252 ]
categoria_seleccion = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
color_seleccion = ['#00FF00', '#66FF66', '#00CC00', '#009900', '#E0E0E0', '#FFFF00', '#FF8000', '#FF0000']


def  mapa():
    df_fechas =pd.DataFrame
    df_fechas= Load_tables.leer_fecha_data()
    df_stock =Load_tables.leer_stock_data()
    df_activos= Load_tables.leer_activos()

    fact_df = pd.merge(df_fechas, df_stock, how="inner", on=["ID_DATE", "ID_DATE"])
    fact_df= pd.merge (fact_df, df_activos, how= "left", on =["ID_ASSET" ,"ID_ASSET" ])

    df_fechas_comparative = pd.DataFrame()
    temp_df=pd.DataFrame()

    for i in range(len(dias)):
        df_fechas_comparative = df_fechas_comparative.append(   df_fechas[ ( df_fechas['ID_DATE']) == df_fechas['ID_DATE'].max() - dias[i]  ])

    for i in range(len(dias)):
        visual_df = fact_df[ (fact_df['ID_DATE']) >= fact_df['ID_DATE'].max() - dias[i] - 50  ] #revisar porque 50 agregar
        visual_df.loc[:,'Cambio Porcentual']=visual_df.sort_values('Date').groupby(['ID_ASSET'])['ADJ_CLOSE'].pct_change(periods= dias[i])
        visual_df['Variacion']=visual_df['SYMBOL'] + ' ' + visual_df['Cambio Porcentual'].astype(str)
        visual_df=visual_df[( visual_df['Date'] == visual_df['Date'].max())]
        condicion = [visual_df['Cambio Porcentual'] >= 0.30,visual_df['Cambio Porcentual'] >= 0.20, visual_df['Cambio Porcentual'] >= 0.10,
             visual_df['Cambio Porcentual'] >= 0.05,(visual_df['Cambio Porcentual'] > - 0.05) & (visual_df['Cambio Porcentual'] < 0.05 ),
            visual_df['Cambio Porcentual'] <= -0.05, visual_df['Cambio Porcentual'] <= -0.10,visual_df['Cambio Porcentual'] >= -0.15]
        visual_df['Condition'] = np.select(condicion,categoria_seleccion)
        seleccion_color=[visual_df['Condition'] == 'A',  visual_df['Condition'] == 'B', visual_df['Condition'] == 'C', visual_df['Condition'] == 'D',
                     visual_df['Condition'] == 'E', visual_df['Condition'] == 'F', visual_df['Condition'] == 'G',visual_df['Condition'] == 'H']
        visual_df['Color']=np.select(seleccion_color,color_seleccion)
        visual_df['Change_Day']=dias[i]
        frames = [ temp_df, visual_df]
        temp_df=pd.concat(frames)

    visual_df=pd.concat(frames)

    fig = make_subplots(
        cols = 2, rows = 1,
        column_widths = [0.4, 0.4],
        subplot_titles = ('BMV: <b>Acciones<br />&nbsp;<br />', 'BMV: <b>ETF<br />&nbsp;<br />'),
        specs = [[{'type': 'treemap', 'rowspan': 1}, {'type': 'treemap'}]]
    )

    for i in range(len(etiquetas)):
        fig.add_trace(go.Treemap(
            branchvalues = "remainder",
            text=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'A')]['Cambio Porcentual'].to_list(),
            labels= visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'A')]['SYMBOL'].to_list(),
            parents=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'A')]['STOCK_EXCHANGE'].to_list(),
            values=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'A')]['ADJ_CLOSE'].to_list(),
            visible=visibilidad[i],
            name=etiquetas[i],
            marker=dict (colors=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'A')]['Color']),
            textinfo = "label+value",
            texttemplate="<b>%{label}</b><br>%{text:.2%}</br>",
        #root_color="whitesmoke"
        ),row = 1, col = 1)

    i=0

    for i in range(len(etiquetas)):
        fig.add_trace(go.Treemap(
            branchvalues = "remainder",
            text=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'E')]['Cambio Porcentual'].to_list(),
            labels= visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'E')]['SYMBOL'].to_list(),
            parents=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'E')]['STOCK_EXCHANGE'].to_list(),
            values=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'E')]['ADJ_CLOSE'].to_list(),
            visible=visibilidad[i],
            name=etiquetas[i],
            marker=dict (colors=visual_df.loc[(visual_df['Change_Day'] == dias[i]) &  (visual_df['CATEGORY'] == 'E')]['Color']),
            textinfo = "label+value",
            texttemplate="<b>%{label}</b><br>%{text:.2%}</br>",
            ),row = 1, col = 2)


    fig.update_layout(
        uniformtext= dict(minsize=16,mode='hide'),
        margin = dict(t=50, l=25, r=25, b=25),
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="1 Día",
                        method="update",
                        args=[{"visible": [True, False, False, False] } ]),
                    dict(label="1 Semana",
                        method="update",
                        args=[{"visible": [False, True, False, False ]}]),
                    dict(label="1 Mes",
                         method="update",
                        args=[{"visible": [False, False, True, False]}]),
                    dict(label="1 Año",
                        method="update",
                        args=[{"visible": [False, False, False, True] }]),
                ]),
            )
        ]
    )

    fig.update_traces( hovertemplate= "<b>%{label}</b><br>Precio: %{value:$.2f}</br><br>Tipo: %{parent}</br>" ,  root_color="White"
                   )

    fig.show()

if __name__ == '__main__':
    print("Iniciando Visualización: ")
    mapa()