#include <iostream>
#include <iostream>
#include <vector>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

using namespace std;
typedef pid_t Pid;

int main (int argc, char **argv) {
    vector<Pid> children;

    int rgenToA1[2], a1ToA2[2];
    pipe(rgenToA1);
    pipe(a1ToA2);

    Pid pRgen, pA1, pA2;

    pRgen = fork();
    cout << "After pRgen: " <<pRgen << endl; // split into two process here

    pA1 = fork();
    cout << "After pA1: " << pA1 << endl; // split into two process here
    return 0;
}
