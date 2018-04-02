from math import sqrt


TOTAL_PRODUCT_COUNT = 24000
PLANNING_TIME = 365
NEEDED_PRODUCTS_PER_DAY = TOTAL_PRODUCT_COUNT / PLANNING_TIME
MONTHLY_STORAGE_COST_PER_PRODUCT = 0.1
DAILY_STORAGE_COST_PER_PRODUCT = MONTHLY_STORAGE_COST_PER_PRODUCT * 12 / 365
COST_PER_BATCH = 350
Q0 = sqrt(2 * NEEDED_PRODUCTS_PER_DAY * COST_PER_BATCH / DAILY_STORAGE_COST_PER_PRODUCT)


def calculate_qn(n):
    return NEEDED_PRODUCTS_PER_DAY * TOTAL_PRODUCT_COUNT / n


def calculate_average_cost(q):
    return (NEEDED_PRODUCTS_PER_DAY * COST_PER_BATCH / q) + (DAILY_STORAGE_COST_PER_PRODUCT * q / 2)


def calculate_optimal_interval(optimal_batch_size):
    return PLANNING_TIME / (TOTAL_PRODUCT_COUNT / optimal_batch_size)


def main():
    q_next = 0
    q_previous = 0
    n = 1
    while not (q_previous >= Q0 > q_next):
        q_previous = q_next
        q_next = calculate_qn(n)
        n += 1
    f_next = calculate_average_cost(q_next)
    f_previous = calculate_average_cost(q_previous)
    optimal_batch_size = q_next if f_next < f_previous else q_previous
    optimal_interval = calculate_optimal_interval(optimal_batch_size)
    print('Optimal batch size: {}'.format(optimal_batch_size))
    print('Optimal interval: {}'.format(optimal_interval))


if __name__ == '__main__':
    main()
    