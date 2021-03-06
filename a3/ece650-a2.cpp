// Compile with c++ ece650-a2cpp -std=c++11 -o ece650-a2
#include <iostream>
#include <sstream>
#include <vector>
#include <queue>
#include <regex>

using namespace std;

typedef unsigned int num;

class Graph {
private:

    vector<vector<num>> adj;

    // Function: bfs() : do breadth first search from src to dest
    // src: the source node
    // dest: the destination node
    // traversed: the traversed path of length v, assume -1 at the beginning.
    // return: whether a path can be established
    bool bfs(num src, num dest, vector<num> & traversed) {
        queue<num> que;
        vector<num> visited(v + 1, 0);
        visited[src] = true;
        que.push(src);

        while(!que.empty()) {
            num u = que.front();
            que.pop();
            // cout << "first " <<u << ", size " << adj.size() << endl;

            for (auto block: adj[u]) {
                // cout << " later block "<< block << endl;
                if (visited[block] == 0) {
                    visited[block] = 1;
                    traversed[block] = u;
                    que.push(block);

                    if (block == dest) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

public:
    num v;
    explicit Graph(num vertex_num) {
        v = 0;
        init(vertex_num);
    }

    void init(num vertex_num) {
        v = vertex_num;
        // cout << "new v" << v << endl;
        adj = vector<vector<num>>(v + 1, vector<num>());
        // showGraph();
    }

    void init() {
        // cout << "new v" << v << endl;
        adj = vector<vector<num>>(v + 1, vector<num>());
        // showGraph();
    }
//    void showBasic() const {
//        cout << "v " <<v <<endl;
//    }


    bool addEdge(num src, num dest) {
        // cout << src << " " << dest << " " << this->v << endl;
        if (src < 1 || src > v || dest < 1 || dest > v || src == dest) {
            return false;
        }
        adj[src].push_back(dest);
        adj[dest].push_back(src);
        return true;
    }

//    void showGraph() {
//        cout << "V: " << v << endl;
//        for (num i = 0; i < adj.size();i++) {
//            cout << "Node #" << i <<": ";
//            vector<num> roads = adj[i];
//            for (auto i: roads) {
//                cout << to_string(i) + " ";
//            }
//            cout << endl;
//        }
//    }

    string shortestDest(num src, num dest) {
        // showGraph();
        num negative = -1; //
        vector<num> traverse(v + 1, negative);
        if (src < 1 || src > v || dest < 1 || dest > v || src == dest) {
            return "Error: source and destination out of bound";
        }
        if (src == dest) {
            return to_string(src);
        }
        bool found = false;
        try {
            found = bfs(src, dest, traverse);
        } catch (exception & e) {
            cerr << e.what() << endl;
        }
        if (!found) {
            return "Error: a path does not exist between node<"
                   + to_string(src) + "> and node<" + to_string(dest) + ">" ;
        }
        vector<num> path;
        num next = dest;
        path.push_back(next);
        string res = to_string(dest);

        while (traverse[next] != negative) {
            res =  res.insert(0, to_string(traverse[next]) + '-');
            next = traverse[next];
        }
        return res;
    }
};


vector<pair<num,num>> parse(string s) {
    pair<num, num> edge;
    vector<pair<num,num> > result;

    try {
        regex re("-?[0-9]+"); // match numbers
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
        cout << "Error: cannot parse coordinates input" << endl;
        result.clear();
        return result;
    }
    return result;
}


void runnable() {
    Graph graph(0);

    while (!cin.eof()) {
        string line;
        getline(cin, line);
        istringstream input(line);


        while (!input.eof()) {
            char cmd;
            // parse a number
            input >> cmd;
            if (input.fail()) {
                // cerr << "Error command";
                break;
            }
            // cout << "command: " << cmd << endl;

            if (cmd == 'V') {
                num ver_num = 0;
                input >> ver_num;
                if (ver_num < 0 ) {
                    cout << "Error: V smaller than 0" << endl;
                }
                graph.init(ver_num);
                // cout << cmd << " " << ver_num << endl;
                // graph.showBasic();
                break;
            } else if (cmd == 'E') {
                string raw_ver;
                input >> raw_ver;
                vector<pair<num, num>> edge = parse(raw_ver);
                // cout << cmd << " " << raw_ver << endl;
                bool all_good = true;
                for (auto p: edge) {
                    if (!graph.addEdge(p.first, p.second)) {
                        // cout << "Error: The edge <" << p.first << "," << p.second
                            // << "> is out of the bound and cannot be added" << endl;
                        graph.init();
                        all_good = false;
                        break;
                    }
                }
                if (all_good) {
                    cout << "V " << graph.v << endl;
                    cout << "E " << raw_ver << endl;
                }

                break;
            } else if (cmd == 's') {
                num src, dest;
                input >> src >> dest;
                // cout << "cmd:" << cmd << ", src:" << src << ", dest:" << dest << endl;

                string answer = graph.shortestDest(src, dest);
                cout << answer << endl;
                break;
            } else {
                cout << "Error: the command is invalid " << cmd << endl;
                break;
            }
        }
        // cout << "newCycle" << endl;
    }
}

int main() {
    runnable();
    return 0;
}
