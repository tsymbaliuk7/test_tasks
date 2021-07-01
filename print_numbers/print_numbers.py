def print_numbers():
    for i in range(11, 80):
        string = '$$' if i % 3 == 0 else ''
        string = string + '@@' if i % 5 == 0 else string
        print(string if string else i)


print_numbers()
