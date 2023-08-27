from bs4 import BeautifulSoup
import requests

# url of scrape
url = 'https://en.wikipedia.org/wiki/List_of_English_monarchs'

# Get the HTML content using requests
html_content = requests.get(url).text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

all_king_tables = soup.find_all('table',{'class':"wikitable"})

df_all = pd.DataFrame(columns=['Name', 'Birth', 'Death', 'Claim'])

for i in all_king_tables:
  df=pd.read_html(str(i))[0]

  if 'Claim' in df.columns:
    selected_columns = ['Name', 'Birth', 'Death', 'Claim']
  else:
    selected_columns = ['Name', 'Birth', 'Death']
    df['Claim'] = None 

  # convert list to dataframe
  df=pd.DataFrame(df)[selected_columns]

  df_all = pd.concat([df_all, df], axis=0, ignore_index=True)

# clean data
#############################
# Delete rows with invalid data
df_all.drop([18, 25, 48], inplace=True)
#reset indexing
df_all.reset_index(drop=True, inplace=True)

# Print the updated DataFrame

df_all[['Name', 'description']] = df_all['Name'].str.split(r'\[\d+\]', 1, expand=True)
