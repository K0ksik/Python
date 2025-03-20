import re

all_roman = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

def to_roman(num):
    roman = ''
    while num > 0:
        for i, r in all_roman:
            while num >= i:
                roman += r
                num -= i
    return roman

n = int(input("Введите число: "))
print("Перевод: " + to_roman(n))
print("Перевод числа 1945: " + to_roman(1945))
print("-"*100)


word = input("Введите слово для проверки на палиндром: ")
clword = re.sub(r'[^\w]', '', word.lower())  
print(clword == clword[::-1])

print("-"*100)
print("Прибавление единицы:")
def plus(mass):
    num = int(''.join(map(str, mass)))
    num += 1
    return [int(m) for m in str(num)]

mass = [1, 0, 0]
result = plus(mass)
print(result) 


