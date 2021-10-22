// Compile with c++ ece650-a2cpp -std=c++11 -o ece650-a2
#include <iostream>
#include <sstream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

class Graph {
public:
    int v;
    vector<vector<int>> adj;



    Graph(int vertex_num) {
        v = vertex_num;
        adj = vector<vector<int>>(v, vector<int>());
    }

    bool addEdge(int src, int dest) {
        adj[src].push_back(dest);
        adj[src].push_back(src);
        return false;
    }

    bool bfs(int src, int dest, int v, int pred[]) {
//        queue<int> que;
//        bool visited[v];
//        fill_n(pred, v, -1);
//        visited[src];
        return false;
    }
};


int main(int argc, char** argv) {

    // read and display init arguments
    cout << "Called with " << argc << " arguments\n";
    for (int i = 0; i < argc; ++i) {
        cout << "Arg " << i << " is " << argv[i] << "\n";
    }

    // separator character
    const char comma = ',';

    while (!cin.eof()) {
        string line;
        getline(cin, line);
        istringstream input(line);

        vector<unsigned> nums;
        Graph graph(0);

        while (!input.eof()) {
            char cmd;
            // parse an integer
            input >> cmd;
            if (input.fail()) {
                // cerr << "Error command";
                break;
            }
            cout << "command: " <<cmd << endl;

            if (cmd == 'V') {
                unsigned int ver_num;
                input >> ver_num;
                graph = Graph(ver_num);
                cout << cmd << " " << ver_num << endl;
                break;
            } else if (cmd == 'E') {
                string raw_ver;
                input >> raw_ver;
                cout << cmd <<" " << raw_ver << endl;
                break;
            } else if (cmd == 's') {
                unsigned int src, dest;
                input >> src >> dest;
                cout << cmd << " " << src << " " << dest << endl;
                break;
            } else {
                cout << "Error: the command is invalid " << cmd << endl;
                break;
            }
        }
        cout << "newCycle" <<endl;
    }
}
