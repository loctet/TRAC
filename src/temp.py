def function1():
    print("Function 1 is called")

def function2():
    print("Function 2 is called")

# Define functions up to function10
def function3():
    print("Function 3 is called")

functions = {
    1: function1,
    2: function2,
    3: function3
}

for i in range(1, 4):  # from 1 to 10
    functions[i]()

for i in range(1, 4):
    eval(f'function{i}()')

for i in range(1, 4):
    func = globals()[f'function{i}']
    func()
