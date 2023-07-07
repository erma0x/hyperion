import json

configurations = []
GENERATION_SIZE = 100

for i in range(GENERATION_SIZE):
    try:
        with open(f'strategies/{i}.txt', 'r') as f:
            configuration = json.load(f)
            configurations.append(configuration) 
    except:
        print('error')

sorted_list = sorted(configurations, key=lambda k: k['final_equity'], reverse=True)

from pprint import pprint
pprint(sorted_list[:10])