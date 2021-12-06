// Compile with c++ ece650-a2cpp -std=c++11 -o ece650-a2
#include <iostream>
#include <sstream>
#include <vector>
#include <queue>
#include <regex>
#include "minisat/core/SolverTypes.h"
#include "minisat/core/Solver.h"

using namespace std;


class Graph {
public:
    int vertex_int;
    vector<pair<int, int>> edges;

    explicit Graph(int vint) {
        vertex_int = 0;
        vertex_int = vint;
    }

    void init(int vint) {
        vertex_int = vint;
        edges = vector<pair<int, int>>();
    }

    void init() {
        vertex_int = 0;
        edges = vector<pair<int, int>>();
    }

    bool addEdge(int src, int dest) {
        if (src < 1 || src > vertex_int || dest < 1 || dest > vertex_int || src == dest) {
            return false;
        }
        edges.push_back(make_pair(src, dest));
        return true;
    }

    // consulted online sources https://github.com/thapliyal28/Analysis-of-vertex-cover-algorithms.
    void calc_vertex_cover() {
        std::unique_ptr<Minisat::Solver> solver(new Minisat::Solver());

        int n = vertex_int;
        // k - number of vertex-cover
        for (int k = 1; k <= n; ++k) {
            // create literals
            Minisat::vec<Minisat::Lit> lits; // n * k
            for (int i = 0; i < n * k; ++i) {
                lits.push(Minisat::mkLit(solver->newVar()));
            }

            // create clause
            for (int j = 0; j < k; ++j) {
                Minisat::vec<Minisat::Lit> v;
                for (int i = 0; i < n; ++i) {
                    v.push(lits[i * k + j]);
                }
                solver->addClause(v);
            }

            // 2. No one vertex can appear twice in a vertex cover
            for (int i = 0; i < n; ++i) {
                for (int p = 0; p < k - 1; ++p) {
                    for (int q = p + 1; q < k; ++q) {
                        solver->addClause(~lits[i * k + p], ~lits[i * k + q]);
                    }
                }
            }

            // 3. no more vertex in same position in cover
            for (int p = 0; p < n - 1; ++p) {
                for (int q = p + 1; q < n; ++q) {
                    for (int j = 0; j < k; ++j) {
                        solver->addClause(~lits[p * k + j], ~lits[q * k + j]);
                    }
                }
            }


            // 4. each edge contains one in vertex cover
            for (pair<int, int> &edge: edges) {
                Minisat::vec<Minisat::Lit> v;
                for (int p = 0; p < k; ++p) {
                    v.push(lits[(edge.first - 1) * k + p]);
                    v.push(lits[(edge.second - 1) * k + p]);
                }
                solver->addClause(v);
            }

            bool res = solver->solve();
            if (res) // satisfiable
            {
                // check model with Literals
                std::vector<int> cover;
                for (int i = 0; i < n; ++i) {
                    for (int j = 0; j < k; ++j) {
                        if (solver->modelValue(lits[i * k + j]) == Minisat::l_True) {
                            cover.push_back(i + 1);
                            break;
                        }
                    }
                    if (cover.size() == k) {
                        break;
                    }
                }

                // sort
                std::sort(cover.begin(), cover.end());
                // output the result
                for (int i = 0; i < cover.size(); ++i) {
                    std::cout << cover[i] << " ";
                }
                solver.reset();
                break;
            }
            solver.reset(new Minisat::Solver());
        }
        cout << endl;
    }
};


vector<pair<int,int>> parse(string s) {
    pair<int, int> edge;
    vector<pair<int,int> > result;

    try {
        regex re("-?[0-9]+"); // match intbers
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
            // parse a intber
            input >> cmd;
            if (input.fail()) {
                // cerr << "Error command";
                break;
            }
            // cout << "command: " << cmd << endl;

            if (cmd == 'V') {
                int ver_int = 0;
                input >> ver_int;
                if (ver_int < 0 ) {
                    cout << "Error: V smaller than 0" << endl;
                }
                graph.init(ver_int);
                // cout << cmd << " " << ver_int << endl;
                // graph.showBasic();
                break;
            } else if (cmd == 'E') {
                string raw_ver;
                input >> raw_ver;
                vector<pair<int, int>> edge = parse(raw_ver);
                // cout << cmd << " " << raw_ver << endl;
                for (auto p: edge) {
                    bool isAdded = graph.addEdge(p.first, p.second);
                    if (!isAdded) {
                        cout << "Error: The edge <" << p.first << "," << p.second
                             << "> is out of the bound and cannot be added" << endl;
                        graph.init();
                        break;
                    }
                }
                graph.calc_vertex_cover();
                break;
            } else {
                cout << "Error: the command is invalid " << cmd << endl;
                break;
            }
        }
    }
}

int main() {
    runnable();
    return 0;
}