import itertools
import sys


def get_input_words():
    num_words = int(input("Enter the number of words you want to input: "))
    words = []
    for _ in range(num_words):
        word = input("Enter a word: ")
        words.append(word)
    return words


def get_letter_substitutions():
    return {
        'a': ['4', '@'],
        'b': ['8'],
        'e': ['3', '€'],
        'g': ['6', '9'],
        'h': ['#'],
        'i': ['1', '!'],
        'l': ['1', '|'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'z': ['2'],
    }


def get_special_symbols():
    return ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def generate_case_combinations(word):
    if not word:
        return ['']
    first_letter = word[0]
    rest_combinations = generate_case_combinations(word[1:])
    substitutions = get_letter_substitutions().get(first_letter.lower(), [])
    return [first_letter.lower() + rest for rest in rest_combinations] + \
           [first_letter.upper() + rest for rest in rest_combinations] + \
           [sub + rest for sub in substitutions for rest in rest_combinations]


def count_combinations(words):
    count = 0
    for i in range(0, len(words) + 1):
        for combo in itertools.permutations(words, i):
            mixed_case_combos = list(itertools.product(*(generate_case_combinations(word) for word in combo)))
            count += len(mixed_case_combos) * len(list(itertools.combinations(range(len(combo) + 1), 16 -
                                                                              len("".join(combo)))))
    return count


def generate_and_save_combinations(words, file_name="combinations.txt"):
    special_symbols = get_special_symbols()
    completed_combinations = 0
    generated_combinations = set()

    with open(file_name, "w") as f:
        for i in range(0, len(words) + 1):  # Update the range start from 1 to 0
            for combo in itertools.permutations(words, i):
                mixed_case_combos = itertools.product(*(generate_case_combinations(word) for word in combo))
                for mixed_case_combo in mixed_case_combos:
                    for filler_count in range(16 - len("".join(mixed_case_combo)) + 1):
                        for filler_positions in itertools.combinations(range(len(mixed_case_combo) + 1), filler_count):
                            fillers = itertools.product(special_symbols, repeat=filler_count)
                            for filler_set in fillers:
                                result = []
                                filler_index = 0
                                for j, word in enumerate(mixed_case_combo):
                                    if j in filler_positions:
                                        result.append(filler_set[filler_index])
                                        filler_index += 1
                                    result.append(word)
                                if len("".join(result)) <= 32 and "".join(result) not in generated_combinations:
                                    f.write("".join(result) + "\n")
                                    generated_combinations.add("".join(result))
                                    completed_combinations += 1
                                    if completed_combinations % 1000 == 0:  # Update progress every 1000 combinations
                                        sys.stdout.write(f"\r{completed_combinations} combinations completed.")
                                        sys.stdout.flush()

    print(f"\n{len(generated_combinations)} unique combinations saved to '{file_name}'")

def main():
    words = get_input_words()
    generate_and_save_combinations(words)
    print(f"\nCombinations saved to 'combinations.txt'")


if __name__ == "__main__":
    main()
