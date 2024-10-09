all: 0044 0139 0144 0351

clean:
	rm *.o 0044 0139 0144 0351

util.o: util.h util.cpp
	g++ -c -o util.o util.cpp

0044: 0044.cpp util.o
	g++ -o 0044 0044.cpp util.o

0139: 0139.cpp
	g++ -o 0139 0139.cpp

0144: 0144.cpp util.o
	g++ -o 0144 0144.cpp

0351: 0351.cpp util.o
	g++ -o 0351 0351.cpp util.o
