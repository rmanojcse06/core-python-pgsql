import time;
import datetime;

def mymethod1():
    for i in range(1, 20, 2):
        return i

def mymethod2():
    for i in range(1, 20, 2):
        yield i


list=[ i+100 for i in range(2,22,3)]
list2=[mymethod2()]


def myfunc1(text):
    return text.upper();

func1var=myfunc1;


def add_using_first_class_objects(firstFunc,secondFunc):
    a=firstFunc();
    b=secondFunc();
    return a+b;


########################################
def hi_decorator(func):
    print(">>> Hi ");
    func();

@hi_decorator
def print_user():
    print("Sanjana")

########################################
def add_curry(x):
    def adder(y):
        return x+y;
    return adder;

adder_10 = add_curry(10);
print(" Add is ",adder_10(23));


########################################
def log_decorator(func):
    def inner(*args, **kwargs):
        begin=time.time_ns();
        x=func(*args, **kwargs);
        end=time.time_ns();
        print(str(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"))+"[LOG]:: function=",func.__name__," outputs to ",x);
        return x;
    return inner;

@log_decorator
def square(n):
    return 1 if n < 1 else n+square(n-1);
########################################


########################################
def input_decorator(*args, **kwargs):
    def inner(func):
        a=int(input(kwargs['fText']))
        b=int(input(kwargs['sText']))
        x=func(a,b);
        return x;
    return inner;

@input_decorator(fText="First :",sText="Second :")
@log_decorator
def sum(a,b):
    return a+b;
########################################

loop = 0
def memoize_decorator(func):
    
    memory={}
    def inner(num):
        global loop
        loop += 1
        x=func(num);
        memory[loop]=x
        print("memory => ",memory)
        return x;
    return inner;

@memoize_decorator
def factorial(num):
    return 1 if num <=1 else num * factorial(num-1);

print("Factorial of 5 is ",factorial(5))
