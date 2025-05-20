# Project2_Ecommerce_Analysis
Este projeto foi desenvolvido como parte da disciplina de Análise de Dados da EBAC, durante o módulo "Manipulação de Dados com Python". O objetivo era analisar dados de uma plataforma fictícia de e-commerce oferecida pela disciplina. O conjunto de dados foi limpo, processado e preparado para permitir análises mais precisas. Por fim, foi criada uma aplicação Dash para facilitar a visualização dos insights obtidos. O código-fonte da aplicação Dash está incluído nos arquivos do projeto.

## Etapas do projeto
### Tratamento dos dados
- Identificação de dados nulos:
  ```
  # Verifique a quantidade de linhas e colunas
  linhas_colunas = df.shape
  print('Verificar a qtd de Linhas e colunas: ', linhas_colunas)

  # Verifique os tipos de dados
  tipos = df.dtypes
  print('Verificar Tipagem:\n', tipos)

  # Verifique a quantidade de valores nulos
  nulos = df.isnull().sum()
  print('Verificar valores nulos:\n', nulos)
  ```
- Uso do método **'fillna'** do pandas para substituir valores nulos das colunas 'Temporada' e 'Marca' pelo texto 'Não definido':
  ```
  df['Temporada'] = df['Temporada'].fillna('Não definido')
  df['Marca'] = df['Marca'].fillna('Não definido')
  ```
- Uniformização dos dados de texto para serem escritos em minúsculo:
  ```
  # Converter a coluna 'Marca' para letras minúsculas
  df['Marca'] = df['Marca'].str.lower()

  # Converter a coluna 'Material' para letras minúsculas
  df['Material'] = df['Material'].str.lower()

  # Converter a coluna 'Temporada' para letras minúsculas
  df['Temporada'] = df['Temporada'].str.lower()
  ```
- Remoção das linhas duplicadas:
  ```
  df.drop_duplicates()
  ```
- Remoção das linhas com menos de 8 valores não nulos através do parâmetro **'thresh'**:
  ```
  df = df.dropna(thresh=8)
  ```
- Utilização do **método IQR** para identificar outliers:
  ```
  # Calcular o intervalo interquartil (IQR)
  q1 = df['N_Avaliacoes'].quantile(0.25)
  q3 = df['N_Avaliacoes'].quantile(0.75)
  iqr = q3 - q1

  # Definir o limite superior para identificar outliers
  limite_alto = q3 + 1.5 * iqr

  # Filtrar os produtos que possuem um número de avaliações maior que o limite superior
  df_avaliados = df[df['N_Avaliacoes'] >= limite_alto]
  print(df_avaliados)
  ```
- Tratamento de colunas:
  - Coluna 'Desconto', que apresentava valores com o seguinte formato'18% OFF', foi tratada para representar apenas o numeral 18 da seguinte maneira:
    ```
    # Converter a coluna 'Desconto' para string
    
    df['Desconto'] = df['Desconto'].astype(str)
    print(df['Desconto'])
    
    # A função lambda é usada aqui para remover o símbolo '%' da string na coluna 'Desconto'
    
    df['Desconto'] = df['Desconto'].apply(lambda x: x.split('%')[0].strip() if '%' in x else x)
    print(df['Desconto'])
    ```
  - Coluna 'Condição', que apresentava valores com o seguinte formato 'Novo|+10mil vendidos', foi dividida em duas novas colunas 'Condicao_Atual' e 'Qtd_Vendidos' da seguinte maneira:
    ```
    # Extrair e limpar os dados da coluna 'Condicao'
    # A função lambda é usada aqui para pegar a primeira palavra da string na coluna 'Condicao'
    # x.split(' ')[0] pega a primeira palavra da string.
    
    df['Condicao_Atual'] = df['Condicao'].apply(lambda x: x.split(' ')[0].strip())
    
    # A função lambda é usada aqui para pegar a quinta palavra da string na coluna 'Condicao' se existir, caso contrário, retorna 'Nenhum'
    
    df['Qtd_Vendidos'] = df['Condicao'].apply(lambda x: x.split('|')[1].strip().split(' ')[0].strip() if len(x.split('|')) > 1 else 'Nenhum')
    ```
