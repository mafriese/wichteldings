import unittest
import json
from pairing import generate_pairs
from crypto import encrypt_data, decrypt_data

class TestWichteln(unittest.TestCase):
    def test_pairing_simple(self):
        participants = ['A', 'B', 'C', 'D']
        pairs = generate_pairs(participants, n_giftees=1)
        self.assertIsNotNone(pairs)
        self.assertEqual(len(pairs), 4)
        
        all_receivers = []
        for giver, receivers in pairs.items():
            self.assertEqual(len(receivers), 1)
            self.assertNotEqual(giver, receivers[0])
            all_receivers.extend(receivers)
            
        self.assertEqual(set(all_receivers), set(participants))

    def test_pairing_two_giftees(self):
        participants = ['A', 'B', 'C', 'D', 'E']
        pairs = generate_pairs(participants, n_giftees=2)
        self.assertIsNotNone(pairs)
        
        for giver, receivers in pairs.items():
            self.assertEqual(len(receivers), 2)
            self.assertNotIn(giver, receivers)
            self.assertEqual(len(set(receivers)), 2) # Unique receivers

    def test_pairing_impossible(self):
        # 3 people, 3 giftees each -> impossible (can't gift self)
        participants = ['A', 'B', 'C']
        with self.assertRaises(ValueError):
            generate_pairs(participants, n_giftees=3)

    def test_pairing_with_exclusions(self):
        participants = ['A', 'B', 'C']
        # A cannot gift B. So A must gift C (if n=1).
        exclusions = [('A', 'B')]
        pairs = generate_pairs(participants, n_giftees=1, exclusions=exclusions)
        self.assertIsNotNone(pairs)
        self.assertEqual(pairs['A'], ['C'])
        
        # Check others
        # B can gift A or C. C can gift A or B.
        # But since A->C, C cannot gift A (if we want a perfect cycle? No, cycles aren't required, just valid mapping)
        # Wait, if A->C, then C must gift B (because C!=C, C!=A is allowed but let's see)
        # If A->C, remaining for B are {A}, remaining for C are {B}.
        # So B->A, C->B.
        # Let's just check the constraints.
        for giver, receivers in pairs.items():
            for r in receivers:
                self.assertNotEqual(giver, r)
                if giver == 'A':
                    self.assertNotEqual(r, 'B')

    def test_pairing_impossible_exclusion(self):
        participants = ['A', 'B']
        # A cannot gift B. A cannot gift A. -> A has no one to gift.
        exclusions = [('A', 'B')]
        pairs = generate_pairs(participants, n_giftees=1, exclusions=exclusions)
        self.assertIsNone(pairs)

    def test_encryption(self):
        data = {'giver': 'Alice', 'receivers': ['Bob', 'Charlie']}
        json_str = json.dumps(data)
        token = encrypt_data(json_str)
        
        decrypted_str = decrypt_data(token)
        self.assertEqual(json_str, decrypted_str)
        
        decrypted_data = json.loads(decrypted_str)
        self.assertEqual(decrypted_data, data)

if __name__ == '__main__':
    unittest.main()
