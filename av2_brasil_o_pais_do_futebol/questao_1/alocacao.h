#ifndef	_ALOCACAO_H
#define	_ALOCACAO_H

#include <malloc.h>
#include <stdlib.h>
#include "complex.h"

typedef  struct{unsigned bit : 1;} sbit;

int **aloca_matriz_int(int N, int K);
sbit *aloca_vetor_sbit (int N);
double *aloca_vetor_double(int N);
int *aloca_vetor_int(int N);
fcomplex *aloca_vetor_fcomplex (int N);
double **aloca_matrizd(int N, int K);
void desaloca_matrizd(double **pt, int N);
fcomplex *aloca_vetor_fcomplex(int N);


int *aloca_vetor_int(int N){
/*******************************************************************
* Fun��o que  retorna um ponteiro inteiro de dimens�o N.           *
*******************************************************************/
int *x,i;

x = (int *)malloc(N*sizeof(int));  
if(!x){
  printf("\nFalha na aloca��o de mem�ria\n");
  exit(1);
}

for(i=0;i<N;i++)
  x[i] = 0;

return (x);
}

double *aloca_vetor_double(int N){
/*******************************************************************
* Fun��o que  retorna um ponteiro double de dimens�o N.           *
*******************************************************************/
double *x;
int i;

x = (double *)malloc(N*sizeof(double));  
if(!x){
  printf("\nFalha na aloca��o de mem�ria\n");
  exit(1);
}

for(i=0;i<N;i++)
  x[i] = 0.0;

return (x);
}

double **aloca_matrizd(int N, int K){
/*******************************************************************
* Fun��o que  retorna um ponteiro double de dimens�o N x K         *
*******************************************************************/
int i,j;
double **x;

x = (double **)malloc(N*sizeof(double*));  
if(!x){
  printf("\nFalha na aloca��o de mem�ria\n");
  exit(1);
}

for(i=0;i<N;i++){
   x[i] =(double *)malloc(K * sizeof(double));
   if(!x[i]) {
     printf("\nFalha na aloca��o de mem�ria\n");
     exit(1);
   }
}

for(i=0;i<N;i++)
  for(j=0;j<K;j++)
	 x[i][j] = 0.0;

return (x);
}


void desaloca_matrizd(double **pt, int N){
/******************************************************************
* Desaloca o ponteiro da matriz double (dim N x K).               *
******************************************************************/

int i;

for(i=0;i<N;i++)
  free(pt[i]);
free(pt);

return;
}


fcomplex *aloca_vetor_fcomplex(int N){
/*******************************************************************
* Fun��o que  retorna um ponteiro fcomplex de dimens�o N           *
*******************************************************************/

fcomplex *x;

x = (fcomplex *)malloc(N*sizeof(fcomplex));  
if(!x){
  printf("\nFalha na aloca��o de mem�ria\n");
  exit(1);
}

return (x);
}

sbit *aloca_vetor_sbit(int N){
/*******************************************************************
* Fun��o que  retorna um ponteiro sbit de dimens�o N           *
*******************************************************************/

sbit *x;

x = (sbit *)malloc(N*sizeof(sbit));  
if(!x){
  printf("\nFalha na aloca��o de mem�ria\n");
  exit(1);
}

return (x);
}

int **aloca_matriz_int(int N, int K){
/*******************************************************************
* Fun��o que  retorna um ponteiro int de dimens�o N x K         *
*******************************************************************/
int i;
int **x;

x = (int **)malloc(N*sizeof(int*));  
if(!x){
  printf("\nFalha na aloca��o de mem�ria\n");
  exit(1);
}

for(i=0;i<N;i++){
   x[i] =(int *)malloc(K * sizeof(int));
   if(!x[i]) {
     printf("\nFalha na aloca��o de mem�ria\n");
     exit(1);
   }
}

return (x);
}




#endif	/* alocacao.h  */
