import random
from typing import List, Dict

def generate_pairs(participants: List[str], n_giftees: int = 1, exclusions: List[tuple] = None) -> Dict[str, List[str]]:
    """
    Generates secret santa pairs.
    
    Args:
        participants: List of participant names.
        n_giftees: Number of people each person has to gift.
        exclusions: List of tuples (giver, excluded_receiver).
        
    Returns:
        A dictionary mapping giver -> list of receivers.
        Returns None if a valid pairing cannot be found after max retries.
    """
    if len(participants) <= n_giftees:
        raise ValueError(f"Not enough participants. Need at least {n_giftees + 1} for {n_giftees} giftees per person.")

    if exclusions is None:
        exclusions = []
        
    # Normalize exclusions for faster lookup
    # Map giver -> set of excluded receivers
    exclusion_map = {p: set() for p in participants}
    for giver, excluded in exclusions:
        if giver in exclusion_map:
            exclusion_map[giver].add(excluded)
            
    max_retries = 1000
    
    for _ in range(max_retries):
        pairs = {p: [] for p in participants}
        available_receivers = participants * n_giftees
        random.shuffle(available_receivers)
        
        valid_attempt = True
        
        temp_receivers = list(available_receivers)
        
        for giver in participants:
            receivers_for_giver = []
            for _ in range(n_giftees):
                # Find a valid receiver in temp_receivers
                # Valid means: 
                # 1. not self
                # 2. not already assigned to this giver
                # 3. not in exclusion list for this giver
                candidates = [
                    r for r in temp_receivers 
                    if r != giver 
                    and r not in receivers_for_giver
                    and r not in exclusion_map[giver]
                ]
                
                if not candidates:
                    valid_attempt = False
                    break
                
                # Pick one
                receiver = candidates[0] 
                receivers_for_giver.append(receiver)
                temp_receivers.remove(receiver) 
            
            if not valid_attempt:
                break
            
            pairs[giver] = receivers_for_giver
            
        if valid_attempt:
            return pairs
            
    return None
