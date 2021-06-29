def slice_less(my_list: list, lesser: int):
    return list(sorted(filter(lambda x: x > lesser, my_list), reverse=True))


lst = list(range(10, 20))
print(slice_less(lst, 15))
