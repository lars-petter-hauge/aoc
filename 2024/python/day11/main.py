import sys
from functools import cache

TEST_INPUT = "125 17"
with open(sys.argv[1]) as fh:
    content = fh.read()

@cache
def num_stones(stone, blinks):
    if blinks == 0:
        return 1
    if stone == 0:
        return num_stones(1, blinks-1)

    str_stone = str(stone)
    if len(str_stone)%2 == 0:
        middel = len(str_stone)//2
        a,b = str_stone[:middel],str_stone[middel:]
        return num_stones(int(a), blinks-1) + num_stones(int(b), blinks -1)
    
    return num_stones(stone * 2024, blinks-1)

# import numpy as np
# import pandas as pd
# import plotly.express as px
# print(sum([num_stones(int(c),25) for c in TEST_INPUT.split()]))
# y=[0,0,0]
# diffs = []
# for i in range(100):
#     y.append(np.log(sum([num_stones(int(c),i) for c in content.split()])))
#     a = (y[-1]-y[-2])
#
#     print(f"{i}) diff: {(y[-2]-a)-y[-3]}") 
#     diffs.append((y[-2]-a)-y[-3])
#
# diffs = diffs[3:]
# x = range(len(diffs))
# df = pd.DataFrame({"actual":diffs},index=x)
# fig = px.scatter(df)
# fig.show()
