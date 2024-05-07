import heapq
import itertools
import random
import sys
import os
from collections import defaultdict, Counter

import networkx as nx
from utils import remove_all, unique, first, probability, isnumber, issequence, Expr, expr, subexpressions, extend, infix_ops

def parse_kb_file(file_path):
    kb = PropDefiniteKB()
    query = None # Initialize Query with None
    try:
        with open(file_path, 'r') as file:
            mode = None
            for line in file:
                line = line.strip()
                if 'TELL' in line:
                    mode= 'tell'
                    continue
                elif 'ASK' in line:
                    mode = 'ask'
                    continue # Skips the line with ASK 
                
                if mode == 'tell' and line:
                    # Splitting each instruction on the line by semicolon
                    instructions = line.split(';')
                    for instruction in instructions:
                        if instruction.strip(): #Ensure the instruction is not empty
                            kb.tell(instruction.strip()) 
                elif mode == 'ask' and line:
                    # Handles the ask instruction if needed
                 
                    query = line.strip() # Directly store the query line
    except IOError:
        print(f"Error opening or reading the file: {file_path}") # Error message
    return kb, query



class KB:
    def __init__(self):
        self.clauses = []
    def tell(self, sentence):
        # Adds a sentence to the KB.
        raise NotImplementedError("This method should be overridden by subclasses")
    def ask(self, query):
        # Asks the KB if a query can be derived
        raise NotImplementedError("This method should be overridden by subclasses")
    def retract(self, sentence):
        # Removes a sentence from KB
        raise NotImplementedError("This method should be overridden by subclasses")


class PropDefiniteKB(KB):
    def __init__(self):
        super().__init__()
        self.inferred = set() # Initialize the inferred facts set as an instance variable
        
    def tell(self, sentence):
        # Parse and store rules and facts from the sentence 
        if '=>' in sentence:
            premise, conclusion = sentence.split('=>')
            premises = set(prem.strip() for prem in premise.split('&'))
            self.clauses.append((premises, conclusion.strip()))
        else:
            # Treat every standalone fact as a rule with an empty premise
            self.clauses.append((set(), sentence.strip()))
            self.inferred.add(sentence.strip()) # Directly add standalone facts to inferred

    def forward_chain(self):
        # Apply forward chaining to infer all possible facts
        added = True
        while added:
            added = False
            print(f"Current inferred facts: {self.inferred}") # Show current state of inferred facts
            for premises, conclusion in self.clauses:
                
                if premises.issubset(self.inferred):
                    if conclusion not in self.inferred:
                        self.inferred.add(conclusion)
                        added = True
                        print(f"Derived new fact: {conclusion}")
                    else:
                        print(f"Failed to derive new fact from premises: {premises} for conclusion: {conclusion}") # Debug Output
                else:
                    print(f"Failed to derive new fact from premises: {premises} for conclusion: {conclusion}")
            

    def ask(self, query):
        # Check if a query can be derived
        return query in self.inferred
    
    def retract(self, sentence):
        # Removes a sentence's clause from the KB
        self.clauses = [clause for clause in self.clauses if clause[1] != sentence]
        self.inferred.discard(sentence) # also remove from inferred if it was directly inferred

def main(file_path, method):
    kb, query = parse_kb_file(file_path)
    

    if method == "FC":
        kb.forward_chain() # Do forward chaining to derive possible facts
        derived_facts = sorted(kb.inferred)
         
        if query and kb.ask(query):
            print(f"YES: {', '.join(derived_facts)}")
        else:
            print(f"NO")
    else: 
        print(f"Unsupported Method: {method}")


    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: Python <script.py> <filename> <method>")
    else:
        filename = sys.argv[1]
        method = sys.argv[2]
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        main(file_path, method)