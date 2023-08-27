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
df_all['Name'] = df_all['Name'].str.replace(r'\[.*?\]', '')
df_all[['Name', 'desc']] = df_all['Name'].str.split(r'\s\d|\[\d+\]', 1, expand=True)

# clean up names column by removing repeating names
df_all['Name'] = df_all['Name'].apply(lambda row: ' '.join(sorted(set(row.split()), key=row.index)))

#exstract dates from description
df_all['dates'] = df_all['desc'].str.extract(r'(\s*\w*\s*\d{3,4}\s*(?:–\s*\d{0,2}\s*\w*\s*\d{3,4})?)')

# manually set value for messy rows
df_all['dates'][3] = '927 – 27 October 939'
df_all['desc'][29] = 'July 1307 – Abdicated 20 January 1327'
