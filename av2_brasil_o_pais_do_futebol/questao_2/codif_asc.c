/******************************************************************
* Arquivo: codif_asc.c                                            *
*                                                                 *
* Codifica um arquivo ascii segundo o dicion�rio QV fornecido, se-*
* guindo a regra da distor��o m�nima (dist�ncia euclidiana).      *
*                                                                 *
* Autor: Francisco Madeiro Bernardino Junior                      *
* UFPB - CCT - DEE - LABCOM                                       *
*                                                                 * 
* Modificado por: Waslon Terllizzie Araujo Lopes                  *
* Data: 17/04/2001                                                *
******************************************************************/ 

#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <math.h>
#include <string.h>
#include "alocacao.h"
#include "inout.h"
#define cnome 50 

int codifica(double **pta, double *y, int N, int K); 
void codifica_arquivo(char entrada[], char saida[], double **x, int N, int K);
double distancia(double *pta, double *ptb, int K);

int main(int argc, char *argv[])
{
   char dicion[cnome], codi[cnome], ent[cnome];
   int   K, N;
   double **pta;
   
   if(argc!=6){
      printf("Qual a dimens�o do quantizador?\n");
      scanf("%d", &K);

      printf("Qual o n�mero de n�veis do dicion�rio?\n");
      scanf("%d", &N);

      printf("Qual o nome do arquivo que cont�m o dicion�rio ?\n");
      scanf("%s", dicion);

      printf("Qual o nome do arquivo que cont�m os dados a serem codificados ?\n");
      scanf("%s", ent);

      printf("Qual o nome do arquivo de s�mbolos codificados?\n");
      scanf("%s", codi);
   }
   else{
      K = atoi(argv[1]); // atoi converts a string to an integer
      N = atoi(argv[2]);
      strcpy(dicion,argv[3]); // strcpy copies a string
      strcpy(ent,argv[4]);
      strcpy(codi,argv[5]);
   }

   pta = ler_arquivo(dicion,N,K);

   codifica_arquivo(ent,codi,pta,N,K); 

   return (0);
     
} /* fim do main */

int codifica(double **pta, double *y, int N, int K){ 
//Retorna o �ndice do vetor-c�digo  que produz a menor distor��o 
//Dicion�rio (pta) - Vetor (y) - N�mero de vetores do dicion�rio (N)

int i,cod;
double dist;

dist = distancia(pta[0],y,K);
cod = 0;

for(i=1;i<N;i++)
	if(dist > distancia(pta[i],y,K) ){
		dist = distancia(pta[i],y,K);
		cod = i;
	}
	
return cod;
}

double distancia(double *pta, double *ptb, int K)
// Calcula a distancia euclidiana entre os vetores (dimensao K) pta e ptb
{
int i;
double dist;

dist = 0.0;

for(i=0;i<K;i++)
	dist += pow(pta[i] - ptb[i],2.0);

dist = sqrt(dist);

return dist;
}


void codifica_arquivo(char entrada[], char saida[], double **x, int N, int K){
/******************************************************************
* Fun��o que codifica os vetores do arquivo de nome "entrada" em  *
* �ndices armazenados no arquivo de nomes "sa�da", de acordo com  *
* o dicion�rio "x" de dimens�o N,K.                               *
******************************************************************/

FILE *entradap, *saidap;
int i, j;
double *y;

y = aloca_vetor_double(K);  

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


for(i=0;!feof(entradap);i+=K){
	  fscanf(entradap,"%lf",&y[0]);
	  if( feof(entradap) ) break;
     for(j=1;j<K;j++)
	    fscanf(entradap,"%lf",&y[j]);
     fprintf(saidap,"%d\n",codifica(x,y,N,K));
	  for(j=0;j<K;j++)
		 y[j] = 0.0;
   }

fclose(saidap);
fclose(entradap);

return;
}

