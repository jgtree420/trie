"""
CS3C, Final Project - Trie data structure
implementation of core features of the trie data structure
insert, search, delete, autocomplete
Jonathan Gordon
"""


class TrieNode:
    """
    A single Trie Node
    """

    def __init__(self):
        # store children (TrieNodes) in a dictionary
        self._children = {}
        # signifies the end of a word.  This is needed for words that
        # are completed but the prefix to a longer word
        self._is_end_of_word = False

    @property
    def children(self) -> dict:
        return self._children

    @property
    def is_end_of_word(self) -> bool:
        return self._is_end_of_word

    @is_end_of_word.setter
    def is_end_of_word(self, value: bool):
        self._is_end_of_word = value


class Trie:
    """
    The main Trie Data Structure
    """

    def __init__(self, words: list[str] = None):
        """
        initialize root with an empty TrieNode
        """
        self._root = TrieNode()
        # keep track of the Trie size
        self._count = 0

        # load words during initialization if set
        if words:
            for word in words:
                self.insert(word)

    def _find_prefix_end_node(self, prefix: str) -> TrieNode | None:
        """
        Helper method used to navigate to node containing the final character of
        the prefix
        """
        current_node = self._root
        for c in prefix:
            if c not in current_node.children:
                return None
            current_node = current_node.children[c]

        return current_node

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word starts with the prefix
        return True if it does.  False otherwise
        """
        return self._find_prefix_end_node(prefix) is not None

    def insert(self, word: str):
        current_node = self._root
        # perform dfs for each character in the word
        for c in word:
            # if the char is not in current node's children add
            if c not in current_node.children:
                current_node.children[c] = TrieNode()
            # continue dfs
            current_node = current_node.children[c]

        # we reached the end, mark this node as the end of the word
        # update count only if current_node.is_end_of_word was not set previously
        if not current_node.is_end_of_word:
            current_node.is_end_of_word = True
            self._count += 1

    def search(self, word: str) -> bool:
        """
        :param word: word to find
        :return: True if final character in the string is also marked as end of the word
                    False otherwise (not found)
        """
        node = self._find_prefix_end_node(word)

        # if node is not None, and node is marked as the end of the word
        if node is not None and node.is_end_of_word:
            return True
        else:
            return False

    def delete(self, word: str) -> bool:
        """
        If delete is successful return True
         else return False
        """

        # if word does not exist return false
        if not self.search(word):
            return False

        # ignore _delete_recursive return because its used only for
        # the pruning of the Trie.  It does not signify success.
        self._delete_recursive(self._root, word, 0)
        self._count -= 1
        return True

    def _delete_recursive(self, current_node: TrieNode,
                          word: str, index: int) -> bool:
        """
        This recursive method returns a boolean to signal
        to the parent node if it's safe to delete the child node
        True -> Its safe to delete the child node because child node has
                 no children
                AND
                the child node is not marked as the end of a word
        False -> do not delete child node because it's still in use
        """
        # set is_end_of_word to False if index = len(word)
        # if current_node has 0 children return True
        # else return False
        if index == len(word):
            current_node.is_end_of_word = False
            return len(current_node.children) == 0

        c = word[index]
        if c not in current_node.children:
            return False

        child_node = current_node.children[c]
        if child_node is None:
            return False

        # recursively call _delete by increasing index + 1
        # delete_child is set to True if the child_node has no children as well
        #  and the child_node is not marked as end of a word
        ok_to_delete_child = self._delete_recursive(child_node, word, index + 1)

        if ok_to_delete_child:
            # remove from dictionary
            del current_node.children[c]

            # determine if current_node is safe to delete
            # no children and not marked as end of a word
            if len(current_node.children) == 0 \
                    and not current_node.is_end_of_word:
                return True
        # return False for all other cases
        return False

    def _get_words_from_prefix(self, current_node: TrieNode,
                               current_prefix: str):
        """
        a generator that uses recursion to return all words
         starting from the current node
        """
        if current_node.is_end_of_word:
            yield current_prefix

        for c in current_node.children:
            child_node = current_node.children[c]
            # recursively call with child node and current_prefix + c
            yield from self._get_words_from_prefix(child_node, current_prefix + c)

    def autocomplete(self, prefix: str):
        """
        generate a list of words that start with the given prefix
        """

        # find starting node
        node = self._find_prefix_end_node(prefix)

        if node:
            yield from self._get_words_from_prefix(node, prefix)

    def __iter__(self):
        """
        iterates over ALL words in the Trie
        """
        yield from self._get_words_from_prefix(self._root, "")

    def __len__(self):
        """
        returns the total number of words in the Trie
        """
        return self._count

    def __str__(self):
        all_words = list(self)
        return (f"Number of Words={len(self)}\n"
                f"words={all_words}")

    def __repr__(self):
        return str(self)
