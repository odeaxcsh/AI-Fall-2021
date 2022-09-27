# set gcc standard to c++20
# and -Wall -Wextra -Wpedantic -Werror
flags = -std=c++20 -Wall -Wextra -Wpedantic -Werror 

# set include path to current directory
include = -I.

# libraries
libs = -lstdc++

all:
	g++ $(flags) $(include) $(libs) console.cpp -o console

win:
	g++ $(flags) $(include) $(libs) -o console.exe console.cpp

clean: 
	rm -f console

win-clean:
	del console.exe
