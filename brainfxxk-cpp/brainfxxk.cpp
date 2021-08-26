#include <cstdio>
#include <cstdlib>
#include <stack>
#include <vector>
#include <cstring>

using namespace std;

void yyerror(char* msg){
	fprintf(stderr, "%s\n", msg);
	exit(-1);
}

void op_lt();		// <
void op_rt();		// >
void op_plus();		// +
void op_minus();	// -
void op_lp();		// [
void op_rp();		// ]
void op_comma();	// ,
void op_dot();		// .

void printstate();

int ip = 0;
int sp = 0;

char mem[1024] = { 0, };
char buf[65536] = { 0, };
int len = 0;
stack<int> jump_index;
vector<char> out;

int main(){
	scanf("%65535s", buf);
	getchar();
	len = strlen(buf);
	for(ip = 0; ip < len; ip++){
		switch(buf[ip]){
			case '>':
				op_rt();
				break;
			case '<':
				op_lt();
				break;
			case '+':
				op_plus();
				break;
			case '-':
				op_minus();
				break;
			case '.':
				op_dot();
				break;
			case ',':
				op_comma();
				break;
			case '[':
				op_lp();
				break;
			case ']':
				op_rp();
				break;
			case ' ':
			case '\n':
			case '\t':
				break;
			default:
			yyerror("Invalid token");
		}
		printstate();
	}

	printf("OUTPUT ::\n");
	for(char x : out){
		putchar(x);
	}
	return 0;
}

void op_lt(){
	sp--;
}
void op_rt(){
	sp++;
}
void op_plus(){
	mem[sp]++;
}
void op_minus(){
	mem[sp]--;
}
void op_lp(){
	if(mem[sp] == 0){
		while(buf[ip] != ']'){
			ip++;
			if(ip >= len) yyerror("Syntax Error :: \']\' missing");
		}
	}
	else{
		jump_index.push(ip);
	}
}
void op_rp(){
	if(mem[sp] != 0){
		ip = jump_index.top();
	}
	else{
		jump_index.pop();
	}
}
void op_comma(){
	mem[sp] = getchar();
}
void op_dot(){
	printf("OUTPUT : %c\n", mem[sp]);
	out.push_back(mem[sp]);
}

void printstate(){
	int esp = sp < 7 ? 0 : sp-7;
	int eip = ip < 7 ? 0 : ip-7;

	
	printf("\tInst\t\t      Memory\n");
	printf("    ============\t=================\n");
	for(int i = 0; i < 8; i++){
		if(eip + i == ip){
			printf("    %4d:  * %c\t",eip+i, buf[eip+i]);
		}
		else{
			printf("    %4d:    %c\t",eip+i, buf[eip+i]);
		}

		if(esp + i == sp){
			printf("  #\t%x\n", mem[esp+i]);
		}
		else{
			printf("   \t%x\n", mem[esp+i]);
		}
	}
	printf("\n\n\t ip : %d, sp : %d\n", ip, sp);
	printf("====================================================================\n");

	getchar();
}