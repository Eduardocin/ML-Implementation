#include <iostream>
#include <vector>
#include <queue>
#include <set>
#include <cmath>
#include <algorithm>
#include <utility>

using namespace std;

class Node {
public:
    int x, y;
    int g;  // Custo do caminho do início até este nó
    int h;  // Valor heurístico (estimativa do custo até o objetivo)
    int f;  // Custo total (g + h)
    Node* parent;

    Node(int x, int y, int g = 0, int h = 0, Node* parent = nullptr)
        : x(x), y(y), g(g), h(h), f(g + h), parent(parent) {}

    // Operador de comparação para a fila de prioridade (min-heap)
    bool operator<(const Node& other) const {
        return f > other.f;  
    }
};

// Função heurística (Distância de Manhattan)
int heuristic(const pair<int, int>& current_pos, const pair<int, int>& goal_pos) {
    return abs(current_pos.first - goal_pos.first) + 
           abs(current_pos.second - goal_pos.second);
}

// Verifica se uma posição é válida e caminhável
bool isWalkable(const vector<vector<int>>& grid, int x, int y) {
    return x >= 0 && x < grid.size() && 
           y >= 0 && y < grid[0].size() && 
           grid[x][y] == 0;
}

// Algoritmo A*
vector<pair<int, int>> aStar(const vector<vector<int>>& grid, 
                             const pair<int, int>& start, 
                             const pair<int, int>& goal) {
    /*
    1. Inicializar a lista aberta (fila de prioridade) e a lista fechada (conjunto)
    2. Adicionar o nó inicial à lista aberta
    3. Enquanto a lista aberta não estiver vazia:
        a. Pegar o nó com menor f(n) da lista aberta
        b. Se o nó for o objetivo, reconstruir e retornar o caminho
        c. Mover o nó para a lista fechada
        d. Para cada vizinho do nó:
            i. Se o vizinho não é válido ou está na lista fechada, pular
            ii. Calcular o novo g(n) para este vizinho
            iii. Se o vizinho não está na lista aberta ou tem um g(n) maior,
                 atualizar suas informações e adicionar à lista aberta
    4. Se a lista aberta ficar vazia sem encontrar o objetivo, não há caminho
    */
    
    // Fila de prioridade para a lista aberta
    priority_queue<Node> open_list;
    
    // Conjunto para a lista fechada (nós já processados)
    set<pair<int, int>> closed_list;
    
    // Calcular a heurística para o nó inicial
    int start_h = heuristic(start, goal);
    
    // Criar e adicionar o nó inicial à lista aberta
    open_list.push(Node(start.first, start.second, 0, start_h));
    
    // Mapa para rastrear os nós na lista aberta para rápida verificação e atualização
    vector<vector<Node*>> node_map(grid.size(), vector<Node*>(grid[0].size(), nullptr));
    
    while (!open_list.empty()) {
        // Pegar o nó com menor f(n)
        Node current = open_list.top();
        open_list.pop();
        
        // Verificar se chegamos ao objetivo
        if (make_pair(current.x, current.y) == goal) {
            vector<pair<int, int>> path;
            Node* curr_ptr = new Node(current); // Cópia do nó atual
            
            while (curr_ptr) {
                path.push_back(make_pair(curr_ptr->x, curr_ptr->y));
                curr_ptr = curr_ptr->parent;
            }
            
            reverse(path.begin(), path.end());
            
            for (auto& row : node_map) {
                for (auto& node_ptr : row) {
                    delete node_ptr;
                }
            }
            
            return path;
        }
        
        closed_list.insert(make_pair(current.x, current.y));
        
        const int dx[] = {-1, 0, 1, 0};
        const int dy[] = {0, 1, 0, -1};
        
        // Verificar todos os vizinhos
        for (int i = 0; i < 4; i++) {
            int neighbor_x = current.x + dx[i];
            int neighbor_y = current.y + dy[i];
            pair<int, int> neighbor_pos = make_pair(neighbor_x, neighbor_y);
            
            // Verificar se o vizinho é válido e não está na lista fechada
            if (!isWalkable(grid, neighbor_x, neighbor_y) || 
                closed_list.find(neighbor_pos) != closed_list.end()) {
                continue;
            }
            
            // Calcular o novo g(n)
            int g = current.g + 1;
            
            // Calcular h(n)
            int h = heuristic(neighbor_pos, goal);
            
            // Verificar se já existe na lista aberta
            bool skip = false;
            
            if (node_map[neighbor_x][neighbor_y]) {
                // Se o novo caminho é pior, ignorar
                if (node_map[neighbor_x][neighbor_y]->g <= g) {
                    skip = true;
                } else {
                    // Caso contrário, vamos atualizar este nó
                    // Precisamos removê-lo e adicionar novamente à lista aberta
                    delete node_map[neighbor_x][neighbor_y];
                    node_map[neighbor_x][neighbor_y] = nullptr;
                }
            }
            
            if (!skip) {
                // Criar um novo nó e adicionar à lista aberta
                Node* parent_copy = new Node(current);
                Node* new_node = new Node(neighbor_x, neighbor_y, g, h, parent_copy);
                node_map[neighbor_x][neighbor_y] = new_node;
                open_list.push(*new_node);
            }
        }
    }
    
    // Não encontrou caminho
    return vector<pair<int, int>>();
}

int main() {
    // Grid de exemplo: 0 = caminhável, 1 = obstáculo
    vector<vector<int>> grid = {
        {0, 0, 0, 1, 0},
        {0, 1, 0, 1, 0},
        {0, 1, 0, 0, 0},
        {0, 0, 0, 1, 0},
        {1, 0, 0, 0, 0}
    };
    
    pair<int, int> start(0, 0);
    pair<int, int> goal(4, 4);
    
    vector<pair<int, int>> path = aStar(grid, start, goal);
    
    cout << "Caminho encontrado com A*: ";
    if (path.empty()) {
        cout << "Nenhum caminho encontrado!" << endl;
    } else {
        for (const auto& pos : path) {
            cout << "(" << pos.first << "," << pos.second << ") ";
        }
        cout << endl;
        
        // Mostrar o grid com o caminho
        cout << "\nGrid com o caminho (X = caminho, # = obstáculo, . = espaço livre):\n";
        for (int i = 0; i < grid.size(); i++) {
            for (int j = 0; j < grid[i].size(); j++) {
                if (grid[i][j] == 1) {
                    cout << "# ";
                } else {
                    bool in_path = false;
                    for (const auto& pos : path) {
                        if (pos.first == i && pos.second == j) {
                            in_path = true;
                            break;
                        }
                    }
                    cout << (in_path ? "X " : ". ");
                }
            }
            cout << endl;
        }
    }
    
    return 0;
}