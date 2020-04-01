try:
    print(int('1234a'))
except ValueError:
    print('invalid id')