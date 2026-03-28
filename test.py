"""Basic test of tokenizer implementation."""

from tokenizer import BasicTokenizer

tokenizer = BasicTokenizer()
with open('test_data/taylorswift.txt', 'r', encoding='utf-8') as file:
        train_data = file.read()

tokenizer.train(train_data, vocab_size=512)

TEST_STR = "안녕하세요 👋 (hello in Korean!)"

print(f'Test String Pre-Reconstruction: {TEST_STR}')
encoded_str = tokenizer.encode(TEST_STR)
print(f'Encoded Str: {encoded_str}')
reconstructed_str = tokenizer.decode(encoded_str)
print(f'Test Str After Reconstruction: {reconstructed_str}')