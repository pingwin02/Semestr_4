#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <signal.h>
#include <semaphore.h>
#include <fcntl.h>
#include "pqueue.h"

char *filename = "queue.dat";

int itemId = 0;
sem_t *sem;

typedef struct item item;
struct item
{
	int id;
};

item *
produce()
{
	int time = rand() % 5 + 1;
	item *it = (item *)malloc(sizeof(item));

	sleep(time);
	it->id = itemId;
	itemId += 1;
	return it;
}

void consume(item *it)
{
	int time = rand() % 5 + 1;
	sleep(time);
	free(it);
}

void print_item_con(void *data)
{
	item *it = (item *)data;
	printf("C: Item %d", it->id);
}

void print_item_prod(void *data)
{
	item *it = (item *)data;
	printf("P: Item %d", it->id);
}

void producer(pid_t childPid)
{
	sem_wait(sem);
	pqueue *qu = NULL;
	qunserialize(&qu, sizeof(item), filename);
	int size = 0;
	pqueue *tmp = qu;
	while (tmp != NULL)
	{
		size++;
		tmp = tmp->next;
	}
	if (size > 4)
	{
		printf("Producer is waiting for consumer\n");
	}
	else
	{
		item *it = produce();
		printf("Producer is producing an item %d\n", it->id);
		qinsert(&qu, it, it->id);
		qlist(qu, print_item_prod);
		qserialize(qu, sizeof(item), filename);
	}
	sem_post(sem);
	sleep(1);
}

void consumer()
{
	sem_wait(sem);
	pqueue *qu = NULL;
	qunserialize(&qu, sizeof(item), filename);
	pqueue *node = qpop(&qu);
	qserialize(qu, sizeof(item), filename);
	sem_post(sem);
	sleep(1);
	if (node != NULL)
	{
		item *it = node->data;
		printf("Consumer is consuming an item %d\n", it->id);
		qlist(qu, print_item_con);
		consume(it);
		free(node);
	}
	else
	{
		printf("Consumer is waiting for an item\n");
	}
}

void my_handler(int s)
{
	sem_close(sem);
	sem_unlink("mysemaphore");
	exit(1);
}

int main(int argc, char **argv)
{
	pid_t pid;
	pqueue *qu = NULL;
	/* watch -n 1 ps -l --forest */

	// setbuf(stdout, NULL);

	sem = sem_open("mysemaphore", O_CREAT, 0600, 1);

	/* create empty queue */
	qserialize(qu, sizeof(item), filename);

	signal(SIGINT, my_handler);

	pid = fork();
	if (pid == 0)
	{
		while (1)
		{
			consumer();
		}
	}
	else
	{
		while (1)
		{
			producer(pid);
		}
	}

	return 0;
}
