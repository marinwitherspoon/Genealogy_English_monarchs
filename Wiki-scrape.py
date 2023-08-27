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

# - clean up name column -------------------
#seperate the name form the rest of the string
df_all[['Name', 'desc']] = df_all['Name'].str.split(r'\s\d|\[\d+\]', 1, expand=True)

#remove any left over markers including excess spaces
df_all['desc'] = df_all['desc'].str.replace(r'^\[\d+\]\s*|c\.\s*', '', regex=True)
df_all['desc'] = df_all['desc'].str.strip()

#split before first number?
print(df_all['Name'])
print(df_all['desc'])
