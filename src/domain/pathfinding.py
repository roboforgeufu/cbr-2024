from pybricks.parameters import Color

import heapq

ROBOT_SIZE_HALF = 7.7


class Graph:
    def __init__(self, adj_matrix):
        self.adj_matrix = adj_matrix
        self.num_vertices = len(adj_matrix)
        self.obstacles = []

    def add_edge(self, origin, destiny, direction, weight=1):
        self.adj_matrix[origin].append(["V{}".format(destiny), direction, weight])

    def remove_edge(self, origin, destiny):
        vertice = "V" + str(destiny)
        for idx, items in enumerate(self.adj_matrix[origin]):
            if items[0] == vertice:
                self.matriz_lista_adjacencia[origin].pop(idx)

    def show_matrix(self):
        for line in self.adj_matrix:
            print(line)

    def mark_obstacle(self, vertice):
        for line in self.adj_matrix:
            for edge in line:
                if str(edge[0]).strip() == vertice:
                    edge[-1] = float("inf")
        self.obstacles.append(vertice)

    def unmark_obstacle(self, vertice):
        for line in self.adj_matrix:
            for idx_edge, edge in enumerate(line):
                if str(edge[0]).strip() == vertice:
                    index = line[0][0]
                    self.adj_matrix[index][idx_edge] = [
                        edge[0],
                        edge[1],
                        self.adj_matrix[index][idx_edge][2],
                    ]
        self.mostrar_matriz(self.adj_matrix)

    def dijkstra(self, inicio, fim):
        distancias = {i: float("inf") for i in range(self.num_vertices)}
        distancias[inicio] = 0
        heap = [(0, inicio)]
        anterior = {i: None for i in range(self.num_vertices)}
        direcao = {i: None for i in range(self.num_vertices)}
        pesos = {i: None for i in range(self.num_vertices)}

        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)

            if vertice_atual == fim:
                break

            if dist_atual > distancias[vertice_atual]:
                continue

            for vizinho_info in self.adj_matrix[vertice_atual]:
                if len(vizinho_info) == 3:
                    vizinho, dir_cardinal, peso = vizinho_info
                    vizinho_num = int(vizinho[1:])

                    if peso == float("inf"):
                        continue

                    nova_distancia = dist_atual + peso

                    if nova_distancia < distancias[vizinho_num]:
                        distancias[vizinho_num] = nova_distancia
                        anterior[vizinho_num] = vertice_atual
                        direcao[vizinho_num] = dir_cardinal
                        pesos[vizinho_num] = peso
                        heapq.heappush(heap, (nova_distancia, vizinho_num))

        caminho = []
        direcoes_pesos = []
        if distancias[fim] != float("inf"):
            atual = fim
            while atual is not None:
                caminho.append(atual)
                if anterior[atual] is not None:
                    direcoes_pesos.append((direcao[atual], pesos[atual]))
                atual = anterior[atual]
            caminho.reverse()
            direcoes_pesos.reverse()

        return caminho, distancias[fim], direcoes_pesos

    def recalcular_caminho_sem_obstaculos(self, inicio, fim):
        for vertice in self.obstaculos:
            self.unmark_obstacle(vertice)
            caminho, distancia, _ = self.dijkstra(inicio, fim)
            if distancia != float("inf"):
                return caminho, distancia
        return None, float("inf")


