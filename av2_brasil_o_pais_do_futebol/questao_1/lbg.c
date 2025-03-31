/******************************************************************
 *	Programa lbg.c                                                 *
 *  Realiza o treinamento do dicion�rio pelo algoritmo LBG         *
 *  Modificado por: Waslon Terllizzie Ara�jo Lopes                 *
 *  Data: 17/04/2001                                               *
 ******************************************************************/

#include <stdio.h>
#include "alocacao.h"
#include "inout.h"
#include <stdlib.h>
#include <math.h>
#include <string.h>
#define cnome 100 /* comprimento maximo de nome de arquivo,incluindo diretorio */

void classifica(double **x, int N, int K, double **y, int nvet, int *c);
void centroide(double **x, int N, int K, double **y, int nvet, int *c);
double distorcao(double **x, int N, int K, double **y, int nvet, int *c);
double distq(double *x, double *y, int K);
void soma_vet(double *x, double *y, int K);

int main(int argc, char *argv[])
{

  char dicion[cnome], dicioini[cnome], amos[cnome];
  int K, N, nvet, *c;
  double epslon, dist, dist_old;
  double **x, **y, aux;
  if(argc!=7){
    printf("Qual a dimens�o do quantizador?\n");
    scanf("%d", &K);
    printf("Qual o n�mero de n�veis do dicion�rio?\n");
    scanf("%d", &N);
    printf("Qual o limite de redu��o percentual na distor��o?\n");
    scanf("%lf", &epslon);
    printf("Qual o nome do arquivo que cont�m o dicion�rio inicial?\n");
    scanf("%s", dicioini);
    printf("Qual o nome do arquivo que cont�m a sequ�ncia de treino?\n");
    scanf("%s", amos);
    printf("Qual o nome do arquivo para armazenar o dicion�rio final?\n");
    scanf("%s", dicion);
  } else {
    K = atoi(argv[1]); // atoi converts a string to an integer
    N = atoi(argv[2]);
    epslon = atof(argv[3]);
    strcpy(dicioini,argv[4]); // strcpy copies a string
    strcpy(amos,argv[5]);
    strcpy(dicion,argv[6]);
  }


  /* Leitura dos vetores do dicion�rio inicial */

  x = ler_arquivo(dicioini, N, K);

  /* Leitura dos vetores de treino */

  y = ler_arquivo_treino(amos, &nvet, K);

  /* Aloca��o de mem�ria para o vetor c que ir� guardar para cada vetor
  de treino y, o �ndice do vetor do dicion�rio que produz a menor
  distor��o */

  c = aloca_vetor_int(nvet);

  /* O algoritmo LBG come�a aqui */

  dist_old = 1e20;

  classifica(x, N, K, y, nvet, c);

  for (;;)
  {

    centroide(x, N, K, y, nvet, c);

    dist = distorcao(x, N, K, y, nvet, c);

    aux = (dist_old - dist) / dist_old * 100;
    printf("distor��o: %.3e \t redu��o(%%): %.3e\n", dist, aux);

    if (dist == 0.0)
    {
      escreve_arquivo(dicion, x, N, K);
      exit(1);
    }

    if ((dist_old - dist) / dist_old < epslon / 100.0)
      break;

    dist_old = dist;
  }

  /* Escreve os vetores do dicion�rio calculado no arquivo de sa�da */

  escreve_arquivo(dicion, x, N, K);

  return (0);

} /* Fim do programa principal */

void classifica(double **x, int N, int K, double **y, int nvet, int *c)
{
  /******************************************************************
   * Esta fun��o classifica os vetores de entrada y de acordo com os *
   * vetores do dicion�rio x, associando a vari�vel c o �ndice do ve-*
   * tor que produz a menor distor��o.                               *
   *    x = vetores do dicion�rio                                    *
   *    N = n�mero de vetores do dicion�rio                          *
   *	  K = n�mero de componentes de cada vetor                      *
   *	  y = vetores a serem classificados                            *
   *	  nvet = n�mero de vetores a serem classificados               *
   *	  c = vetor que ir� armazenar a classifica��o de cada vetor y  *
   ******************************************************************/

  int i, j;
  double dist;

  for (i = 0; i < nvet; i++)
  {
    dist = distq(y[i], x[0], K);
    c[i] = 0;
    for (j = 1; j < N; j++)
    {
      if (dist > distq(y[i], x[j], K))
      {
        dist = distq(y[i], x[j], K);
        c[i] = j;
      }
    }
  }

  return;
}

double distq(double *x, double *y, int K)
{
  /******************************************************************
   * Esta fun��o retorna a dist�ncia euclidiana quadr�tica entre os  *
   * vetores x e y, considerando K componentes em cada vetor         *
   ******************************************************************/

  double distq;
  int i;

  distq = 0.0;

  for (i = 0; i < K; i++)
    distq += (x[i] - y[i]) * (x[i] - y[i]);

  return distq;
}

void centroide(double **x, int N, int K, double **y, int nvet, int *c)
{
  /******************************************************************
   * Esta fun��o gera o dicion�rio de vetores x a partir dos vetores *
   * y  segundo a classifica��o armazenada na vari�vel c             *
   * x = vetores do dicion�rio                                       *
   * N = n�mero de vetores do dicion�rio                             *
   * K = n�mero de componentes de cada vetor                         *
   * y = vetores de entrada                                          *
   * nvet = n�mero de vetores y                                      *
   * c = vetor que armazena a classifica��o de cada vetor de y       *
   ******************************************************************/

  int i, j;
  int *nc; /* armazena o n�mero de vetores de cada classe */
  double *temp, **x_aux;

  x_aux = aloca_matrizd(N, K);

  temp = aloca_vetor_double(K);

  nc = aloca_vetor_int(N);

  /* Inicia o processo de c�lculo do centr�ide */
  /* 1.o Acumula os vetores */
  /* 2.o Normaliza��o */

  for (i = 0; i < nvet; i++)
    soma_vet(x_aux[c[i]], y[i], K);

  for (i = 0; i < N; i++)
    nc[i] = 0;

  for (i = 0; i < nvet; i++)
    nc[c[i]]++;

  for (i = 0; i < N; i++)
    for (j = 0; j < K; j++)
    {
      temp[j] = x_aux[i][j];
      if (nc[i] != 0)
        x_aux[i][j] = temp[j] / nc[i];
    }

  for (i = 0; i < N; i++)
    if (nc[i] != 0)
      for (j = 0; j < K; j++)
        x[i][j] = x_aux[i][j];
  // Algortimo de Lee
  //		x[i][j] = x[i][j] + s *(x_aux[i][j] -x[i][j]);

  free(temp);
  free(nc);
  desaloca_matrizd(x_aux, N);

  return;
}

void soma_vet(double *x, double *y, int K)
{
  /******************************************************************
   * Esta fun��o acrescenta o vetor y ao vetor x                     *
   ******************************************************************/

  int i;
  double temp[K];

  for (i = 0; i < K; i++)
    temp[i] = x[i];

  for (i = 0; i < K; i++)
    x[i] = temp[i] + y[i];

  return;
}

double distorcao(double **x, int N, int K, double **y, int nvet, int *c)
{
  /******************************************************************
   * Esta fun��o calcula a distor��o entre os vetores de entrada y e *
   * o dicion�rio calculado na fun��o centr�ide.                     *
   ******************************************************************/

  int i;
  double dist_total;

  classifica(x, N, K, y, nvet, c);

  dist_total = 0.0;

  for (i = 0; i < nvet; i++)
    dist_total += distq(y[i], x[c[i]], K);

  return dist_total;
}
