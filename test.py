import ast

product_dict = {}

i = 0

with open('C:/Users/Administrateur/Documents/Click&Boat/Thomas/boat24/boat24/spiders/save.json') as data_file:
    for z in data_file:
        z= ast.literal_eval(z)
        print z["Length"]