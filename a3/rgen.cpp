//
// Created by eugen on 2021-11-21.
#include <iostream>
#include <fstream>
#include <vector>
#include <unistd.h>
#include <limits>
#include <algorithm>

using namespace std;


int randint(int min, int max) {
    if (min == max) {
        return min;
    }
    unsigned int num;
    ifstream urandom("/dev/urandom");
    urandom.read((char *) &num, sizeof(num));
    urandom.close();
    return num % (max - min + 1) + min;
}

// are_zero_line_segment basically check if x=x and y=y of two points.
bool isPoint(vector<int> p1, vector<int> p2) {
    return p1[0] == p2[0] and p1[1] == p2[1];
}

// is_intersection_on_line_segment check if a point is on a line
bool isPointOnLine(vector<int> l1, vector<int> l2, vector<double> p) {
    vector<int> x { l1[0], l2[0] };
    vector<int> y { l1[1], l2[1] };
    sort(x.begin(), x.end());
    sort(y.begin(), y.end());

    // cout << x[0] << x[1] << y[0] << y[1] << endl; // output to see if the assignment works
    return x[0] <= p[0] && p[0] <= x[1] && y[0] <= p[1] && p[1] <= y[1];
}

bool areOverlapping(vector<int> p1, vector<int> p2, vector<int> p3, vector<int> p4) {
    int x1, y1, x2, y2, x3, y3, x4, y4;

    // no k can be calculated
    if (p1[0] == p2[0] and p3[0] == p4[0] and p1[0] == p3[3]) {
        y1 = p2[1], y2 = p1[1];
        if (p1[1] < p2[1]) swap(y1, y2);
        y3 = p4[1], y4 = p3[1];
        if (p3[1] < p4[1]) swap(y3, y4);

        if ((y1 <= y3 and y3 < y2) or
                (y1 < y4 and y4 <= y2) or
                (y3 <= y1 and y1 < y4) or
                (y3 < y2 and y2 <= y4)) return true;
    }
    // k exist here
    if (p1[0] != p2[0] and p3[0] != p4[0]) {
        x1 = p2[0], y1 = p2[1], x2 = p1[0], y2 = p1[1];
        if (p1[0] < p2[0]) {
            swap(y1, y2);
            swap(x1, x2);
        }
        x3 = p4[0], y3 = p4[1], x4 = p3[0], y4 = p3[1];
        if (p3[0] < p4[0]) {
            swap(x3, x4);
            swap(y3, y4);
        }
        double k1 = (y2 - y1);
        k1 = k1 / (x2 - x1);
        double k2 = (y4 - y3);
        k2 = k2 / (x4 - x3);
        double b1 = (x2*y1 - x1 * y2);
        b1 = b1 / (x2 - x1);
        double b2 = (x4 * y3 -x3 * y4);
        b2 = b2 / (x4 - x3);
        if ((k1 == k2 and b1 == b2) and
            ((x1 <= x3 and x3 < x2) or (x1 < x4 and x4 <= x2) or (x3 <= x1 and x1 < x4) or (x3 < x2 and x2 <= x4))
        ) {
            return true;
        }
    }
    return false;
}


