typedef struct vm {
    char c0;
    char c1;
    char c2;
    char c3;
    int dw4;
    int dw8;
    int dw12;
    int dw16;
    int dw20;
    int pc_counter; // 28
    unsigned short c30;
    unsigned short c32;
    unsigned short sh36;
    unsigned short sh38;
    unsigned char yyy0;
    unsigned char yyy1;
    unsigned char instr_offset;
    unsigned char yyy3;
    unsigned short sh1;
    unsigned short sh2;
    unsigned short c48;
    char always_true;
    char c51;
    unsigned char opcode;
    char xx1;
    unsigned short xx2;
    unsigned short reg1;  // 56
    unsigned short reg2;  // 58
    char is_next_ins;  // 56
    char c57;  // 57
    char c58;  // 58
    char c59;  // 59
    unsigned short c60;  // 60
    unsigned short answer;  // 62
    unsigned char zz1;
    unsigned char zz2;
} VM, *PVM;