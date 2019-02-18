import multiprocessing


def func(x):
    return x ** 2


pool = multiprocessing.Pool(4)
result = pool.map(func, range(10))
print(result)
