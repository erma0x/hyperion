import json

configs = {'1':'2','final_equity':5}

with open(f'{i}.txt', 'w') as f:
    json.dump(configs, f)
