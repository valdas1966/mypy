import plotly.express as px
import pandas as pd

csv_betexplorer = 'G:\\Study\\BigData\\Soccer\\BetExplorerResults.csv'
csv_countries_plotly = 'G:\\Study\\BigData\\Soccer\\countries_plotly.csv'
csv_countries_betexplorer = \
    'G:\\Study\\BigData\\Soccer\\countries_betexplorer.csv'


world = px.data.gapminder()
countries = world['country'].unique()
df_plotly = pd.DataFrame(countries)
df_plotly.to_csv(csv_countries_plotly)

df_bete = pd.read_csv(csv_betexplorer, low_memory=False)
df_bete = pd.DataFrame(df_bete['Column3'].unique())
df_bete.to_csv(csv_countries_betexplorer)



