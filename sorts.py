from random import shuffle


start = 1
compare = 2
move = 3
complete = 4


def bubble_sort(array):
    for i in range(len(array)-1, 0, -1):
        swapped = False
        for j in range(i):
            yield array, compare, j, j+1
            if array[j] > array[j+1]:
                swapped = True
                array[j], array[j+1] = array[j+1], array[j]
                yield array, move, j, j+1
        if not swapped:
            yield array, complete, -1, -1
    yield array, complete, -1, -1


def selection_sort(array):
    for i in range(len(array)):
        selected = i
        for j in range(i+1, len(array)):
            yield array, compare, selected, j
            if array[selected] > array[j]:
                selected = j
        array[i], array[selected] = array[selected], array[i]
        yield array, move, i, selected
    yield array, complete, -1, -1


def insertion_sort(array):
    for i in range(1, len(array)):
        current = array[i]
        j = i
        while j > 0 and array[j-1] > current:
            array[j] = array[j-1]
            j -= 1
            yield array, compare, i, j
        array[j] = current
        yield array, compare, i, j
        yield array, move, i, j
    yield array, complete, -1, -1


def quick_sort_generator(array, first, end):
    if first >= end:
        return

    pivot = array[end]
    index = first

    for i in range(first, end):
        if array[i] < pivot:
            array[i], array[index] = array[index], array[i]
            index += 1
        yield array, move, i, index
    array[end], array[index] = array[index], array[end]
    yield array, move, end, index

    yield from quick_sort_generator(array, first, index - 1)
    yield from quick_sort_generator(array, index + 1, end)


def quick_sort(array, first, end):
    yield from quick_sort_generator(array, first, end)
    yield array, complete, -1, -1


def merge(array, first, end):
    merged = sorted(array[first:end+1])

    for i, sorted_val in enumerate(merged):
        array[first + i] = sorted_val
        yield array, move, first + i, first + i


def merge_sort_generator(array, first, end):
    if end <= first:
        return

    mid = (first + (end - 1)) // 2
    yield from merge_sort_generator(array, first, mid)
    yield from merge_sort_generator(array, mid+1, end)
    yield from merge(array, first, end)


def merge_sort(array, first, end):
    yield from merge_sort_generator(array, first, end)
    yield array, complete, -1, -1


def is_sorted(array):
    for i in range(0, len(array) - 1):
        if array[i] > array[i + 1]:
            return False
    return True


def bogo_sort(array):
    while not is_sorted(array):
        shuffle(array)
        yield array, start, 0, 0


def radix_sort(array):
    max_digits = len(str(max(array)))

    for i in range(max_digits):
        buckets = [[] for _ in range(10)]
        for j in range(len(array)):
            n_digit = (array[j] // (10 ** i)) % 10
            buckets[n_digit].append(array[j])
            yield array, compare, j, j

        digit_array = [element for bucket in buckets for element in bucket]

        # For visualization purposes
        for k in range(len(array)):
            index = array.index(digit_array[k])
            array[k], array[index] = array[index], array[k]
            yield array, move, k, index
    yield array, complete, -1, -1
