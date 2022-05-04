#include <iostream>
#include <string>
#include <stdbool.h>
#include <ctype.h>
#include <malloc.h>

using namespace std;

struct list
{
    char n_terminal;
    string derivation;
};

typedef struct list list;

int lowcase(string word)
{
    int low;

    for (int h = 0; h < word.size(); h++)
    {
        if (isupper(word[h]))
            low = 0;
        else
            low = 1;
    }
    return low;
}

string firsts = " ";
string follows = " ";

void first(char firstChar)
{
    int size = 9; // 9 regras da gramática, pode ser alterado conforme a quantidade de regras
    // table recebe a gramática: não terminal e suas derivações
    list table[size] = {
        {'S', "S ; S "},
        {'S', "id = E "},
        {'S', "print ( L ) "},
        {'E', "id "},
        {'E', "num "},
        {'E', "E + E "},
        {'E', "( S , E ) "},
        {'L', "E "},
        {'L', "L , E "}};
    string derivation_aux;
    char word[25];
    int h = 0, i = 0;

    for (i = 0; i < size; i++)
    {
        if (table[i].n_terminal == firstChar)
        {
            derivation_aux = table[i].derivation;
            for (int j = 0; j < derivation_aux.size(); j++)
            {
                if ((derivation_aux[j] != ' '))
                {
                    word[h] = derivation_aux[j];
                    h++;
                }
                else if (derivation_aux[j] == '\n')
                {
                    word[h] = derivation_aux[j];
                    h++;
                }
                else
                {
                    word[h] = '\0';
                    h = 0;
                    break;
                }
            }
            int ret = lowcase(word);
            if (ret == 1)
            {
                firsts += ' ';
                firsts += word;
            }
            else
            {
                firsts = firsts + ' ';
                if (firstChar != word[0])
                {
                    first(word[0]);
                }
            }
        }
    }
}

void follow(char followChar)
{
    int size = 9; // 9 regras da gramática, pode ser alterado conforme a quantidade de regras
    // table recebe a gramática: não terminal e suas derivações
    list table[size] = {
        {'S', "S ; S "},
        {'S', "id = E "},
        {'S', "print ( L ) "},
        {'E', "id "},
        {'E', "num "},
        {'E', "E + E "},
        {'E', "( S , E ) "},
        {'L', "E "},
        {'L', "L , E "}};

    char word[25];
    int h = 0;
    string derivation_aux;

    for (int i = 0; i < size; i++)
    {
        derivation_aux = table[i].derivation;
        for (int j = 0; j < derivation_aux.size(); j++)
        {
            if (derivation_aux[j] == followChar)
            {
                for (int x = j + 2; x < derivation_aux.size(); x++)
                {
                    if ((derivation_aux[x] != ' '))
                    {
                        word[h] = derivation_aux[x];
                        h++;
                    }
                    else if (derivation_aux[x] == '\n')
                    {
                        word[h] = derivation_aux[j];
                        h++;
                    }
                    else
                    {
                        word[h] = '\0';
                        h = 0;
                        break;
                    }
                }
                int ret = lowcase(word);
                if (ret == 1) // significa que é um terminal
                {
                    follows += ' ';
                    follows += word;
                }
                else // significa que é um não terminal, precisamos achar o first do não terminal
                {
                    first(word[0]);
                    follows += firsts;
                }
            }
        }
    }
}

int main()
{
    char firstChar, character, followChar;

    cout << "OBS 1: preencha a tabela na funcao first com sua gramatica, e informe abaixo somente o NAO TERMINAL, exemplo: S" << endl;
    // FAÇA O FIRST OU FOLLOW, NÃO FAÇA OS DOIS DE UMA VEZ, PODE TER ERRO DEVIDO BUFFER NAS VARIÁVEIS GLOBAIS

    // RETIRE O COMENTÁRIO ABAIXO PARA OBTER O FIRST
    /*
    cout << "Inform no terminal first: ";
    cin >> firstChar;
    first(firstChar);
    */

    // RETIRE O COMENTÁRIO ABAIXO PARA OBTER O FOLLOW
    cout << "Inform no terminal follow: ";
    cin >> followChar;
    follow(followChar);

    cout << endl
         << "----------------------------------------" << endl;
    // cout << "FIRST "<< "(" << firstChar << "): " << firsts << endl;
    cout << "FOLLOW "
         << "(" << followChar << "): " << follows << endl;
    cout << "----------------------------------------" << endl;
    cout << "*OBS 2: desconsiderar os terminais repetidos, visto que sao obtidos via recursao" << endl;

    return 0;
}
