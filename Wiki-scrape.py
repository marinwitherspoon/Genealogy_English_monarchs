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

#  clean data  ##########################

# Delete rows with invalid data
df_all.drop([18, 25, 48], inplace=True)
#reset indexing
df_all.reset_index(drop=True, inplace=True)

# - clean up name column -------------------
#seperate the name form the rest of the string
df_all['Name'] = df_all['Name'].str.replace(r'\[.*?\]', '')

#cleaning name column to include only names
df_all[['Name', 'desc']] = df_all['Name'].str.split(r'\s\d|\[\d+\]', 1, expand=True)
df_all['Name'] = df_all['Name'].apply(lambda row: ' '.join(sorted(set(row.split()), key=row.index)))

#exstract dates from description
df_all['dates'] = df_all['desc'].str.extract(r'(\s*\d{3,4}\s*(?:–\s*\d{0,2}\s*\w*\s*\d{3,4})?)')
df_all['dates'][29] = '1307 – 1327'
df_all['dates'][3] = '927 – 939'
#remove days and months
df_all['dates'] = df_all['dates'].str.replace(r'\s+\d{0,2}\s+\w*\s+', ' ')

# - clean up Birth column -------------------
df_all['Birth'] = df_all['Birth'].str.extract(r'(\d{3,4})')

# - clean up Death column -------------------
df_all['Death'] = df_all['Death'].str.extract(r'(\d{3,4})')

# - clean up Claim column -------------------
df_all['Claim'] = df_all['Claim'].str.replace(r'/.*?of', 'of')
#exstract relationship
df_all['ClaimRelation'] = df_all['Claim'].str.extract(r'(\w*(?:-\w+)*(?:Son|Daughter))\s+',flags=re.IGNORECASE)
# exstract and clean up names
df_all['Claim'] = df_all['Claim'].str.extract(r'(?:Son|Daughter)\s+of\s+(\w+\s*(?:[IV]+|of\s+\w+|the\s+\w+)*)',flags=re.IGNORECASE)
df_all['Claim'] = df_all['Claim'].str.replace(r'(?<=[^ ])(?<![IV])([A-Z])(.*?)$','')

#manually correct data
df_all['Claim'][10] = NaN
df_all['Claim'][45] = 'spouse'
