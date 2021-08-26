all: lex.yy.c nyan.cpp
	g++ -o nyan lex.yy.cpp nyan.cpp
lex.yy.c: nyan.l
	flex -o lex.yy.cpp nyan.l
clean:
	rm -rf *.yy.* *.o nyan *.hh