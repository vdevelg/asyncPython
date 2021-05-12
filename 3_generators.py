from time import time



def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)
        
        yield pattern.format(str(t))

        sum = 5 + 5
        print(sum)


g = gen_filename()



# Пример алгоритма "карусель":

def gen1(s):
    for i in s:
        yield i


def gen2(n):
    for i in range(n):
        yield i


g1 = gen1('Vladislav')
g2 = gen2(9)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
