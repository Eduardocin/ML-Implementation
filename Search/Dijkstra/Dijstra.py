import heapq
import pygame
import math


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra's Algorithm")


RED = (255, 0, 0)         # Células já visitadas (fechadas)
GREEN = (0, 255, 0)       # Células na fronteira (abertas)
BLUE = (0, 255, 0)        # Não utilizado (igual ao verde)
YELLOW = (255, 255, 0)    # Não utilizado
WHITE = (255, 255, 255)   # Células vazias
BLACK = (0, 0, 0)         # Barreiras/obstáculos
PURPLE = (128, 0, 128)    # Caminho final encontrado
ORANGE = (255, 165 ,0)    # Ponto de partida
GREY = (128, 128, 128)    # Grade/linhas divisórias
TURQUOISE = (64, 224, 208) # Ponto de chegada

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
        # Retorna a posição (linha, coluna) da célula na grade
    def get_pos(self):
        return self.row, self.col

    # Métodos para verificar o estado atual da célula
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE
    
    # Métodos para alterar o estado da célula
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    
    def update_neighbors(self, grid):
        """Atualiza a lista de vizinhos válidos da célula"""
        self.neighbors = []
        
        # Verifica vizinho abaixo
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
            
        # Verifica vizinho acima
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
            
        # Verifica vizinho à direita
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
            
        # Verifica vizinho à esquerda
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
        
def dijkstra(draw, grid, start, end):
    """
    Implementa o algoritmo de Dijkstra para encontrar o caminho mais curto em um grid
    
    Parâmetros:
    - draw: função para atualizar a visualização
    - grid: grade de células
    - start: célula inicial
    - end: célula final
    
    Retorna True se um caminho foi encontrado, False caso contrário
    """
    # Inicializa a contagem para desempate na fila de prioridade
    count = 0
    
    # Fila de prioridade para gerenciar os nós a serem explorados
    # (distância, contagem, nó)
    open_queue = []
    heapq.heappush(open_queue, (0, count, start))
    
    # Dicionário para rastrear o caminho - de onde viemos para cada nó
    came_from = {}
    
    # Inicializa as distâncias como infinito para todos os nós
    dist = {spot: float("inf") for row in grid for spot in row}
    dist[start] = 0
    
    # Conjunto para manter os nós visitados
    visited = {spot: False for row in grid for spot in row}
    
    # Enquanto houver nós a serem explorados
    while open_queue:
        # Verifica se o usuário fechou a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        # Obtém o nó atual com a menor distância
        current_dist, _, current = heapq.heappop(open_queue)
        
        # Se já visitamos este nó, continuamos para o próximo
        if visited[current]:
            continue
            
        # Se chegamos ao destino, reconstruímos o caminho
        if current == end:
            # Reconstruir o caminho
            current = end
            while current in came_from:
                current = came_from[current]
                if current != start:  # Não colorimos o início
                    current.make_path()
                draw()
            
            # Garantimos que o início e fim permaneçam marcados
            start.make_start()
            end.make_end()
            return True
        
        # Marca o nó como visitado
        visited[current] = True
        
        # Se não for o nó inicial, marca como fechado (para visualização)
        if current != start:
            current.make_closed()
        
        # Explora os vizinhos do nó atual
        for neighbor in current.neighbors:
            # Se o vizinho já foi visitado, pula
            if visited[neighbor]:
                continue
                
            # Peso constante de 1 entre células adjacentes
            # Em um grafo com pesos variáveis, isso seria o peso da aresta
            new_dist = dist[current] + 1
            
            # Se encontramos um caminho melhor para o vizinho
            if new_dist < dist[neighbor]:
                # Atualiza o caminho e a distância
                came_from[neighbor] = current
                dist[neighbor] = new_dist
                
                # Adiciona o vizinho à fila para exploração
                count += 1
                heapq.heappush(open_queue, (new_dist, count, neighbor))
                neighbor.make_open()  # Para visualização
        
        # Atualiza a visualização após processar cada nó
        draw()
    
    # Se chegamos aqui, não encontramos um caminho
    return False

def reconstruct_path(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()
        
# Cria o grid de células
def make_grid(rows, width):
    grid = []
    gap = width // rows  
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
            
    return grid

# Desenha as linhas da grade
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
            
# Função para atualizar a visualização do grid
def draw(win, grid, rows, width):
    win.fill(WHITE) 

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()  


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

    
def main(win, width):
    ROWS = 50  # Define quantas linhas/colunas terá o grid
    grid = make_grid(ROWS, width)

    start = None  # Ponto inicial
    end = None    # Ponto final

    run = True
    while run:
        # Atualiza a visualização
        draw(win, grid, ROWS, width)
        
        # Processa eventos
        for event in pygame.event.get():
            # Fechar a janela
            if event.type == pygame.QUIT:
                run = False

            # Clique esquerdo do mouse
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            # Clique direito do mouse (reset de células)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # Teclas do teclado
            if event.type == pygame.KEYDOWN:
                # Tecla ESPAÇO inicia o algoritmo
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

            
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Tecla C limpa o grid
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)