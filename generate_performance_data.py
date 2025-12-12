"""
CS3C, Final Project - Trie
Performance Test
Performance Data and Charts are stored here
https://docs.google.com/spreadsheets/d/1AJwvonATKYG73zY29ZabC9i9n1JjX9KIxpOYLX2zEfY/edit?usp=sharing

Jonathan Gordon
"""

import random
import string

import timeit
from trie import Trie

COMMON_PREFIXES = (
    "un", "re", "in", "dis", "non",
    "pre", "post", "sub", "inter", "trans",
    "pro", "anti", "over", "under",
    "auto", "micro", "macro", "multi", "mono"
)


def generate_autocomplete_prefixes(words: list[str], max_num_prefixes):
    """Helper to dynamically generate prefixes for the given list of words
    # Add some nonexistent prefixes to simulate misses

    """

    prefixes = set()
    hit_to_miss_ratio = .80
    max_num_prefixes_valid = int(max_num_prefixes * hit_to_miss_ratio)
    chars = string.ascii_lowercase

    # generate valid prefixes
    while len(prefixes) < max_num_prefixes_valid:
        word = random.choice(words)

        prefix_len = random.randint(1, len(word))
        prefix = word[:prefix_len]
        prefixes.add(prefix)

    # add invalid prefixes
    # loop until we fill the set with invalid prefixes
    while len(prefixes) < max_num_prefixes:
        prefix_len = random.randint(1, 5)
        prefix = "".join(random.choice(chars) for _ in range(prefix_len))
        prefixes.add(prefix)

    return prefixes


def generate_performance_dataset(word_count):
    """
    generate N (word_count) random words and save to a file that can be loaded
    for performance testing.  The random words randomly may include a common_prefix
    """
    chars = string.ascii_lowercase

    # threshold used to determine if a common prefix should be used
    use_prefix_threshold = 0.7

    for _ in range(word_count):
        word_length = random.randint(1, 30)

        # determine if prefix should be used
        if random.random() < use_prefix_threshold:
            prefix = random.choice(COMMON_PREFIXES)
        else:
            prefix = ""

        yield prefix + "".join(random.choice(chars) for _ in range(word_length))


def run_trie_insert(trie: Trie, words):
    for word in words:
        trie.insert(word)


def run_trie_search(trie: Trie, words):
    for word in words:
        trie.search(word)


def run_trie_autocomplete(trie: Trie, prefixes):
    for prefix in prefixes:
        # need to convert to a list because this is a generator
        _ = list(trie.autocomplete(prefix))


def run_trie_starts_with(trie: Trie, prefixes):
    """
    Measures the time to walk down the prefix.
    """
    for prefix in prefixes:
        _ = trie.starts_with(prefix)


def run_list_insert(list_: list[str], words):
    for word in words:
        list_.append(word)


def run_list_search(list_: list[str], words):
    for word in words:
        _ = word in list_


def run_list_autocomplete(list_: list[str], prefixes):
    for prefix in prefixes:
        for word in list_:
            _ = word.startswith(prefix)


def run_list_starts_with(list_: list[str], prefixes):
    """
    Measures the time to walk down the prefix.
    """
    for prefix in prefixes:
        _ = any(word.startswith(prefix) for word in list_)


def run_set_insert(set_: set, words):
    for word in words:
        set_.add(word)


def run_set_search(set_: set, words):
    for word in words:
        _ = word in set_


def run_set_autocomplete(set_: set, prefixes):
    for prefix in prefixes:
        for word in set_:
            _ = word.startswith(prefix)


def run_set_starts_with(set_: set, prefixes):
    for prefix in prefixes:
        _ = any(word.startswith(prefix) for word in set_)


def run_performance_test():
    word_count_sizes = [1_000, 10_000, 50_000, 100_000, 200_000, 300_000, 400_000,
                        500_000, 600_000, 700_000, 800_000]

    # word_count_sizes = [1_000, 10_000]

    heading = "WordCount,DataStucture,Operation,Duration"
    print(heading)

    random.seed(42)

    for word_count in word_count_sizes:
        performance_dataset = list(generate_performance_dataset(word_count))
        autocomplete_prefixes = generate_autocomplete_prefixes(performance_dataset, 500)

        # create a shuffled dataset for searching
        shuffled_performance_dataset = random.sample(performance_dataset, k=len(performance_dataset))

        ### TRIE
        trie = Trie()
        # trie insert
        duration = timeit.timeit(lambda: run_trie_insert(trie, performance_dataset), number=1)
        print(f"{word_count}, trie, insert, {duration:.6f}")

        # trie search
        duration = timeit.timeit(lambda: run_trie_search(trie, shuffled_performance_dataset), number=1)
        print(f"{word_count}, trie, search, {duration:.6f}")

        # trie autocomplete
        duration = timeit.timeit(lambda: run_trie_autocomplete(trie, autocomplete_prefixes), number=1)
        print(f"{word_count}, trie, autocomplete, {duration:.6f}")

        # trie starts-with
        duration = timeit.timeit(lambda: run_trie_starts_with(trie, autocomplete_prefixes), number=1)
        print(f"{word_count}, trie, starts-with, {duration:.6f}")

        ### LIST
        test_list = list()
        # list insert
        duration = timeit.timeit(lambda: run_list_insert(test_list, performance_dataset), number=1)
        print(f"{word_count}, list, insert, {duration:.6f}")

        # list search
        # note list search degrades after 100_000 so we will skip this after
        if word_count <= 100_000:
            duration = timeit.timeit(lambda: run_list_search(test_list, shuffled_performance_dataset), number=1)
            print(f"{word_count}, list, search, {duration:.6f}")

        # list autocomplete
        duration = timeit.timeit(lambda: run_list_autocomplete(test_list, autocomplete_prefixes), number=1)
        print(f"{word_count}, list, autocomplete, {duration:.6f}")

        # list starts-with
        duration = timeit.timeit(lambda: run_list_starts_with(test_list, autocomplete_prefixes), number=1)
        print(f"{word_count}, list, starts-with, {duration:.6f}")

        ### SET
        test_set = set()
        # list insert
        duration = timeit.timeit(lambda: run_set_insert(test_set, performance_dataset), number=1)
        print(f"{word_count}, set, insert, {duration:.6f}")

        # list search
        duration = timeit.timeit(lambda: run_set_search(test_set, shuffled_performance_dataset), number=1)
        print(f"{word_count}, set, search, {duration:.6f}")

        # list autocomplete
        duration = timeit.timeit(lambda: run_set_autocomplete(test_set, autocomplete_prefixes), number=1)
        print(f"{word_count}, set, autocomplete, {duration:.6f}")

        # trie starts-with
        duration = timeit.timeit(lambda: run_set_starts_with(test_set, autocomplete_prefixes), number=1)
        print(f"{word_count}, set, starts-with, {duration:.6f}")


if __name__ == "__main__":
    run_performance_test()


