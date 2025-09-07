import random

class GameLogic:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.number_to_guess = random.randint(1, 100)
        self.attempts = 0
        self.hints_given = []

    def check_guess(self, guess):
        self.attempts += 1
        if guess < self.number_to_guess:
            return "Too low! Try again."
        elif guess > self.number_to_guess:
            return "Too high! Try again."
        else:
            return "Correct!"

    def get_hint(self):
        hints = []
        # Hint 1: Odd or Even
        hints.append("The number is even." if self.number_to_guess % 2 == 0 else "The number is odd.")

        # Hint 2: Range
        if self.number_to_guess <= 50:
            hints.append("The number is between 1 and 50.")
        else:
            hints.append("The number is between 51 and 100.")

        # Hint 3: Closer range
        low = max(1, self.number_to_guess - 10)
        high = min(100, self.number_to_guess + 10)
        hints.append(f"The number is between {low} and {high}.")

        # Avoid repeating hints
        new_hints = [h for h in hints if h not in self.hints_given]
        if new_hints:
            import random
            hint = random.choice(new_hints)
            self.hints_given.append(hint)
            return hint
        else:
            return "No more hints left!"

    def reveal_answer(self):
        return self.number_to_guess
