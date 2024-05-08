import heapq
import itertools
import random
import sys
import os
from collections import defaultdict, Counter

import networkx as nx
from utils import remove_all, unique, first, probability, isnumber, issequence, Expr, expr, subexpressions, extend, infix_ops

def parse_kb_file(file_path): # Parses the knowledge base file
    kb = PropDefiniteKB() # Create instance of PropDefiniteKB
    query = None # Initialize Query with None to store any queries found in the file
    try: 
        with open(file_path, 'r') as file: # Opens the file in read mode
            mode = None # Initialize mode to None which will be used to determine the current section of the file tell or ask
            for line in file: # Iterate through each line in the file
                line = line.strip() # Strips the whitespace from the start and end of the line
                if 'TELL' in line: 
                    mode= 'tell' # Set mode to 'tell' when the line contains tell
                    continue # Skips to the next iteration
                elif 'ASK' in line:
                    mode = 'ask' # Sets mode to 'ask' when the line contains ask
                    continue # Skips the line with ASK 
                
                if mode == 'tell' and line:
                    instructions = line.split(';') # Splits the line into separate instructions at each semicolon
                    for instruction in instructions:
                        if instruction.strip(): #Ensure the instruction is not empty
                            kb.tell(instruction.strip())  # Add the instruction to the knowledge base
                elif mode == 'ask' and line: # Store the line as a query if in 'ask' mode and the line is not empty
                   
                 
                    query = line.strip() # Directly store the query line
    except IOError:
        print(f"Error opening or reading the file: {file_path}") # Error message
    return kb, query



class KB: # Base Class for KB
    def __init__(self):
        self.clauses = [] # Initialize empty list to store kb clauses
    def tell(self, sentence): 
        # Adds a sentence to the KB
        raise NotImplementedError("This method should be overridden by subclasses")
    def ask(self, query):
        # Asks the KB if a query can be derived
        raise NotImplementedError("This method should be overridden by subclasses")
    def retract(self, sentence):
        # Removes a sentence from KB
        raise NotImplementedError("This method should be overridden by subclasses")


class PropDefiniteKB(KB): # Subclass of KB which will handle propositional definite kb
    def __init__(self):
        super().__init__() # Call the initializer of the base class
        self.inferred = set() # Initialize the inferred facts set as an instance variable
        
    def tell(self, sentence):   # Parse and store rules and facts from the sentence 
        if '=>' in sentence:
            premise, conclusion = sentence.split('=>') # Split sentence into premise and conclusion at =>
            premises = set(prem.strip() for prem in premise.split('&'))  # Create set of premises split at &
            self.clauses.append((premises, conclusion.strip())) # Add rule to the kb
        else:
            self.clauses.append((set(), sentence.strip())) # Treats every standalone fact as a rule with an empty premise
            self.inferred.add(sentence.strip()) # Directly add standalone facts to inferred

    def forward_chain(self): # Apply forward chaining to infer all possible facts
        added = True
        while added:
            added = False # Reset flag to false
            print(f"Current inferred facts: {self.inferred}") # Show current state of inferred facts
            for premises, conclusion in self.clauses:
                
                if premises.issubset(self.inferred): # Checks if all premises are already inferred
                    if conclusion not in self.inferred: # Checks if conclusion is not already inferred
                        self.inferred.add(conclusion) # Adds the conclusion to the inferred facts
                        added = True # Sets the flag to True to show new fact was inferred
                        print(f"Derived new fact: {conclusion}")  # Debug Statements here;
                    else:
                        print(f"Failed to derive new fact from premises: {premises} for conclusion: {conclusion}") # Debug Output
                else:
                    print(f"Failed to derive new fact from premises: {premises} for conclusion: {conclusion}")
            

    def ask(self, query):
        return query in self.inferred # Check if a query can be derived
    
    def retract(self, sentence):
        self.clauses = [clause for clause in self.clauses if clause[1] != sentence] # Removes a sentence's clause from the KB
        self.inferred.discard(sentence) # remove from inferred if it was directly inferred


def main(file_path, method): 
    kb, query = parse_kb_file(file_path) # Parsing here
    

    if method == "FC":
        kb.forward_chain() # Do forward chaining to infer facts
        derived_facts = sorted(kb.inferred) # Sort the inferred facts
         
        if query and kb.ask(query): # Check if the query can be derived
            print(f"YES: {', '.join(derived_facts)}") # Prints the results if query can be derived
        else:
            print(f"NO") #Prints no if the query cannot be derived
    else: 
        print(f"Unsupported Method: {method}") # Print an error message if the method is not supported


    

if __name__ == "__main__": # Script starts
    if len(sys.argv) != 3:
        print("Usage: Python <script.py> <filename> <method>") # Prints out a validation statement
    else:
        filename = sys.argv[1]
        method = sys.argv[2]
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename) # makes the file path
        main(file_path, method) # Calls the main func
        