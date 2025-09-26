import pandas as pd
from itertools import product
import torch
from sentence_transformers import CrossEncoder

# --------------------------
# 1️⃣ Load CSVs
# --------------------------
df_a = pd.read_csv("mistersavage_reddit.csv")
df_b = pd.read_csv("J_Kenji_Lopez-Alt_reddit.csv")

posts_a = df_a['text'].fillna("").astype(str).tolist()
posts_b = df_b['text'].fillna("").astype(str).tolist()

pairs_cross = list(product(posts_a, posts_b))

# --------------------------
# 2️⃣ Load Cross-Encoder
# --------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

cross_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    device=device
)

# --------------------------
# 3️⃣ Predict with FP16 if GPU
# --------------------------
batch_size = 8 if device == "cuda" else 2

if device == "cuda":
    # Use autocast for FP16 inference
    scores_cross = []
    with torch.cuda.amp.autocast():
        for i in range(0, len(pairs_cross), batch_size):
            batch = pairs_cross[i:i+batch_size]
            scores_cross.extend(cross_model.predict(batch))
else:
    # CPU inference
    scores_cross = cross_model.predict(pairs_cross, batch_size=batch_size)

# --------------------------
# 4️⃣ Save results
# --------------------------
results = []
for (post_a, post_b), score in zip(pairs_cross, scores_cross):
    results.append({
        "PostA": post_a,
        "PostB": post_b,
        "CrossEncoderScore": float(score)
    })

df_results = pd.DataFrame(results)
df_results.to_csv("cross_encoder_results.csv", index=False)
print("✅ Cross-encoder scoring complete. Saved to 'cross_encoder_results.csv'")
