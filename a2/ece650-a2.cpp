// Compile with c++ ece650-a2cpp -std=c++11 -o ece650-a2
#include <iostream>
#include <sstream>
#include <vector>
#include <queue>
#include <algorithm>
#include <regex>

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
        if (src < 1 || src > v || dest < 1 || dest > v || src == dest) {
            return false;
        }
        adj[src].push_back(dest);
        adj[src].push_back(src);
        return true;
    }

    bool bfs(int src, int dest, int v, int pred[]) {
//        queue<int> que;
//        bool visited[v];
//        fill_n(pred, v, -1);
//        visited[src];
        return false;
    }
};


vector<pair<int,int>> parse(string s) {
    pair<int, int> edge;
    vector<pair<int,int> > result;

    // using regex
    try {
        regex re("-?[0-9]+"); //match consectuive numbers
        sregex_iterator next(s.begin(), s.end(), re);
        sregex_iterator end;
        while (next != end) {
            smatch match1;
            smatch match2;

            match1 = *next;
            next++;
            // iterate to next match
            if (next != end) {
                match2 = *next;
                edge.first = stoi(match1.str());
                edge.second = stoi(match2.str());
                result.push_back(edge);
                next++;
            }
        }
    }
    catch (regex_error& e) {
        result.clear();
    }
    return result;
}

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
                vector<pair<int, int>> edge = parse(raw_ver);
                cout << cmd <<" " << raw_ver << endl;
                for (auto p: edge) {
                    graph.addEdge(p.first, p.second);
                }
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
