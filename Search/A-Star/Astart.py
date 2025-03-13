import pygame
import math
from queue import PriorityQueue

# Definição do tamanho da janela (900x900 pixels)
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Definição de cores para diferentes elementos na visualização
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

# Classe que representa cada célula (nó) no grid
class Spot:
    def __init__(self, row, col, width, total_rows):
        # Posição da célula na grade
        self.row = row
        self.col = col
        # Posição em pixels na tela
        self.x = row * width
        self.y = col * width
        self.color = WHITE  # Começa como célula vazia
        self.neighbors = [] # Lista para armazenar vizinhos válidos
        self.width = width  # Largura da célula em pixels
        self.total_rows = total_rows # Número total de linhas no grid

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

    # Desenha a célula na janela
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Atualiza a lista de vizinhos válidos (não-barreiras) da célula
    def update_neighbors(self, grid):
        self.neighbors = []
        # Verifica célula abaixo
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Verifica célula acima
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Verifica célula à direita
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Verifica célula à esquerda
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # Método para comparação (usado pela PriorityQueue)
    def __lt__(self, other):
        return False


# Função heurística - calcula a distância Manhattan entre dois pontos
# Esta é a parte "A" do A* - estima o custo restante até o destino
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Traça o caminho encontrado, do fim ao início
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


# Implementação do algoritmo A*
def algorithm(draw, grid, start, end):
    count = 0
    # Fila de prioridade para selecionar o próximo nó a explorar
    open_set = PriorityQueue()
    # Adiciona o nó inicial com prioridade 0
    open_set.put((0, count, start))
    # Dicionário para rastrear de onde viemos para cada nó
    came_from = {}
    
    # Inicializa g_score (custo do início até o nó)
    # Infinito para todos os nós, exceto o inicial
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    # Inicializa f_score (custo estimado total = g_score + heurística)
    # f_score = g_score + h_score
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # Conjunto auxiliar para verificar se um nó está no open_set
    open_set_hash = {start}

    # Loop principal do algoritmo
    while not open_set.empty():
        # Verifica eventos (como fechar a janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Obtém o nó com menor f_score da fila de prioridade
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Se chegamos ao fim, reconstrua o caminho
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()  # Mantenha o destino visível
            return True

        # Explore os vizinhos do nó atual
        for neighbor in current.neighbors:
            # Custo para chegar ao vizinho passando pelo nó atual
            # (assumindo custo 1 para cada movimento)
            temp_g_score = g_score[current] + 1

            # Se encontramos um caminho melhor para este vizinho
            if temp_g_score < g_score[neighbor]:
                # Atualize as informações para este vizinho
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # Adicione à fila para explorar posteriormente se ainda não estiver lá
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # Marque como aberto visualmente

        # Redesenha o grid para mostrar o progresso
        draw()

        # Marque o nó atual como fechado (já explorado)
        if current != start:
            current.make_closed()

    # Se chegamos aqui, não foi encontrado caminho
    return False


# Cria o grid de células
def make_grid(rows, width):
    grid = []
    gap = width // rows  # Tamanho de cada célula em pixels
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
        # Linhas horizontais
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            # Linhas verticais
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# Função para atualizar a visualização do grid
def draw(win, grid, rows, width):
    win.fill(WHITE)  # Limpa a tela

    # Desenha todas as células
    for row in grid:
        for spot in row:
            spot.draw(win)

    # Desenha as linhas da grade
    draw_grid(win, rows, width)
    pygame.display.update()  # Atualiza a tela


# Converte posição do mouse em coordenadas do grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# Função principal do programa
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
                
                # Se não há ponto inicial definido, define-o
                if not start and spot != end:
                    start = spot
                    start.make_start()
                # Se há ponto inicial mas não ponto final, define-o
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                # Se ambos já estão definidos, cria barreiras
                elif spot != end and spot != start:
                    spot.make_barrier()

            # Clique direito do mouse (reset de células)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                # Remove o ponto inicial ou final se clicado
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # Teclas do teclado
            if event.type == pygame.KEYDOWN:
                # Tecla ESPAÇO inicia o algoritmo
                if event.key == pygame.K_SPACE and start and end:
                    # Atualiza os vizinhos de cada célula antes de iniciar
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # Executa o algoritmo A*
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Tecla C limpa o grid
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

# Inicia o programa
main(WIN, WIDTH)