# Any tool that requires compilation should go here. The fewer, the better.

all: status_time wclive
	

status_time: status_time.c
	gcc -o status_time status_time.c
	cp status_time ..

wclive: wclive.cpp
	g++ -o wclive wclive.cpp
	cp wclive ..
