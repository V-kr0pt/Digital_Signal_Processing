/******************************************************************
* Arquivo:decodif_asc.c                                           *
*                                                                 *
* Reconstru��o de sinal quantizado vetorialmente.                 *
*                                                                 *
* Autor: Francisco Madeiro Bernardino Junior                      *
*                                                                 *
* Modificado por: Waslon Terllizzie Ara�jo Lopes                  *
*                                                                 *
* Data: 18/04/2001.                                               *
*                                                                 *
******************************************************************/


#include <stdio.h>
#include <malloc.h>
#include <math.h>
#include "inout.h"
#define cnome 50 /* comprimento max. de nome de arquivo,incluindo diretorio */

void decodifica_arquivo(char entrada[], char saida[], double **x, int N, int K);
double distancia(double *pta, double *ptb, int K);

int main()
{
   char dicion[cnome], codi[cnome], decod[cnome];
   int   K, N;
   double **pta;
   

   printf("Qual a dimens�o do quantizador?\n");
   scanf("%d", &K);

   printf("Qual o n�mero de n�veis do dicion�rio?\n");
   scanf("%d", &N);

   printf("Qual o nome do arquivo que cont�m o dicion�rio ?\n");
   scanf("%s", dicion);

   printf("Qual o nome do arquivo de s�mbolos a serem decodificados ?\n");
   scanf("%s", codi);

   printf("Qual o nome do arquivo de s�mbolos decodificados ?\n");
   scanf("%s", decod);


   //Aloca��o de mem�ria -- vetor N x K

   pta = ler_arquivo(dicion,N,K); 

   decodifica_arquivo(codi,decod, pta, N, K);
	  
	return (0);     

} /* fim do main */

void decodifica_arquivo(char entrada[], char saida[], double **x, int N, int K){
/******************************************************************
* Fun��o que os �ndices armazenados no arquivo de nomes "entrada",*
* de acordo com o dicion�rio "x" de dimens�o N,K. Os dados de sa�-*
* s�o escritos no arqbuivo de nome "saida".                       *
******************************************************************/

FILE *entradap, *saidap;
int i, j;

entradap = fopen(entrada,"r");
if (!entradap) {
   printf("\nErro na abertura do arquivo dos dados a serem codificados\n");
   exit(1);
}

saidap = fopen(saida,"w");
if (!saidap) {
   printf("\nErro na abertura do arquivo dos dados codificados\n");
   exit(1);
}

for(;!feof(entradap);){
  fscanf(entradap,"%d",&i);
  if( feof(entradap) ) break;
     for(j=0;j<K;j++)
	     fprintf(saidap,"%f\n",*(x[i]+j));
}

fclose(saidap);
fclose(entradap);

return;
}

