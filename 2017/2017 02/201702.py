import pandas as pd

df = pd.read_table("input.txt", header=None, dtype="int")
df["min2max"] = df.max(axis=1) - df.min(axis=1)
print(df["min2max"].sum())


# %% Part 2
def find_multiple_pairs(nums):
    for a in nums:
        for b in nums:
            if a > b and a % b == 0:
                return a, b, int(a/b)


for i in df.index:
    nums = df.loc[i, :15]
    _, _, df.loc[i, "part2ans"] = find_multiple_pairs(nums)

print(df["part2ans"].sum())
