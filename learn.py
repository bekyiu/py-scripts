res = 'adbc %d %s' % (10, 'aaa')
print(res)

l = ['a', 'b', 'z', 'www']
# 解构
a, b, *_ = l
print(a, b)

a = 10
b = 10
print(a is b)

print(a in [1, 2, 10])
print(a not in [1, 2, 3])

print(f'{a}, {len(l)}')

if 2 > 1:
    print('da')
elif 1 == 1:
    print('deng')
else:
    print('xiao')
