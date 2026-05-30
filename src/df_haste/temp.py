import tomllib

with open('config.toml', "rb") as f:
    data = tomllib.load(f)
data = data['database']
d = {}
for x in data:
    if x['name'] in d: 
        raise ValueError
    d[x['name']] = x 
    del d[x['name']]['name']
print(d)
