# %%
import pandas as pd
import ast

# %%
raw = pd.read_csv("c:/Users/David/Documents/Python Projects/Animal Crossing/Crafting Calculator/recipes.csv")

# %%
df = raw[['Internal ID', 'Name', 'Material 1', '#1', 'Material 2', '#2', 'Material 3', '#3', 'Material 4', '#4', 'Material 5', '#5', 'Material 6', '#6', 'Source', 'Category']]

# %%
columns_to_convert = ['#2', '#3', '#4', '#5', '#6']
df.loc[:, columns_to_convert] = df.loc[:, columns_to_convert].apply(pd.to_numeric, errors='coerce').fillna(0).astype(str)
df.loc[:, columns_to_convert] = df.loc[:, columns_to_convert].astype(float)
df.loc[:, columns_to_convert] = df.loc[:, columns_to_convert].astype('Int64')

# %%
material_columns = [f'Material {i}' for i in range(1, 7)]
for column in material_columns:
    df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x: f"'{x}'")

# %%
df.loc[:, 'mat1'] = None
df.loc[df['#1'] > 0, 'mat1'] = df['Material 1'].astype(str) + ": " + df['#1'].astype(str)
df.head()

# %%
def combine_materials(new_column_name, col1, col2, data=df):
    data.loc[:, new_column_name] = None
    data.loc[data[col2] > 0, new_column_name] = data[col1].astype(str) + ": " + data[col2].astype(str)
    return data

# %%
combine_materials('mat1', 'Material 1', '#1')
combine_materials('mat2', 'Material 2', '#2')
combine_materials('mat3', 'Material 3', '#3')
combine_materials('mat4', 'Material 4', '#4')
combine_materials('mat5', 'Material 5', '#5')
combine_materials('mat6', 'Material 6', '#6')

# %%
columns_to_join = ['mat1', 'mat2', 'mat3', 'mat4', 'mat5', 'mat6']
df.loc[:, ['materials']] = df[columns_to_join].apply(lambda row: ', '.join(map(str, [val for val in row if pd.notnull(val)])), axis=1)
columns_to_drop = ['Material 1', '#1', 'Material 2', '#2', 'Material 3', '#3', 'Material 4', '#4', 'Material 5', '#5', 'Material 6', '#6']
df = df.drop(columns = columns_to_join)
df = df.drop(columns = columns_to_drop)

# %%
df.loc[:, 'materials'] = df.loc[:, 'materials'].apply(lambda x:'{' + x + '}')
df = df.rename(columns={'Internal ID': 'id', 'Name': 'name', 'Source': 'source', 'Category': 'category'}).sort_values('id')

# %%
#df['name'] = df['name'].str.title()
df['name'] = df['name'].str.lower()
df['source'] = df['source'].str.title()
df['materials'] = df['materials'].str.title()

# %%
craftables = df.to_dict(orient='records')


# %%

# Convert 'materials' values to dictionaries and remove single quotes
for item in craftables:
    item['materials'] = ast.literal_eval(item['materials'])

craftables


