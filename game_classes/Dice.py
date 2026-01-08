# Class handling dices and rolls
import random


class Dice:
    dice_type = ""
    dice_value = 0
    dice_types = ["d4", "d6", "d8", "d10", "d12", "d20"]

    def __init__(self, dice_type):
        if dice_type in self.dice_types:
            self.dice_type = str(dice_type)
            self.dice_value = int(self.dice_type.split("d")[1])

    def roll(self, quantity=1):
        result = []
        step = 0

        if int(quantity) >= 1:
            while step < int(quantity):
                result.append(random.randint(1, self.dice_value))
                step += 1
            
        return result