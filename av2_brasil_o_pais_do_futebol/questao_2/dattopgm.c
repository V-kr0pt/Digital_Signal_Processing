/* Programa de conversao de imagens *.dat(madeiro)
   para imagens no formato *.pgm

   Autor: Waslon Terllizzie Araujo Lopes
   Data: Dez/99   
*/

#include <stdio.h> 
#include <stdlib.h> 
#include <malloc.h>
#include <string.h>
#include <math.h>

#define DIM 256
int main(int argc, char *argv[]){

	char name[25];
	int i,j,k,l;
	FILE *arquivo;
	int *ha,**pta;
	long w;
	float x;
	int flag;

	if(argc != 3){
		flag = 1;
	}
	
	if (flag){
		printf("\nDigite o nome do arquivo  de entrada de dados (*.dat): ");
		scanf("%s",&name[0]);
	} else {
		strcpy(name, argv[1]); 
	}
	
	if((arquivo=fopen(name,"r"))==NULL){
		printf("\nN�o foi poss�vel abrir o arquivo de entrada de dados\n");
		exit(1);
	}


	// alocacao da memoria 

	ha = (int *)malloc(DIM * DIM  * sizeof(int)); //n.o de pixels para niv. de cinza

	if( (!ha) ){
		     printf("\nFalha na aloca��o de mem�ria\n");
		     exit(1);
	}



	// alocacao da memoria  -- imagem de entrada

	pta = (int **)malloc(DIM*sizeof(int *));  // nivel de cinza de cada pixel
	if(!pta){
		  printf("\nFalha na aloca��o de mem�ria\n");
		  exit(1);
	}

	for(i=0;i<DIM;i++){
	     pta[i] =(int *)malloc(DIM * sizeof(int));
	     if(!pta[i]) {
		     printf("\nFalha na aloca��o de mem�ria\n");
		     exit(1);
	     }
	}



	//leitura dos valores da matriz da imagem de entrada

	for(i=0;i<DIM*DIM;i++){
		fscanf(arquivo,"%f",&x);
		*(ha+i) = x;
	}
	fclose(arquivo);


	// reconstrucao da imagem a partir do vetor de entrada

	for(i=0;i<64;i++)
		for(j=0;j<64;j++)
			for(k=0;k<4;k++)
				for(l=0;l<4;l++)
					   pta[4*i+k][4*j+l] = ha[1024*i + 16*j + 4*k + l];

	//armazenamento da imagem reconstruida em arquivo
	if(flag){
		printf("\nDigite o nome do arquivo da imagem de saida (*.pgm): ");
		scanf("%s",&name[0]);
	}
	else {
		strcpy(name, argv[2]); 
	}
	if((arquivo=fopen(name,"w"))==NULL){
	  printf("\nN�o foi poss�vel abrir o arquivo de sa�da de dados\n");
	  exit(1);
	  }

	fprintf(arquivo,"P2 \n256 256 \n255\n"); //Cabecalho .pgm

	w = 1;
	for(i=0;i<DIM;i++)
		for(j=0;j<DIM;j++){
			fprintf(arquivo,"%d ",*(pta[i]+j));
			if(!(w%256))
				fprintf(arquivo,"\n");
			w++;
		}
	fclose(arquivo);

	return 1;
}     // fim do programa principal