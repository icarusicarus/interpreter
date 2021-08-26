%option noyywrap
%{
	#include <stdio.h>
	#include "nyan.h"

	INST insts[1024];
	int pointer = 0;
	int ip = 0;
%}

%%
Ny[a]+n			{ 
					insts[pointer].T = INST_NYAN;
					insts[pointer].len = strlen(yytext)-3;
					pointer++;
				}
Ny[u]+n			{
					insts[pointer].T = INST_NYUN;
					insts[pointer].len = strlen(yytext)-3;
					pointer++;
				}
Me[o]+w			{ 
					insts[pointer].T = INST_MEOW;
					insts[pointer].len = strlen(yytext)-3;
					pointer++;
				}
M[o]+w			{ 
					insts[pointer].T = INST_MOW;
					insts[pointer].len = strlen(yytext)-2;
					pointer++;
				}
[.]+			{ 
					insts[pointer].T = INST_REP;
					insts[pointer].len = strlen(yytext);
					pointer++;
				}
His[s]+			{ 
					insts[pointer].T = INST_HISS;
					insts[pointer].len = strlen(yytext)-3;
					pointer++;
				}
Pur[r]+			{ 
					insts[pointer].T = INST_PURR;
					insts[pointer].len = strlen(yytext)-3;
					pointer++;
				}
Eh[.]+			{
					insts[pointer].T = INST_REPSTART;
					insts[pointer].len = strlen(yytext)-2;
					pointer++;
				}
\~				{
					insts[pointer].T = INST_REPEND;
					pointer++;
				}

[\t\n ]				{ }
%%

int main(){
	yylex();

	InitVector();

	for(ip = 0; ip  < pointer; ip++){
		INST it = insts[ip];
		fps[it.T](it);
		printState();
	}

	printf("OUTPUT: %s\n", out);

}