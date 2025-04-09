/******************************************************************
*	Programa dat2raw.c                                             *
*                                                                 *
*  Transforma um arquivo texto de aúdio (-1 <= x < +1) em aúdio   *
*  binário usando 16 bits.                                        *
*                                                                 *
*  Autor: Waslon Terllizzie Araújo Lopes                          *
*  Data: 29/01/2017                                               *
*                                                                 *
*  Uso: dat2raw.out entrada.dat saida.raw                         *
******************************************************************/
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "inout.h"
#define cnome 100 /* comprimento max de nome de arquivo */

int main (int argc, char **argv){

FILE *f;
char amos[cnome],quant[cnome];
int16_t ampl;
int8_t bytes[2];
unsigned int t;
int n_amos;
double *y;

/* Abre os arquivos de entrada e saída */
if(argc!=3){
printf("Qual o nome do arquivo original (*.dat)?\n");
scanf("%s", amos); 
y = ler_vetor_arquivo_treino(amos,&n_amos);

printf("Qual o nome do arquivo de aúdio (*.raw)?\n");
scanf("%s", quant);
f = fopen(quant, "wb");
} 
else {
y = ler_vetor_arquivo_treino(argv[1],&n_amos);
f = fopen(argv[2], "wb");
}

for (t = 0; t < n_amos; ++t) {
    ampl = INT16_MAX * y[t];
    bytes[1] = ampl >> 8;
    bytes[0] = ampl & 255;
    fwrite(bytes, 2, sizeof(int8_t), f);
}
fclose(f);
return (1);
}
