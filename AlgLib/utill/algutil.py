import matplotlib.pyplot as plt
import random
import numpy as np
def generate_array(len, min = "empty", max = "empty", unique = False):
    max_value = len // 2
    if min == "empty" or not isinstance(min, int):
        min = -max_value

    if max == "empty" or not isinstance(max, int):
        max = max_value

    if max - min + 1 < len:
        raise ValueError("Range between min and max is too small for the requested array length.")


    if unique:
        array = random.sample(range(min, max + 1), len)
    else:
        array = [random.randint(min , max) for _ in range(len)]

    return array

def generate_sample(sort):
    samples = [1, 10, 100, 1000, 10000]
    o = []
    for size in samples:
        _, operations = sort(generate_array(size))
        o.append((size, operations))
    return o


def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))


plt.ion()

def visualize_sort(steps):
    print(steps[-1])
    plt.figure(figsize=(5, 4))
    global_min = min(min(s) for s in steps)
    global_max = max(max(s) for s in steps)

    for i, step in enumerate(steps):
        plt.cla()

        plt.ylim(global_min - 1, global_max + 1)
        plt.xticks([])
        plt.yticks([])
        plt.bar(range(len(step)), [0.05 if val == 0 else val for val in step], color='skyblue')
        plt.xlabel(f"Step {i}")
        plt.pause(0.5)

    plt.show()

def o_graph(n_o_pairs):
    x_funcs = np.arange(1, max(n_o_pairs)[0] + 1)
    y_linear = x_funcs
    y_quadratic = x_funcs**2
    y_logarithmic = np.log(x_funcs)
    y_linear_log = x_funcs * np.log(x_funcs)
    y_exponential = 2**x_funcs

    for i in range(1, len(y_exponential)):
        y_exponential[i] = max(y_exponential[i], y_exponential[i-1])

    plt.figure(figsize=(10, 6))

    plt.plot(x_funcs, y_linear, label='O(n)', linewidth=2 ,alpha=0.5)
    plt.plot(x_funcs, y_quadratic, label='O(n^2)', linewidth=2 ,alpha=0.5)
    plt.plot(x_funcs, y_logarithmic, label='O(log n)', linewidth=2 ,alpha=0.5)
    plt.plot(x_funcs, y_linear_log, label='O(n log n)', linewidth=2 ,alpha=0.5)
    plt.plot(x_funcs, y_exponential, label='O(2^n)', linewidth=2 ,alpha=0.5)

    n, o = zip(*n_o_pairs)
    plt.plot(n, o, marker='o', color='green',  linewidth=2, label='Result', zorder=5, markersize=5)

    plt.title('Algorithm Complexity Graph')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Number of Operations')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(1, max(x_funcs))
    plt.ylim(1, max(o))
    plt.legend()

    plt.show()


def test_sorting(num_arrays, sort_function, max_array_length = 20, min_value = -20, max_value = 20):
    success = True
    for _ in range(num_arrays):
        length = random.randint(1, max_array_length)
        min_val = random.randint(min_value, 0)
        max_val = random.randint(0, max_value)
        unique = random.choice([True, False])

        try:
            arr = generate_array(length, min_val, max_val, unique)
        except ValueError as e:
            print(f"Skipping an array due to invalid parameters: {e}")
            continue

        sorted_arr, _ = sort_function(arr)
        if not is_sorted(arr):
            success = False
            print(f"Array {arr} was not sorted correctly to {sorted_arr}.")
            break

    if success:
        print("All arrays sorted successfully!")
    else:
        print("Some arrays were not sorted correctly.")

#%%
