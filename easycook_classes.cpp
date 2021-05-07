#include <iostream>
using namespace std;

class Chefe{
    string nome;
    string username;
    string senha;
    string email;
    Receita favoritadas[100];
    Receita postadas[100];
    bool verificado;
};

class Receita{
    string titulo;
    float avaliacao;
    string tipoCulinaria;
    string equipamentos[100];
    int numComentarios;
    Comentario comentarios[100];
    string preparo;
    string restricoes[100];
    string ingredientes[100];
    float tempoPreparo;  
};

class Admin{
    string email;
    string senha;
};

class Comentario{
    string comentario;
    string timestamp;
};
