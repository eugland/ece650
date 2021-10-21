// Compile with c++ ece650-a2cpp -std=c++11 -o ece650-a2
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

int main(int argc, char** argv) {
    // Test code. Replaced with your code

    // Print command line arguments that were used to start the program
    cout << "Called with " << argc << " arguments\n";
    for (int i = 0; i < argc; ++i) {
        cout << "Arg " << i << " is " << argv[i] << "\n";
    }

    // separator character
    const char comma = ',';

    // read from stdin until EOF
    while (!cin.eof()) {
        cout << "Enter numbers separated by comma: ";

        // read a line of input until EOL and store in a string
        string line;
        getline(cin, line);

        // create an input stream based on the line
        // we will use the input stream to parse the line
        istringstream input(line);

        // we expect each line to contain a list of numbers
        // this vector will store the numbers.
        // they are assumed to be unsigned (i.e., positive)
        vector<unsigned> nums;

        // while there are characters in the input line
        while (!input.eof()) {
            unsigned num;
            // parse an integer
            input >> num;
            if (input.fail()) {
                cerr << "Error parsing a number\n";
                break;
            } else
                nums.push_back(num);

            // if eof bail out
            if (input.eof()) break;

            // read a character
            // Note that whitespace is ignored
            char separator;
            input >> separator;

            // if error parsing, or if the character is not a comma
            if (input.fail() || separator != comma) {
                cerr << "Error parsing separator\n";
                break;
            }
        }

        // done parsing a line, print the numbers
        if (!nums.empty()) {
            cout << "\nYou have entered " << nums.size() << " numbers: ";
            size_t i = 0;
            for (unsigned x : nums) {
                cout << x;
                // print a comma if not the last number
                i++;
                if (i < nums.size()) cout << ",";
            }
        }
        cout << endl;
    }
}
