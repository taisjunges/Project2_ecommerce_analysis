import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from dash import Dash, html, dcc

df = pd.read_csv('C:/Users/tajun/OneDrive/Documents/EBAC/Curso Analista de dados/Parte 4 - Manipulação de dados com Python/atividades/ecommerce_estatistica.csv')

# Função que cria os gráficos
def cria_grafico_hitograma():
    fig1 = px.histogram(
        df,
        x='Nota',
        nbins=30,
        title='Histograma - Distribuição das notas'
    )
    return fig1

def cria_grafico_dispersao():
    fig2 = px.scatter(
        df,
        x='N_Avaliações',
        y='Qtd_Vendidos_Cod',
        title='Quantidade de avaliações vs. quantidade vendida',
        labels={'N_Avaliações':'Quantidade de avaliações', 'Qtd_Vendidos_Cod':'Quantidade ventida'}
    )
    return fig2

def cria_grafico_heatmap():
    df_corr = df[['Nota_MinMax', 'N_Avaliações_MinMax', 'Desconto_MinMax', 'Preço_MinMax', 'Qtd_Vendidos_Cod']].corr()

    fig3 = px.imshow(
        df_corr,
        text_auto=True,
        color_continuous_scale='Viridis',
        title='Mapa de Calor – Correlação entre Variáveis'
    )
    return fig3

def cria_grafico_barra():
    top_marcas = df['Marca'].value_counts().nlargest(10).reset_index()
    top_marcas.columns = ['Marca', 'Quantidade'] # renomear colunas do dataframe top_marcas

    fig4 = px.bar(
        top_marcas,
        x='Marca',
        y='Quantidade',
        title='Top 10 Marcas Mais Vendidas',
        text='Quantidade',
        color_discrete_sequence=['#636EFA']
    )

    fig4.update_layout(
        xaxis_title='Marca',
        yaxis_title='Quantidade de Vendas',
    )
    return fig4

def cria_grafico_pizza():
    genero_vendas = df['Gênero'].value_counts().reset_index()
    genero_vendas.columns = ['Gênero', 'Quantidade']

    fig5 = px.pie(
        genero_vendas,
        names='Gênero',
        values='Quantidade',
        title='Distribuição de Vendas por Gênero',
        hole=0.2,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    return fig5

def cria_grafico_densidade():
    precos = [df['Preço'].dropna()]
    fig6 = ff.create_distplot(
        precos,
        group_labels=['Preço'],
        show_hist=False,
        show_rug=False
    )
    fig6.update_layout(
        title='Densidade de Preços',
        xaxis_title='Preços',
        yaxis_title='Densidade'
    )
    return fig6

def cria_grafico_regressao():
    fig7 = px.scatter(
        df,
        x='N_Avaliações',
        y='Qtd_Vendidos_Cod',
        trendline='ols',  # Adiciona linha de regressão linear
        opacity=0.5,
        title='Regressão de Quantidade de Avaliações e Vendas',
        labels={'N_Avaliações': 'Nº de Avaliações', 'Qtd_Vendidos_Cod': 'Qtd Vendida'}
    )
    fig7.update_traces(marker=dict(color='#34c289'))  # Cor dos pontos
    fig7.update_layout(showlegend=False)
    return fig7

# Funcão que cria app
def cria_app():
    app = Dash(__name__)

    fig1 = cria_grafico_hitograma()
    fig2 = cria_grafico_dispersao()
    fig3 = cria_grafico_heatmap()
    fig4 = cria_grafico_barra()
    fig5 = cria_grafico_pizza()
    fig6 = cria_grafico_densidade()
    fig7 = cria_grafico_regressao()

    app.layout = html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
        dcc.Graph(figure=fig4),
        dcc.Graph(figure=fig5),
        dcc.Graph(figure=fig6),
        dcc.Graph(figure=fig7)
    ])
    return app

# Executa app
if __name__ == '__main__':
    app = cria_app()
    app.run(debug=True, port=8050)