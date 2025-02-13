from pybricks.parameters import Color
import constants as const
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

    def find_best_path(self, inicio: int, destinations: list):
        """Encontra o melhor caminho entre um vértice de início e uma lista de destinos, retornando o caminho, a distância e o conjunto de instruções pra percorrer."""
        paths = []
        for target in destinations:
            path, distance, instructions = self.dijkstra(inicio, target)
            paths.append((path, distance, instructions))
        paths.sort(key=lambda x: x[1])
        return paths[0]

    def recalcular_caminho_sem_obstaculos(self, inicio, fim):
        for vertice in self.obstaculos:
            self.unmark_obstacle(vertice)
            caminho, distancia, _ = self.dijkstra(inicio, fim)
            if distancia != float("inf"):
                return caminho, distancia
        return None, float("inf")


map_matrix = [
    [[0]],
    [[1], ["V0", "O", const.CELL_DISTANCE_TO_PARK], ["V2", "L", const.CELL_DISTANCE], ["V7", "S", const.CELL_DISTANCE]],
    [[2]],
    [[3], ["V4", "L", const.CELL_DISTANCE], ["V9", "S", const.CELL_DISTANCE]],
    [[4]],
    [[5], ["V6", "L", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF], ["V11", "S", const.CELL_DISTANCE]],
    [[6], ["V5", "O", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF]],
    [[7], ["V1", "N", const.CELL_DISTANCE], ["V8", "L", const.CELL_DISTANCE], ["V14", "S", const.CELL_DISTANCE]],
    [[8], ["V7", "O", const.CELL_DISTANCE], ["V2", "N", const.CELL_DISTANCE], ["V9", "L", const.CELL_DISTANCE]],
    [[9], ["V8", "O", const.CELL_DISTANCE], ["V3", "N", const.CELL_DISTANCE], ["V10", "L", const.CELL_DISTANCE], ["V16", "S", const.CELL_DISTANCE]],
    [[10], ["V9", "O", const.CELL_DISTANCE], ["V4", "N", const.CELL_DISTANCE], ["V17", "S", const.CELL_DISTANCE], ["V11", "L", const.CELL_DISTANCE]],
    [
        [11],
        ["V10", "O", const.CELL_DISTANCE],
        ["V12", "L", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF],
        ["V5", "N", const.CELL_DISTANCE],
        ["V18", "S", const.CELL_DISTANCE],
    ],
    [[12], ["V11", "O", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF]],
    [[13]],
    [[14], ["V13", "O", const.CELL_DISTANCE_TO_PARK], ["V15", "L", const.CELL_DISTANCE], ["V20", "S", const.CELL_DISTANCE], ["V7", "N", const.CELL_DISTANCE]],
    [[15]],
    [[16], ["V15", "O", const.CELL_DISTANCE], ["V9", "N", const.CELL_DISTANCE], ["V22", "S", const.CELL_DISTANCE]],
    [[17]],
    [
        [18],
        ["V11", "N", const.CELL_DISTANCE],
        ["V19", "L", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF],
        ["V24", "S", const.CELL_DISTANCE],
    ],
    [[19], ["V18", "O", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF]],
    [[20], ["V14", "N", const.CELL_DISTANCE], ["V21", "L", const.CELL_DISTANCE], ["V27", "S", const.CELL_DISTANCE]],
    [[21], ["V28", "S", const.CELL_DISTANCE], ["V22", "L", const.CELL_DISTANCE], ["V20", "O", const.CELL_DISTANCE]],
    [[22], ["V21", "O", const.CELL_DISTANCE], ["V23", "L", const.CELL_DISTANCE], ["V29", "S", const.CELL_DISTANCE], ["V16", "N", const.CELL_DISTANCE]],
    [[23], ["V22", "O", const.CELL_DISTANCE], ["V17", "N", const.CELL_DISTANCE], ["V30", "S", const.CELL_DISTANCE], ["V24", "L", const.CELL_DISTANCE]],
    [
        [24],
        ["V23", "O", const.CELL_DISTANCE],
        ["V25", "L", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF],
        ["V31", "S", const.CELL_DISTANCE],
        ["V18", "N", const.CELL_DISTANCE],
    ],
    [[25], ["V24", "O", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF]],
    [[26]],
    [[27], ["V26", "O", const.CELL_DISTANCE_TO_PARK], ["V20", "N", const.CELL_DISTANCE]],
    [[28]],
    [[29], ["V28", "O", const.CELL_DISTANCE], ["V22", "N", const.CELL_DISTANCE]],
    [[30]],
    [
        [31],
        ["V30", "O", const.CELL_DISTANCE],
        ["V32", "L", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF],
        ["V24", "N", const.CELL_DISTANCE],
    ],
    [[32], ["V31", "O", const.CELL_DISTANCE_TO_BOARDING - ROBOT_SIZE_HALF]],
]


def get_target_for_passenger(child_adult: str, color):
    """
    Retorna o nro. do vértice alvo do passageiro no grafo do mapa, baseando-se no tamanho ("CHILD" ou "ADULT") e cor.
    No caso da criança verde, retorna os três vértices do parque.
    """
    passenger_lookup_table = {
        "CHILD": {
            Color.GREEN: [0, 13, 26],
            Color.BLUE: [4],
            Color.BROWN: [30],
        },
        "ADULT": {
            Color.GREEN: [17],
            Color.BLUE: [28],
            Color.BROWN: [2],
            Color.RED: [15],
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
