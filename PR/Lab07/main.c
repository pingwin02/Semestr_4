#include <stdio.h>
#include <pthread.h>

#define RANGE 1000
#define NUM_THREADS 10

pthread_mutex_t mutex;

struct primes_data
{
    int primes[RANGE];
    int curr_p;
} typedef primes_data;

struct thread_data
{
    int a;
    int b;
    int no;
    primes_data *prime_data;
} typedef thread_data;

int isPrime(int a)
{
    int flag = 1;

    if (a == 0 || a == 1)
        return 0;
    for (int j = 2; j <= a / 2; ++j)
    {
        if (a % j == 0)
        {
            flag = 0;
            break;
        }
    }
    return flag;
}

void *printPrimes(void *data)
{
    struct thread_data *my_data = data;
    for (int i = my_data->a; i <= my_data->b; i++)
    {
        if (isPrime(i) == 1)
        {
            pthread_mutex_lock(&mutex);
            my_data->prime_data->primes[my_data->prime_data->curr_p] = i;
            my_data->prime_data->curr_p++;
            pthread_mutex_unlock(&mutex);
        }
    }
}

int main()
{
    pthread_t threads[NUM_THREADS];
    thread_data data[NUM_THREADS];

    primes_data prime_data;
    prime_data.curr_p = 0;

    pthread_mutex_init(&mutex, NULL);

    for (int i = 0; i < NUM_THREADS; i++)
    {
        data[i].a = i * (RANGE / NUM_THREADS);
        data[i].b = (i + 1) * (RANGE / NUM_THREADS);
        data[i].no = i + 1;
        data[i].prime_data = &prime_data;
        pthread_create(&threads[i], NULL, printPrimes, &data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("Total number of primes: %d\n", prime_data.curr_p);

    for (int i = 0; i < prime_data.curr_p; i++)
    {
        printf("%d ", prime_data.primes[i]);
    }

    printf("\n");

    pthread_mutex_destroy(&mutex);

    return 0;
}