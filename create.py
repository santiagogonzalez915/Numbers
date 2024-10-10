def createList(difficulty: int) -> list:
    import random
    import math
    
    if difficulty != 1 and difficulty != 2 and difficulty != 3:
        print("Invalid difficulty, use either 1(easy), 2(medium), or 3(hard)")
        exit()
        
    nums = sorted((random.sample(range(1, (int) (10 * math.exp(difficulty))), 6)))
    return nums

def randomOperator(nums: list, operator: int) -> int:
    import random
    
    while True:
        if operator == 0:
            return nums[0] + nums[1]
        elif operator == 1:
            return nums[0] - nums[1]
        elif operator == 2:
            return nums[0] * nums[1]
        elif operator == 3 and nums[0] % nums[1] == 0:
            return nums[0] / nums[1]
        else:
            operator = random.randint(0,2)


def solvePuzzle(nums: list, difficulty: int) -> int:
    import random 
    
    steps = 0
    numbers = []
    if difficulty == 1:
        steps = 2
    elif difficulty == 2:
        steps = random.randint(3,4)
    elif difficulty == 3:
        steps = 5
    else:
        exit()
    
    for _ in range(steps):
        numbers = random.sample(nums, 2)
        nums.remove(numbers[0])
        nums.remove(numbers[1])
        nums.append(randomOperator(numbers, random.randint(0, 3)))
    
    return int(nums[-1])

def createGame(diff: int):
    import math
    from solver import playerSolve
    
    nums = createList(diff)
    old_nums = nums.copy()
    target = solvePuzzle(nums, diff)
    
    while target >= 10 * math.exp(diff) or target <= 0:
        nums = createList(diff)
        old_nums = nums.copy()
        target = solvePuzzle(nums, diff)
        
    print("The given numbers are:", list(old_nums))
    print("The target number is:", target)
    playerSolve(nums, target)