from functools import cached_property

DICTIONARY = None

with open("dictionary.txt", "r") as f:
    DICTIONARY = f.read().split()


class Candidate:
    def __init__(self, word: str) -> None:
        self.word = word
        self.w_length = len(word)
        self.probability = 50

    def update_prob(self, exlude_letters: list[str], placed_letters: list[str]) -> None:
        if any(letter in self.word for letter in exlude_letters):
            self.probability = 0
            return

        for idx, letter in enumerate(placed_letters):
            if letter is not None:
                if self.word[idx] == letter:
                    self.probability += self.probability * (
                        (100 // self.w_length) / 100
                    )

    def __str__(self) -> str:
        return f"Candidate <{self.word}>: {self.probability}"

    def __repr__(self) -> str:
        return f"Candidate <{self.word}>: {self.probability}"


class MotusSolver:
    def __init__(self, solution: str) -> None:
        self.solution = solution
        self.exlude_letters = []
        self.placed_letters = [None] * len(self.solution)
        self.candidates = list(map(Candidate, self.filter_initial_set()))

    @cached_property
    def solution_len(self) -> int:
        return len(self.solution)

    @cached_property
    def first_letter(self) -> str:
        return self.solution[0]

    def filter_initial_set(self) -> None:
        for word in DICTIONARY:
            if len(word) == self.solution_len and word[0] == self.first_letter:
                yield word

    def filter_exluded_letters(self, word: str) -> None:
        for letter in word:
            if letter not in self.exlude_letters:
                yield letter

    def submit_candidate(self):
        for idx, letter in enumerate(
            self.filter_exluded_letters(self.candidates[0].word)
        ):
            if letter == self.solution[idx]:
                self.placed_letters[idx] = letter
            elif letter not in self.solution:
                self.exlude_letters.append(letter)

        if self.candidates[0].word != self.solution:
            del self.candidates[0]

    def update_candidates_prob(self) -> None:
        for candidate in self.candidates:
            candidate.update_prob(self.exlude_letters, self.placed_letters)

        self.candidates.sort(key=lambda candidate: candidate.probability, reverse=True)

    def solve(self) -> str:
        tries = 1
        while None in self.placed_letters:
            if tries > 6:
                print("MON ALGO PUE DU CUL")
                return ""
            print(f"Try number {tries}")
            print(self.candidates[0])
            self.submit_candidate()
            print(f"Excluded letters: {self.exlude_letters}")
            print(f"Placed letters: {self.placed_letters}")
            print("------------------------------------")
            self.update_candidates_prob()
            tries += 1


def main():
    from random import randint

    to_find = DICTIONARY[randint(0, len(DICTIONARY) - 1)]
    print(f"Word to find: {to_find}\n")
    solver = MotusSolver(to_find)
    solver.solve()


if __name__ == "__main__":
    raise SystemExit(main())
