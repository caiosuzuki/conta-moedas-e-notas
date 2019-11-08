import os
import argparse
from count_coins_and_bills import count_coins_and_bills_in_image

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-i", "--img_dir", help="Path to the directory with the input images.")
args = arg_parser.parse_args()
images_directory = args.img_dir

hits = misses = 0
for filename in os.listdir(images_directory):
    number_of_coins_expected = int(filename.split('c')[0])
    number_of_bills_expected = int(filename.split('c')[1].split('n')[0])

    coins, bills = count_coins_and_bills_in_image(f'{images_directory}/{filename}', show_steps=False)

    if coins == number_of_coins_expected and bills == number_of_bills_expected:
        hits += 1
        print(f'Hit: {filename}')
    else:
        misses += 1
        print(f'Miss: {filename} - guessed: {coins}c{bills}n')
print(f'\nHits: {hits}\nMisses: {misses}')