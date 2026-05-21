import pandas as pd

# Load datasets
videos_df = pd.read_csv("videos.csv")
comments_df = pd.read_csv("comments.csv")

print("\n========== VIDEOS DATA ==========")
print(videos_df.head())

print("\n========== COMMENTS DATA ==========")
print(comments_df.head())

print("\n========== DATASET SHAPES ==========")
print("Videos shape:", videos_df.shape)
print("Comments shape:", comments_df.shape)

print("\n========== MISSING VALUES ==========")
print(comments_df.isnull().sum())

print("\n========== COMMENTS PER VIDEO ==========")
print(
    comments_df.groupby("video_id")
    .size()
    .sort_values(ascending=False)
)

print("\n========== SAMPLE COMMENTS ==========\n")

for comment in comments_df["comment_text"].head(10):
    print(comment)
    print("-" * 80)