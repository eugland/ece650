rm -rf build
mkdir build
cd build
cmake ../
make install
pwd
cp ../ece650-a1.py .
./ece650-a3 -s 5 -n 4 -l 6 -c 21

