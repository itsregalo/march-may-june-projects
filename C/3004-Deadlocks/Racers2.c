 
/*
CS 410 OS
Lab 09: The Racers Problem
NAGASWETHA NEERUKONDA
*/


#include<stdio.h>  
#include<pthread.h> 
#include<stdlib.h> 
 
 
#define THREAD_NUM 2  
#define MAX_ROUNDS 200000
#define TRUE  1 
#define FALSE 0
  
  
/* mutex locks for each bridge */  
pthread_mutex_t B0, B1;
 
/* racer ID */ 
int r[THREAD_NUM]={0,1};  
  
/* number of rounds completed by each racer */  
int numRounds[THREAD_NUM]={0,0};  
  
  
void *racer(void *); /* prototype of racer routine */  
  
  
int main()  
{  
    pthread_t tid[THREAD_NUM]; 
    void *status; 
    int i,j;  
 
      
    /* create 2 threads representing 2 racers */  
    for (i = 0; i < THREAD_NUM; i++)  
    {  
        pthread_create(&tid[i], NULL, racer, (void *)&r[i]);  
        printf("Thread %d created\n", i);
 
    }  
  
    /* wait for the join of 2 threads */  
     for (i = 0; i < THREAD_NUM; i++)  
     {  
        printf("Waiting for thread %d to finish\n", i);
        pthread_join(tid[i], &status);
        printf("Thread %d joined\n", i);


     }   
      
    printf("\n");  
    for(i=0; i<THREAD_NUM; i++)  
        printf("Racer %d finished %d rounds!!\n", i, numRounds[i]);  
     
 if(numRounds[0]>=numRounds[1]) printf("\n RACER-0 WINS.\n\n");  
 else  printf("\n RACER-1 WINS..\n\n");  
 
 return (0);  
}  
  
  
void *racer(void  *arg)  
{   
  int  index = *(int*)arg, NotYet; 
  
    while( (numRounds[0] < MAX_ROUNDS) && (numRounds[1] < MAX_ROUNDS) )  
    {  
 
      NotYet = TRUE;

       /* RACER 0 tries to get both locks before she makes a round */  
      if(index==0){
        pthread_mutex_lock(&B0);
        pthread_mutex_lock(&B1);
        NotYet = FALSE;

      }

       /* RACER 1 tries to get both locks before she makes a round */  
      if(index==1){
        pthread_mutex_lock(&B1);
        pthread_mutex_lock(&B0);
        NotYet = FALSE;
	

      } 
       numRounds[index]++;      /* Make one more round */

    
       /* unlock both locks */  
       pthread_mutex_unlock(&B0);  
       pthread_mutex_unlock(&B1);  
 
       /* random yield to another thread */ 
             
    }
    
printf("racer %d made %d rounds !\n", index, numRounds[index]);  

pthread_exit(0);  

} 
