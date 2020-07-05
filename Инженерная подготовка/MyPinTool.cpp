
#include "pin.H"
#include <iostream>
#include <utility>
#include <fstream>
#include <cassert>
#include <vector>

using namespace std;
ofstream logg;

// size of arr of mines
const int m_size = 99 * 2 * 10000;

namespace MineSweeper
{
    // all mines (row, column) in all fields 
    vector<pair<int, int>> v_mines;
    // array of empty positions from left to right, from top to bottom
    vector<pair<int, int>> solution;
    // k - field (from 0 up to 9999)
    int k_field = 0;
    // current possition in solution vector
    int pos = 0;
    // field to make operations on
    char field[24][24];
    

    void load_mines()
    {
        char *memblock;
        int size;
        // open file from disk and read it
        ifstream file("mines.bin", ios::in|ios::binary|ios::ate);
        if (file.is_open())
        {
            size = file.tellg();
            memblock = new char [size];
            file.seekg(0, ios::beg);
            file.read(memblock, size);
            file.close();

            logg << "[+] mines are in memory." << endl;
        }
        else
        {
            logg << "[-] unable to read mines.bin" << endl;
            exit(-1);
        }
        // memblock -> arr of ints.
        auto mines = (int*)memblock;
        // basic check just to be sure it was loaded correctly
        assert(mines[0] == 20);
        // fill v_mines vector
        for (int i = 0; i < m_size; i += 2)
            v_mines.push_back(make_pair(mines[i], mines[i+1]));

        logg << "[+] " << v_mines.size() << " mines are loaded." << std::endl;
        delete[] memblock;
    }

    void fill()
    {
        auto st = v_mines.begin() + (k_field * 99);
        auto cur_mines = vector<pair<int, int>>(st, st + 99);
        for (auto &i : cur_mines)
            field[i.first][i.second] = 1;
    }

    void clear_field()
    {
        for (int i = 0; i < 24; i++)
            for (int j = 0; j < 24; j++)
                field[i][j] = 0;
    }

    void generate_solution()
    {
        solution.clear();
        clear_field();
        fill();
        for (int i = 0; i < 24; i++)
            for (int j = 0; j < 24; j++)
                if (!field[i][j])
                    solution.push_back(make_pair(i, j));
    }
}

/* 
Our make_move replacement
*/
void make_move(unsigned int * row, unsigned int * col)
{
    PIN_LockClient();
    // get current empty position
    auto p = MineSweeper::solution[MineSweeper::pos++];
    *row = p.first;
    *col = p.second;
    PIN_UnlockClient();
}

/* 
Our printf oracle
*/
void PrintfHander(char * fmt)
{
    string str(fmt);
    if (str.find("New game") != std::string::npos)
    {
        MineSweeper::pos = 0;
        MineSweeper::generate_solution();
    }

    if (str.find("Victory") != std::string::npos)
        MineSweeper::k_field++;
}

/*
Called on every image that was loaded.
 */
VOID ImageLoad(IMG img, VOID *v)
{
    logg << "loaded:\t" << IMG_Name(img) << std::endl;

    // we replace make_move function in main executable
    if (IMG_IsMainExecutable(img))
    {
        auto imageBase = IMG_LowAddress(img);
        auto funcAddr  = imageBase + 0xb67;

        auto rtn = RTN_FindByAddress(funcAddr);
        if (RTN_Valid(rtn))
        {
            RTN_Replace(rtn, AFUNPTR(make_move));
            logg << "[+] make_move hijacked." << std::endl; 
            MineSweeper::load_mines();
        }
    }

    // we will use printf as an oracle, so we hook it as well
    // notice that we are not replacing it, but just hooking before the call.
    auto rtn = RTN_FindByName(img, "printf");
    if (RTN_Valid(rtn))
    {
        RTN_Open(rtn);
        RTN_InsertCall(rtn, IPOINT_BEFORE, 
            AFUNPTR(PrintfHander), 
            IARG_FUNCARG_ENTRYPOINT_VALUE, 0,
            IARG_END);
        RTN_Close(rtn);
    }

}

INT32 Usage()
{
    return -1;
}


int main(INT32 argc, CHAR *argv[])
{
    // Initialize symbol processing
    //
    PIN_InitSymbols();

    MineSweeper::load_mines();
    // Initialize pin
    //
    if (PIN_Init(argc, argv))
        return Usage();

    logg.open("log.txt");
    // Register ImageLoad to be called when an image is loaded
    //
    IMG_AddInstrumentFunction(ImageLoad, 0);

    // Start the program in probe mode, never returns
    //
    PIN_StartProgram();

    return 0;
}
