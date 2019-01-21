# -*- coding: utf-8 -*-
basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
fruit = set(basket)
print fruit

a = set('abracadabra')
print(len(a))
b = set('alacazam')
print(len(b))

print a - b 
print a | b
print a & b
print a ^ b
