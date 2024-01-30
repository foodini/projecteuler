all: 0044 0144 0139

0044: 0044.cpp util.o
	g++ -o 0044 0044.cpp util.o

0139: 0139.cpp
	g++ -o 0139 0139.cpp

0144: 0144.cpp util.h
	g++ -o 0144 0144.cpp

util.o: util.h util.cpp
	g++ -c -o util.o util.cpp