### Preparação dos dados
- Verificação dos dados únicos:
  ```
  unicos = df.nunique()
  print('Analise de dados únicos:\n', unicos)
  ```
- Verificação geral das estatísticas dos campos numéricos:
  ```
  estatisticas = df.describe()
  print('Estatísticas dos dados:\n', estatisticas)
  ```
- Criação do campo 'Preco' utilizando os dados das colunas 'Reais' e 'Centavos':
  ```
  df['Preco'] =  df['Reais'] + ((df['Centavos'])/100)
  print("DataFrame com campo 'preco':\n", df.head())
  ```
- Remoção de campos desnecessários para análise:
  ```
  df = df.drop(labels=['Reais', 'Centavos', 'Condicao_Atual'], axis=1)
  print("DataFrame atualizado:\n", df.head())
  ```
- Normalização dos dados numéricos 'Nota', 'N_Avaliacoes', 'Desconto' e 'Preco' por meio da função **MinMaxScaler** da biblioteca **scikit-learn**
  ```
  scaler = MinMaxScaler()
  df['Nota_MinMax'] = scaler.fit_transform(df[['Nota']])
  
  df['N_Avaliacoes_MinMax'] = scaler.fit_transform(df[['N_Avaliacoes']])
  
  df['Desconto_MinMax'] = scaler.fit_transform(df[['Desconto']])
  
  df['Preco_MinMax'] = scaler.fit_transform(df[['Preco']])
  ```
- Criação dos campos 'Marca_Cod', 'Material_Cod' e 'Temporada_Cod' a partir da codificação numérica dos campos 'Marca', 'Material' e 'Temporada' utilizando o **LabelEncoder** da biblioteca **scikit-learn**.
  ```
  label_encoder = LabelEncoder()
  df['Marca_Cod'] = label_encoder.fit_transform(df['Marca'])

  df['Material_Cod'] = label_encoder.fit_transform(df['Material'])

  df['Temporada_Cod'] = label_encoder.fit_transform(df['Temporada'])
  ```
- Criação do campo 'Qtd_Vendidos_Cod' com a transformação do campo 'Qtd_Vendidos' para número de acordo com as suas grandezas ('Nenhum', '1', '2', '3', '4', '+5', '+25', '+50', '+100', '+1000', '+10mil' '+50mil'), exemplo +10mil = 10000.
  ```
  qtd = {'Nenhum':0, '1':1, '2':2, '3':3, '4':4, '+5':5, '+25':25, '+50':50, '+100':100, '+1000':1000, '+10mil':10000, '+50mil':50000}
  df['Qtd_Vendidos_Cod'] = df['Qtd_Vendidos'].map(qtd)
  ```
- Criação dos campos 'Marca_Freq' e 'Material_Freq' a partir da transformação dos campos 'Marca' e 'Material' para valores numéricos de acordo com sua frenquência:
  ```
  marca_freq = df['Marca'].value_counts() / len(df)
  df['Marca_Freq'] = df['Marca'].map(marca_freq)

  material_freq = df['Material'].value_counts() / len(df)
  df['Material_Freq'] = df['Material'].map(material_freq)
  ```
### Visualização dos dados com Dash
Após as etapas de limpeza, tratamento e preparação dos dados, foram criadas visualizações gráficas com o objetivo de facilitar a análise e a interpretação de padrões de comportamento no e-commerce. Para isso, foi desenvolvida uma aplicação interativa utilizando a biblioteca **Dash**.

Os gráficos implementados são:
- Histograma: Distribuição das notas atribuídas aos produtos.
- Gráfico de dispersão: Relação entre o número de avaliações e a quantidade vendida.
- Mapa de calor (Heatmap): Correlação entre variáveis numéricas normalizadas.
- Gráfico de barras: As 10 marcas com maior número de vendas.
- Gráfico de pizza: Proporção de vendas por gênero.
- Gráfico de densidade: Distribuição de preços dos produtos.
- Gráfico de regressão: Tendência entre avaliações e vendas, com linha de regressão linear.

A aplicação é executada localmente e exibe todos os gráficos de forma organizada, permitindo uma análise visual dos dados de e-commerce.
