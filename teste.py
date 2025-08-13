tamanhos = {
    'micropore': [],
    'mesopore': {'mvs': [], 'ms': [], 'mm': [], 'ml': [], 'mvl': []},
    'megapore': {'megaL': [], 'megaM': [], 'megaS': []},
}

for i in range(1, 6):
    tamanhos['micropore'].append(i)
    tamanhos['mesopore']['mvs'].append(i)
    tamanhos['mesopore']['ms'].append(i+2)


print(tamanhos, len(tamanhos['mesopore']['mvs']) + len(tamanhos['mesopore']['ms']))
print(tamanhos['mesopore']['mvs'][0])
