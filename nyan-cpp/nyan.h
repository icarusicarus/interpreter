typedef enum {
	INST_NOP = 0,
	INST_NYAN = 1,
	INST_NYUN = 2,
	INST_MEOW = 3,
	INST_MOW = 4,
	INST_REP = 5,
	INST_HISS = 6,
	INST_PURR = 7,
	INST_REPSTART = 8,
	INST_REPEND = 9
} InstType;


typedef struct instruction {
	InstType T;
	int len;
} INST, *PINST;

typedef struct jumpinfo{
	int index;
	int len;
} JINFO;

extern void (*fps[10])(INST);
extern INST insts[1024];
extern char out[1024];

void InitVector();
void printState();
void printInst(int i);

extern int sp;
extern int ip;