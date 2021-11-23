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
    // cout << "arguments: ";
//    for (int i = 0; i < argc; i++) {
//        cout << argv[i] << " ";
//    }
    cout << endl;


    vector<Pid> children;

    int rgenToA1[2], a1ToA2[2];
    pipe(rgenToA1);
    pipe(a1ToA2);

    Pid pRgen, pA1, pA2;

    pRgen = fork();
    // cout << "After pRgen: " <<pRgen << endl; // split into two process here
    if (pRgen == 0) {
        // cout << "pRgen in" <<endl;
        // pipe stdout to rgenToA1
        dup2(rgenToA1[1], STDOUT_FILENO);
        close(rgenToA1[0]);
        close(rgenToA1[1]);
        close(a1ToA2[0]);
        close(a1ToA2[1]);

        // cout << "pRgen piped" <<endl;
        // run the sub task
        // cout << "new args: ";
        char *args[] = {(char *) "./rgen", (char *) "-l h", nullptr};
        if (execv(args[0], args) == -1 ) {
            cerr << "rengen exec failed " << endl;
            cerr << strerror(int errno) << "\n";
        }
    }
    children.push_back(pRgen);


    pA1 = fork();
    if (pA1 == 0) {
        dup2(rgenToA1[0], STDIN_FILENO);
        dup2(a1ToA2[1], STDOUT_FILENO);
        close(rgenToA1[0]);
        close(rgenToA1[1]);
        close(a1ToA2[0]);
        close(a1ToA2[1]);

        char * args[] = { (char *) "./ece650-a1.py", nullptr };
        execv(args[0], args);
    }
    children.push_back(pA1);


    pA2 = fork();
    if (pA2 == 0) {
        dup2(a1ToA2[0], STDIN_FILENO);
        close(rgenToA1[0]);
        close(rgenToA1[1]);
        close(a1ToA2[0]);
        close(a1ToA2[1]);

        char *args[] = { (char *) "./ece650-a2", nullptr };
        if (execv(args[0], args) == -1){
            cout << "a2 failed " << endl;
            cerr << strerror(int errno) << "\n";
            abort();
        }
    }
    children.push_back(pA2);

    // finally, redirect a2 stdout to the pipe
    dup2(a1ToA2[1], STDOUT_FILENO);
    close(rgenToA1[0]);
    close(rgenToA1[1]);
    close(a1ToA2[0]);
    close(a1ToA2[1]);

    while(!cin.eof()){
        string input;
        getline(cin,input);
        cout << input << endl;
    }

    // send kill signal to all children
    for (pid_t k: children){
        int status;
        kill(k, SIGTERM);
        waitpid(k, &status, 0);
    }

    return 0;
}
