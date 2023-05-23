#include <stdio.h>
#include <stdlib.h>
#include "priority_queue_list.h"

void
qlist(pqueue *head, void (*print_data)(void *)) {
	pqueue *p;
	
	for (p = head; p != NULL; p = p->next) {
		printf("%d: ", p->k);
		print_data(p->data);
		printf("\n");
	}
	
}

void
qinsert(pqueue **phead, void *data, int k) {

	pqueue* p;
	p = (pqueue *) malloc(sizeof(pqueue));
	p->data = data;
	p->k = k;
	p->next = NULL;
	p->prev = NULL;
	if (*phead && k > (*phead)->k) {
		p->next = *phead;
		(*phead)->prev = p;
		*phead = p;
	} else if (*phead) {
		pqueue *q;
		for (q = *phead; q->next != NULL; q = q->next) {
			if (k > q->next->k) {
				p->next = q->next;
				p->prev = q;
				q->next->prev = p;
				q->next = p;
				break;
			}
		}
		if (q->next == NULL) {
			q->next = p;
			p->prev = q;
		}
	}
	else {
		*phead = p;
	}

}


void
qremove(pqueue **phead, int k) {
	if (*phead) {
		pqueue *p;
		for (p = *phead; p != NULL; p = p->next) {
			if (p->k == k) {
				if (p->prev == NULL) {
					*phead = p->next;
					if (p->next != NULL) {
						p->next->prev = NULL;
					}
				}
				else {
					p->prev->next = p->next;
					if (p->next != NULL) {
						p->next->prev = p->prev;
					}
				}
				free(p);
				break;
			}
		}
	}
}

