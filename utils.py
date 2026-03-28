"""Utils to help with tokenization."""

from collections import defaultdict
from dataclasses import dataclass
from typing import List

@dataclass
class Pair:
    first: int
    second:int

def text_to_uf8_byte_list(text: str) -> List[int]:
    """Converts text to list of bytes based on utf-8 encoding."""
    byte_encoding = text.encode('utf-8')
    return list(map(int, byte_encoding))

def get_most_common_consecutive_pair(encoding_list: List[int]) -> Pair:
    """
    Returns most pair of most common consecutive values in current
    encoding list.
    """
    counts = defaultdict(int)
    for first, second in zip(encoding_list[:-1], encoding_list[1:]):
        counts[(first, second)] += 1
    max_tuple =  max(counts, key=counts.get)
    return Pair(max_tuple[0], max_tuple[1])

def merge_pair_in_encoding(encoding_list: List[int],
                           pair_to_merge: Pair,
                           val_to_replace_pair: int) -> List[int]:
    merged_encoding = []
    curr_idx = 0
    while curr_idx < len(encoding_list):
        if (encoding_list[curr_idx] == pair_to_merge.first
            and curr_idx < len(encoding_list) - 1
            and encoding_list[curr_idx+1] == pair_to_merge.second):
            merged_encoding.append(val_to_replace_pair)
            curr_idx += 1
        else:
            merged_encoding.append(encoding_list[curr_idx])
            curr_idx += 1
    return merged_encoding
