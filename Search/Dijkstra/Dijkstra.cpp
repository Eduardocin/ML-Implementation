#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <utility>

using namespace std;

class Edge {
private:
    int destination;
    int weight;

public:
    Edge(int dest, int w) : destination(dest), weight(w) {}

    // Getters
    int getDestination() const { return destination; }
    int getWeight() const { return weight; }
};

// Classe Vertex (Vértice) para armazenar informações sobre um vértice
class Vertex {
private:
    vector<Edge> edges;
    bool visited;

public:
    Vertex() : visited(false) {}

    void addEdge(int destination, int weight) {
        edges.push_back(Edge(destination, weight));
    }

    const vector<Edge>& getEdges() const { return edges; }

    // Métodos para manipular o estado de visitação
    bool isVisited() const { return visited; }
    void setVisited(bool state) { visited = state; }
    void resetVisited() { visited = false; }
};

// Classe Graph (Grafo) para gerenciar o grafo e aplicar algoritmos
class Graph {
private:
    vector<Vertex> vertices;
    int numEdges;

public:
    Graph(int numVertices) : vertices(numVertices), numEdges(0) {}

    void addEdge(int source, int destination, int weight) {
        vertices[source].addEdge(destination, weight);
        numEdges++;
    }

    int getSize() const {
        return vertices.size();
    }

    void resetVisited() {
        for (auto& vertex : vertices) {
            vertex.resetVisited();
        }
    }

    // Estrutura para o retorno do algoritmo de Dijkstra
    struct DijkstraResult {
        vector<int> distances;
        vector<int> previousVertices;
    };

    // Algoritmo de Dijkstra para encontrar o caminho mais curto
    DijkstraResult dijkstra(int startVertex) {
        /*
        1. Inicializar as distâncias para todos os vértices como infinito (INT_MAX)
        2. Inicializar o vetor de vértices anteriores como -1 (sem predecessores)
        3. Criar uma fila de prioridade para selecionar o próximo vértice a ser processado
        4. Definir a distância do vértice inicial como 0
        5. Inserir o vértice inicial na fila de prioridade
        6. Marcar todos os vértices como não visitados
        7. Enquanto houver vértices não visitados:
           a. Extrair o vértice com menor distância da fila
           b. Marcar o vértice como visitado
           c. Atualizar seu predecessor no caminho
           d. Para cada vizinho não visitado, atualizar sua distância se encontrar um caminho mais curto
        8. Retornar as distâncias mínimas e os vértices anteriores
        */
        
        vector<int> distances(getSize(), INT_MAX);
        vector<int> previous(getSize(), -1);
        using QueueElement = pair<int, pair<int, int>>;
        priority_queue<QueueElement, vector<QueueElement>, greater<QueueElement>> pq;
        
        distances[startVertex] = 0;
        pq.emplace(0, make_pair(startVertex, startVertex));
        
        resetVisited();
        
        for (int i = 0; i < getSize(); i++) {
            int currentVertex, prevVertex;
            
            /*
            1. Extrair o próximo vértice não visitado com menor distância
            2. Se a fila estiver vazia, terminar o processamento
            3. Continuar extraindo vértices até encontrar um não visitado
            */
            do {
                if (pq.empty()) {
                    // Impossível alcançar mais vértices
                    return {distances, previous};
                }
                
                auto current = pq.top();
                pq.pop();
                currentVertex = current.second.first;
                prevVertex = current.second.second;
                
            } while (vertices[currentVertex].isVisited());
            
            // Marcar como visitado e atualizar o caminho
            vertices[currentVertex].setVisited(true);
            previous[currentVertex] = prevVertex;
            
            /*
            1. Para cada aresta saindo do vértice atual:
            2. Obter o vértice vizinho e o peso da aresta
            3. Verificar se o vizinho não foi visitado
            4. Verificar se o caminho atual + peso da aresta é menor que a distância conhecida
            5. Se for menor, atualizar a distância e adicionar à fila de prioridade
            */
            for (const auto& edge : vertices[currentVertex].getEdges()) {
                int neighbor = edge.getDestination();
                int weight = edge.getWeight();
                
                if (!vertices[neighbor].isVisited() && distances[neighbor] > distances[currentVertex] + weight) {
                    distances[neighbor] = distances[currentVertex] + weight;
                    pq.emplace(distances[neighbor], make_pair(neighbor, currentVertex));
                }
            }
        }
        
        return {distances, previous};
    }
};