map_matrix = [
    [[0]],
    [[1], ["V0", "O", 24], ["V2", "L", 30], ["V7", "S", 30]],
    [[2]],
    [[3], ["V4", "L", 30], ["V9", "S", 30]],
    [[4]],
    [[5], ["V6", "L", 18 - ROBOT_SIZE_HALF], ["V11", "S", 30]],
    [[6], ["V5", "O", 18 - ROBOT_SIZE_HALF]],
    [[7], ["V1", "N", 30], ["V8", "L", 30], ["V14", "S", 30]],
    [[8], ["V7", "O", 30], ["V2", "N", 30], ["V9", "L", 30]],
    [[9], ["V8", "O", 30], ["V3", "N", 30], ["V10", "L", 30], ["V16", "S", 30]],
    [[10], ["V9", "O", 30], ["V4", "N", 30], ["V17", "S", 30], ["V11", "L", 30]],
    [
        [11],
        ["V10", "O", 30],
        ["V12", "L", 18 - ROBOT_SIZE_HALF],
        ["V5", "N", 30],
        ["V18", "S", 30],
    ],
    [[12], ["V11", "O", 18 - ROBOT_SIZE_HALF]],
    [[13]],
    [[14], ["V13", "O", 24], ["V15", "L", 30], ["V20", "S", 30], ["V7", "N", 30]],
    [[15]],
    [[16], ["V15", "O", 30], ["V9", "N", 30], ["V22", "S", 30]],
    [[17]],
    [
        [18],
        ["V11", "N", 30],
        ["V19", "L", 18 - ROBOT_SIZE_HALF],
        ["V24", "S", 30],
    ],
    [[19], ["V18", "O", 18 - ROBOT_SIZE_HALF]],
    [[20], ["V14", "N", 30], ["V21", "L", 30], ["V27", "S", 30]],
    [[21], ["V28", "S", 30], ["V22", "L", 30], ["V20", "O", 30]],
    [[22], ["V21", "O", 30], ["V23", "L", 30], ["V29", "S", 30], ["V16", "N", 30]],
    [[23], ["V22", "O", 30], ["V17", "N", 30], ["V30", "S", 30], ["V24", "L", 30]],
    [
        [24],
        ["V23", "O", 30],
        ["V25", "L", 18 - ROBOT_SIZE_HALF],
        ["V31", "S", 30],
        ["V18", "N", 30],
    ],
    [[25], ["V24", "O", 18 - ROBOT_SIZE_HALF]],
    [[26]],
    [[27], ["V26", "O", 24], ["V20", "N", 30]],
    [[28]],
    [[29], ["V28", "O", 30], ["V22", "N", 30]],
    [[30]],
    [
        [31],
        ["V30", "O", 30],
        ["V32", "L", 18 - ROBOT_SIZE_HALF],
        ["V24", "N", 30],
    ],
    [[32], ["V31", "O", 18 - ROBOT_SIZE_HALF]],
]


def get_target_for_passenger(child_adult: str, color):
    """
    Retorna o nro. do vértice alvo do passageiro no grafo do mapa, baseando-se no tamanho ("CHILD" ou "ADULT") e cor.
    No caso da criança verde, retorna os três vértices do parque.
    """
    passenger_lookup_table = {
        "CHILD": {
            Color.GREEN: (0, 13, 26),
            Color.BLUE: 4,
            Color.BROWN: 30,
        },
        "ADULT": {
            Color.GREEN: 17,
            Color.BLUE: 28,
            Color.BROWN: 2,
            Color.RED: 15,
        },
    }

    return passenger_lookup_table[child_adult][color]


def main():
    inicio = int(input("Vértice inicial:"))
    fim = int(input("Vértice destino:"))

    grafo = Graph(map_matrix)

    try:
        obstaculo = int(input("Obstaculo:"))
        grafo.mark_obstacle("V{}".format(obstaculo))
    except:  # nosec
        pass

    grafo.show_matrix()

    caminho, distancia, direcoes_pesos = grafo.dijkstra(inicio, fim)

    if distancia != float("inf"):
        print("Os vértices visitados são:", caminho)
        print("A distância mínima calculada vale:", distancia)
        print("A saída pra path control:", direcoes_pesos)
    else:
        print("Caminho bloqueado, tentando remover obstáculos.")
        caminho, distancia = grafo.recalcular_caminho_sem_obstaculos(inicio, fim)
        if distancia != float("inf"):
            print("Caminho após remover obstáculos:", caminho)
            print("A distância mínima recalculada vale:", distancia)
        else:
            print("Não foi possível encontrar um caminho, mesmo sem os obstáculos.")


if __name__ == "__main__":
    main()
