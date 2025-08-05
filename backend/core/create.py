def createList(difficulty: int) -> list:
    import random
    import math
    
    if difficulty != 1 and difficulty != 2 and difficulty != 3:
        print("Invalid difficulty, use either 1(easy), 2(medium), or 3(hard)")
        exit()
    
    if difficulty == 1:
        max_num = 15
    elif difficulty == 2:
        max_num = 25
    else:
        max_num = 40
        
    nums = sorted((random.sample(range(1, max_num + 1), 6)))
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
        steps = 3
    elif difficulty == 3:
        steps = 4
    else:
        exit()
    
    for _ in range(steps):
        numbers = random.sample(nums, 2)
        nums.remove(numbers[0])
        nums.remove(numbers[1])
        nums.append(randomOperator(numbers, random.randint(0, 3)))
    
    return int(nums[-1])

def createGame(difficulty: int = 1) -> dict:
    import math
    import random
    
    nums = createList(difficulty)
    old_nums = nums.copy()
    target = solvePuzzle(nums, difficulty)
    
    max_allowed = 10 * math.exp(difficulty)
    attempts = 0
    max_attempts = 100
    
    while (target >= max_allowed or target <= 0 or target in old_nums) and attempts < max_attempts:
        nums = createList(difficulty)
        old_nums = nums.copy()
        target = solvePuzzle(nums, difficulty)
        attempts += 1
    
    if target in old_nums:
        available_targets = list(range(1, max_allowed + 1))
        for num in old_nums:
            if num in available_targets:
                available_targets.remove(num)
        
        if available_targets:
            target = random.choice(available_targets)
        else:
            target = max(old_nums) + random.randint(1, 10)
    
    return {
        'numbers': old_nums,
        'target': target,
        'steps': [],
        'completed': False,
        'message': None,
        'difficulty': difficulty
    }

def applyMove(state: dict, move: dict) -> tuple:
    num1 = move['num1']
    num2 = move['num2']
    operation = move['operation']
    numbers = state['numbers'][:]
    steps = state['steps'][:]
    target = state['target']
    completed = state['completed']
    message = None
    valid_ops = ['+', '-', '*', '/']
    if completed:
        return ({'correct': False, 'message': 'Game already completed.', 'new_state': state}, state)
    if num1 not in numbers or num2 not in numbers or operation not in valid_ops:
        message = 'Pick numbers in the list and a valid operator.'
        return ({'correct': False, 'message': message, 'new_state': state}, state)
    if operation == '/' and (num2 == 0 or num1 % num2 != 0):
        message = 'To use divide, pick two divisible numbers.'
        return ({'correct': False, 'message': message, 'new_state': state}, state)
    numbers.remove(num1)
    numbers.remove(num2)
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        result = int(num1 / num2)
    numbers.append(result)
    numbers = sorted(numbers)
    steps.append(f"{num1} {operation} {num2} = {result}")
    if target in numbers:
        completed = True
        message = 'Congratulations, you finished the puzzle!'
    new_state = {
        'numbers': numbers,
        'target': target,
        'steps': steps,
        'completed': completed,
        'message': message
    }
    new_state['difficulty'] = state.get('difficulty', 1)
    if 'game_id' in state:
        new_state['game_id'] = state['game_id']
    return ({'correct': True, 'message': message or '', 'new_state': new_state}, new_state)