bool areLineIntersecting(vector<int> p1, vector<int> p2, vector<int> p3, vector<int> p4) {
    int x1 = p1[0], y1 = p1[1], x2 = p2[0], y2 = p2[1];
    int x3 = p3[0], y3 = p3[1], x4 = p4[0], y4 = p4[1];

    if (p1[0] == p2[0] and p3[0] != p4[0]) {
        double k2 = (y4 - y3);
        k2 = k2 / (x4 - x3);
        double b2 = (x4 * y3 - x3 * y4);
        b2 = b2 / (x4 - x3);

        double y_is = k2 * x1 + b2;
        vector<double> intersect { static_cast<double>(x1), y_is };
        if (isPointOnLine(p1, p2, intersect) and isPointOnLine(p3, p4, intersect)) {
            return true;
        }
    }

    if (p1[0] != p2[0] and p3[0] == p4[0]) {
        double k1 = (y2 - y1);
        k1 = k1 / (x2 - x1);
        double b1 = (x2 * y1 - x1 * y2);
        b1 = b1 / (x2 - x1);

        double y_is = k1 * x3 + b1;
        vector<double> intersect { static_cast<double>(x3), y_is };
        if (isPointOnLine(p1, p2, intersect) and isPointOnLine(p3, p4, intersect)) {
            return true;
        }
    }

    if (p1[0] != p2[0] and p3[0] != p4[0]) {
        double k1 = (y2 - y1);
        k1 = k1 / (x2 - x1);
        double b1 = (x2 * y1 - x1 * y2);
        b1 = b1 / (x2 - x1);
        double k2 = (y4 - y3);
        k2 = k2 / (x4 - x3);
        double b2 = (x4 * y3 - x3 * y4);
        b2 = b2 / (x4 - x3);

        if (k1 != k2) {
            double x_ist=(b2-b1);
            x_ist = x_ist/(k1-k2);
            double y_ist=(k1*b2-k2*b1);
            y_ist = y_ist/(k1-k2);

            vector<double> intersect { x_ist, y_ist };
            if (isPointOnLine(p1, p2, intersect) and isPointOnLine(p3, p4, intersect)) {
                return true;
            }
        }

    }
    return false;

}



void unitTest() {
    // testing randint
    cout << "randint(0,2): ";
    for (int i = 0; i < 10; i ++) {
        cout << randint(0, 2) << " ";
    }
    cout << endl;

    //testing same point
    vector<int> a = {1,2};
    vector<int> b = {1,2};
    cout << "is same point {1,2} and {1,2}: " << isPoint(a, b) << endl;
    b[1] = 1;
    cout << "is same point {1,2} and {1,1}: " << isPoint(a, b) << endl;


    // test isPointOnLine
    vector<int> la = {0,0};
    vector<int> lb = {3,3};
    vector<double> p = {2,2};
    cout << "point is on line: " << isPointOnLine(la, lb, p) << endl;
    p[0]=4;
    cout << "point is on line: " << isPointOnLine(la, lb, p) << endl;
}

int main (int argc, char *argv[]) {
    int option;
    string s_com, n_com, l_com, c_com;
    int s = 10, n = 5, l = 5, c = 20;

    while ((option=getopt(argc, argv, "s:n:l:c:")) != -1){
        int number = stoi(optarg);
        if (option == 's') s = number;
        else if (option == 'n') n = number;
        else if (option == 'l') l = number;
        else if (option == 'c') c = number;
    }
    // cout << s << " " << n << " " << l << " " << c << endl;

    vector<string> street_list;
    bool flag = true;
    while (flag) {
        int st_id = 1;
        int st_num = randint(2, s);
        int wait_num = randint(5, l);

        vector<vector<vector<int>>> graph;

        while (st_id <= st_num) {
            int n_num = randint(1, n);
            vector<vector<int>> street;

            int n_id = 1;

            while (n_id <= n_num + 1) {
                vector<int> points;
                points.push_back(randint(-c, c));
                points.push_back(randint(-c, c));

                if (!street.empty()) {
                    int flag = 0, count = 0;
                    while(!flag) {
                        count ++;
                        if (count > 25) {
                            cerr << "Error: failed after 25 attempts at generating" << endl;
                            exit(1);
                        }
                        points[0] = randint(-c, c);
                        points[1] = randint(-c, c)};

                        // check if two points are the same, so no meaningful line segement
                        if (!isPoint(points, street.back())) {
                            flag ++;
                        }

                        if (street.size() > 1) {
                            for (int i = 0; i < street.size() - 1; i++) {

                            }
                        }
                    }
                }
            }
        }

    }


    // unitTest();

    return 0;
}