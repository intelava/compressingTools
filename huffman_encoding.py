import numpy as np
import random
import string
import math

def is_equal(original, compressed):
    return original == compressed

def create_random_text(num_of_k):
    return "".join(random.choices(string.ascii_lowercase, k=num_of_k))

def calc_probs(text):
    char_dict = {}
    for char in text:
        if char in char_dict.keys():
            char_dict[char]["count"] = char_dict[char]["count"] + 1
        else:
            char_dict[char] = {
                "count": 1
            }
    num_of_chars = len(char_dict.keys())
    for char in char_dict.keys():
        char_dict[char] = {
            "prob": char_dict[char]["count"] / len(text)
        }
    finalized_list = []
    for char in char_dict.keys():
        finalized_list.append(Node(char, char_dict[char]["prob"]))
    
    finalized_list = sorted(finalized_list, key=lambda x: x.prob)
    return finalized_list


class Node:
    def __init__(self, char, prob):
        self.char = char
        self.prob = prob
        self.left_node = None
        self.right_node = None
    
    def assign_left(self, node):
        self.left_node = node
    def assign_right(self, node):
        self.right_node = node
    
def create_tree(text):
    probs_list = calc_probs(text)

    while(len(probs_list) != 1):
        new_node1 = probs_list.pop(0)

        new_node2 = probs_list.pop(0)
        

        parent_node = Node("", new_node1.prob + new_node2.prob)
        parent_node.assign_left(new_node1)
        parent_node.assign_right(new_node2)

        probs_list.append(parent_node)
        probs_list = sorted(probs_list, key=lambda x: x.prob)
    
    return probs_list

n = parent_node
code_dct = {}
def traverse_tree(n, code=""):
    if n.right_node != None:
        traverse_tree(n.right_node, code + "0")
    if n.left_node != None:
        traverse_tree(n.left_node, code + "1")
    
    if n.char != "":
        code_dct[n.char] = code
    return

inverse_dct = {v: k for k, v in code_dct.items()}

def encode_text(text):
    for char in text:
        text = text.replace(char, code_dct[char])
    return text

def decode_text(encoded_text):
    decoded_text = ""
    while(len(encoded_text) != 0):
        
        for offset in range(1,6):
            code = encoded_text[0:offset]
            if code in inverse_dct.keys():
                decoded_text += inverse_dct[code]
                encoded_text = encoded_text[offset:]
                break
    
    return decoded_text

def calculate_efficiency(text, encoded):
    code_size = math.ceil(math.log2(len(set(text))))
    total_code_size = len(text) * code_size
    return len(encoded) / total_code_size

def calculate_entropy_based_length(text):
    probs_list = calc_probs(text)
    sum = 0
    for n in probs_list:
        sum += n.prob * -math.log2(n.prob)
    return sum * len(text)