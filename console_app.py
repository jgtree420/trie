"""
CS3C, Final Project - Trie
Console app to test auto-completion
Jonathan Gordon
"""
import os
from trie import Trie


def load_words_from_file(filepath: str):
    """
    A generator that will read a file line by line.  This will
    yield lowercase alphabetic strings
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} NOT Found!")

    try:
        with open(filepath, 'r') as file:
            for line in file:
                # remove whitespace and convert to lowercase
                word = line.strip().lower()
                # yield word if is not empty and empty line
                if word:
                    yield word
    except IOError as e:
        raise IOError(f"Error reading file: {e}")

class SearchApp:
    def __init__(self, words=None):
        self.trie = Trie(words)

        print(f"Trie Loaded with {len(self.trie):,} words")

    def run(self):
        print("==========================================")
        print("               AutoComplete")
        print("==========================================")
        print("Start typing a word.  Press ENTER to see suggestions")
        print("Type ':q' to quit")

        while True:
            try:
                user_input = input("search prefix -> ")
                user_input = user_input.strip().lower()

                if user_input == ":q":
                    print("Exiting AutoComplete")
                    break

                if not user_input:
                    continue

                print(self._auto_complete(user_input))


            except KeyboardInterrupt:
                print("Exiting AutoComplete")
                break

    def _auto_complete(self, prefix, max_results=10):
        print(f"Auto-complete suggestions for prefix {prefix}")
        suggestions = []

        for i, word in enumerate(self.trie.autocomplete(prefix)):
            if i <= max_results:
                suggestions.append(word)
            else:
                break
        return suggestions if suggestions else "No Matching Words"


if __name__ == "__main__":
    word_file = "google-10000-english.txt"
    print(f"Loading Trie from {word_file}")
    app = SearchApp(load_words_from_file(word_file))
    app.run()
