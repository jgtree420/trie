# Trie (Prefix Tree)
The Trie Data Structure using Python

[![Trie Data Structure - Python](https://img.youtube.com/vi/Qqx3Gz9qeGc/0.jpg)](https://youtu.be/Qqx3Gz9qeGc)

## Overview
A Trie (pronounced "try") is a specialized tree-based data structure
used to store a dynamic set of strings. Unlike a standard binary search tree, 
where nodes compare values, a Trie organizes data by character position.

It is most commonly used to retrieve information based on string prefixes.

## Key Features
* Fast Lookups -> Searching for a word takes time proportional to the length of the word ($L$), 
not the number of items in the data structure ($N$).
* Prefix Matching -> It is the optimal structure for finding all words that start with a specific sequence (e.g.,
typing "the" and finding "there", "therefore", "them").
* Space Efficient -> It saves space when storing many words with common prefixes, though it can use more memory 
than a simple list if the words are mostly unique.

## Big O
 **Insert** $O(L)$  
 **Search** $O(L)$  
 **Prefix** $O(L)$  
$L$ = Length of the word 


## Common Use Cases
*  **Autocomplete:** (e.g., Google search bar).
*  **Spell Checkers:** Validating words against a dictionary.
*  **IP Routing:** Longest prefix matching in network routers.


## Sources:  
**google search words**  
https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt

**books/videos used for research**  
Data Structures the Fun Way - Jeremy Kubica  
NeuralNine - Trie - Data Structures in Python #7 - https://youtu.be/y3qN18t-AhQ?si=1l1NPfJMPHjdbSg7 
