def createList(difficulty: int) -> list:
    import random
    import math
    
    if difficulty != 1 and difficulty != 2 and difficulty != 3:
        print("Invalid difficulty, use either 1(easy), 2(medium), or 3(hard)")
        exit()
        
    nums = sorted((random.sample(range(1, (int) (10 * math.exp(difficulty))), 6)))
    print("The numbers given are:", nums)
    return nums

def randomOperator(nums: list, operator: int) -> int:
    import random
    ans = 0
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


def solvePuzzle(nums: list, difficulty: int):
    import random 
    steps = 0
    numbers = []
    if difficulty == 1:
        steps = 2
    elif difficulty == 2:
        steps = 3
    elif difficulty == 3:
        steps = 5
    else:
        exit()

    for _ in range(steps):
        numbers = random.sample(nums, 2)
        nums.remove(numbers[0])
        nums.remove(numbers[1])
        nums.append(randomOperator(numbers, random.randint(0, 3)))

    return nums[-1]

def createGame(diff: int):
    import math
    from solver import playerSolve
    nums = createList(diff)
    target = solvePuzzle(nums, diff)
    while target >= 10 * math.exp(diff) or target <= 0:
        target = solvePuzzle(createList(2), 2)
    print("The target number is:", target)
    playerSolve(nums, target)