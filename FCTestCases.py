import unittest
import string

from ForwardChainingActual import PropDefiniteKB 

class TestForwardChaining(unittest.TestCase):
    def setUp(self):
        self.kb = PropDefiniteKB()

    def test_basic_chain(self):
        # basic linear chain of implications 
        rules = [
            "A => B",
            "B => C",
            "C => D"
        ]
        for rule in rules:
            self.kb.tell(rule)
        self.kb.forward_chain() 
        self.assertTrue(self.kb.ask("D"))
    
    def test_complex_dependencies(self): 
        # Testing Complex Dependencies with Conjunctions
        rules = [
            "A & B => C",
            "C & D => E"
        ]
        facts = ["A", "B", "D"]
        for fact in facts:
            self.kb.tell(fact)
        for rule in rules:
            self.kb.tell(rule)
        self.kb.forward_chain()  
        self.assertTrue(self.kb.ask("E"))

    def test_circular_dependencies(self):
        rules = [ # Rules that create a loop 
            "A => B",
            "B => A"
        ]
        for rule in rules:
            self.kb.tell(rule)
        self.kb.tell("A")
        self.kb.forward_chain()
        self.assertTrue(self.kb.ask("B"))

    def test_negations_and_false_paths(self):
        # rules that should not be triggered
        rules = [
        "A => B",
        "B & C => D"
        ]
        self.kb.tell("A")
        for rule in rules:
            self.kb.tell(rule)
        self.kb.forward_chain()
        self.assertFalse(self.kb.ask("D"))

    def test_empty_and_minimal_input(self):
        # Empty Knowledge base test
        self.assertFalse(self.kb.ask("A"))

    def test_large_knowledge_base(self):
        # A large set of rules and facts
        previous_fact = None
        for letter in string.ascii_uppercase:
            fact = f"{letter}"
            if previous_fact:
                rule = f"{previous_fact} => {fact}"
                self.kb.tell(rule)
            previous_fact = fact
        self.kb.tell("A")  # Trigger the chain here
        self.kb.forward_chain()
        self.assertTrue(self.kb.ask("Z"))  # Check the last fact in the chain

if __name__ == '__main__':
    unittest.main()
