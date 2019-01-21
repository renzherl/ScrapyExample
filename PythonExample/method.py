# -*- coding: utf-8 -*-

def show(mess="hello"):
    print mess

show()
show("machine learning")

def fib(n):
    a, b = 0, 1
    while(a < n):
        print a
        a, b = b, a+b

fib(20000)
