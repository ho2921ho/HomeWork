import random


def lottery():
    numbers = []
    while len(numbers) != 7:
        num = random.choice(range(1,45))
        if num not in numbers:
            numbers.append(num)            
    return sorted(numbers)


