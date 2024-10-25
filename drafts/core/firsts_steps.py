from robot import Robot

matriz = [
    [[1], ["AM", "VM", "AM", "VM"]],
    [[3], ["PR", "VM", "AM", "VM"]],
    [[5], ["PR", "VM", "AZ", "VM"]],
    [[7], ["PR", "VM", "AZ", "AM"]],
    [[8], ["PR", "PR", "AZ", "AM"]],
    [[9], ["PR", "VM", "AZ", "VM"]],
    [[10], ["PR", "AM", "AZ", "AM"]],
    [[11], ["PR", "VM", "AZ", "VM"]],
    [[14], ["AM", "VM", "AM", "VM"]],
    [[16], ["AM", "VM", "PR", "VM"]],
    [[18], ["PR", "VM", "AZ", "VM"]],
    [[20], ["PR", "VM", "AZ", "VM"]],
    [[21], ["PR", "AM", "AZ", "PR"]],
    [[22], ["PR", "VM", "AZ", "VM"]],
    [[23], ["PR", "AM", "AZ", "AM"]],
    [[24], ["PR", "VM", "AZ", "VM"]],
    [[27], ["AM", "VM", "PR", "VM"]],
    [[29], ["AM", "VM", "PR", "VM"]],
    [[31], ["AM", "VM", "AZ", "VM"]]
]

def rotacionar_lista(lista, posicoes):
    return lista[posicoes:] + lista[:posicoes]

def todas_combinacoes(matriz):
    nova_matriz = []
    for sublista in matriz:
        item = [sublista[0], sublista[1]]
        for i in range(1, 4):
            item.append(rotacionar_lista(sublista[1], i))
        nova_matriz.append(item)

    sublista_indices = {}
    for item in nova_matriz:
        for j in range(1, len(item)):
            sublista = tuple(item[j])
            if sublista not in sublista_indices:
                sublista_indices[sublista] = [item[0][0]]  
            elif item[0][0] not in sublista_indices[sublista]:
                sublista_indices[sublista].append(item[0][0])  

    for sublista, indices in sublista_indices.items():
        print(f"{list(sublista)}: {indices}")
        return sublista_indices

todas_combinacoes(matriz)


def adivinha_vertice(lista):
    lista_tuple = tuple(lista)
    if lista_tuple in sublista_indices and len(sublista_indices[lista_tuple]) == 1:
        return "V"+str(sublista_indices[lista_tuple][0] )
    return None 

resultado = adivinha_vertice(['AZ', 'AM', 'PR', 'VM'])
print(resultado)
    