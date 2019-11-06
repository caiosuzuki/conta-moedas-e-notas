import os
from test import count_coins_and_bills_in_image

images_directory = './notas-e-moedas-exemplo'

hits = misses = 0
for filename in os.listdir(images_directory):
    print(os.path.basename(filename))
    number_of_coins_expected = int(filename.split('c')[0])
    number_of_bills_expected = int(filename.split('c')[1].split('n')[0])
    print(f'number of coins expected for {filename}: {number_of_coins_expected}')
    print(f'number of bills expected for {filename}: {number_of_bills_expected}')
    coins, bills = count_coins_and_bills_in_image(f'{images_directory}/{filename}')
    # if coins == number_of_coins_expected and bills == number_of_bills_expected:
    if coins == number_of_coins_expected and bills == 0:
        hits += 1
    else:
        misses += 1
    print(f'Hits: {hits}\nMisses: {misses}')