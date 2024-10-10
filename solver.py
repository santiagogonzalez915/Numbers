def playerSolve(nums: list, target: int):
    ans = 0
    num1 = 0
    num2 = 0
    operations = ["+", "-", "*", "/"]
    operator = ""
    completed_steps = []

    while ans != target:
        ##Getting user input
        num1 = int(input("Number 1: "))
        operator = input("Operation (use only +, -, *, and /): ")
        num2 = int(input("Number 2: "))
        
        print()
        
        ##Check for valid numbers and operator
        if num1 not in nums or num2 not in nums or operator not in operations: 
            print("Pick numbers in the list and a valid operator")
            continue
        
        ##Check that if division is chosen, the numbers are divisible
        if num1 % num2 != 0 and operator == "/":
            print("To use divide, pick two divisible numbers")
            continue
        
        nums.remove(num1)
        nums.remove(num2)
        
        nums.append(performOperation(num1, num2, operator))
        nums = sorted(nums)
        
        completed_steps.append(f"{num1} {operator} {num2} = {performOperation(num1, num2, operator)}")
        
        if target in nums:
            ans = target
            break
        
        print("New List of numbers: ", nums)
    
    print("Congratulations, you finished the puzzle!")
    print()
    print("The steps you took were as follows:")
    print()
    for i in completed_steps:
        print(i)
        

def performOperation(num1: int, num2: int, operation: str) -> int:
    if operation == "+": return num1 + num2
    elif operation == "-": return num1 - num2
    elif operation == "*": return num1 * num2
    elif operation == "/": return int(num1 / num2)
    