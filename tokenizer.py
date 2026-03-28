"""Class with BasicTokenizer implementation."""

import utils

MAX_BYTE_VALUE = 256

class BasicTokenizer:

    def __init__(self):
        self.vocab = {idx: idx for idx in range(MAX_BYTE_VALUE)}
        self.vocab_size = MAX_BYTE_VALUE

    def train(self,
              text: str,
              vocab_size: float):
        """Creates the vocabulary of bytes to merge based on BPE algorithm."""

        assert vocab_size >= 256, f'Vocab size {vocab_size} smaller than max value of a byte.'

        encoding_list = utils.text_to_uf8_byte_list(text)

        num_merges = vocab_size - MAX_BYTE_VALUE
        for i in range(num_merges):
            # should not try to perform a merge when < 2 values in encoding list
            if len(encoding_list) < 2:
                break
            most_common_pair = utils.get_most_common_consecutive_pair(encoding_list)
            self.vocab[MAX_BYTE_VALUE + i] = most_common_pair
            encoding_list = utils.merge_pair_in_encoding(encoding_list, most_common_pair, MAX_BYTE_VALUE + i)
            self.vocab_size += 1
        
    def encode(self, text):
        encoding = utils.text_to_uf8_byte_list(text)
        for vocab_idx in range(MAX_BYTE_VALUE, self.vocab_size):
            encoding = utils.merge_pair_in_encoding(encoding, self.vocab[vocab_idx], vocab_idx)
        return encoding

    def decode(self, encoding: list[int]):
        """Converts list of token ids to text."""
        byte_list = []
        for id in encoding:
            vocab_val = self.vocab[id]
            if isinstance(vocab_val, utils.Pair):
                byte_list.append(vocab_val.first)
                byte_list.append(vocab_val.second)
            else:
                byte_list.append(vocab_val)
        byte_sequence = bytes(byte_list)
        # Use replace to be robust to invalid byte sequences output by model
        return byte_sequence.decode('utf-8', errors='replace')