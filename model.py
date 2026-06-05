import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
df = pd.read_csv("data/F1Drivers_Dataset.csv")

columns_to_drop = [
    "Nationality",
    "Seasons",
    "Championship Years",
    "Decade",
    "Active",
    "Champion",
    "Pole_Positions",
    "Race_Wins",
    "Podiums",
    "Fastest_Laps",
    "Points",
    "Race_Entries",
    "Race_Starts",
    "Championships",
    "Points_Per_Entry",
    "Years_Active"
]

df = df.drop(columns=columns_to_drop)

data = df.drop(columns=["Driver"])

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(scaled_data)

plt.scatter(
    df["Win_Rate"],
    df["Podium_Rate"],
    c=df["Cluster"]
)

plt.xlabel("Win Rate")
plt.ylabel("Podium Rate")
plt.title("F1 Driver Clusters")

plt.show()

for cluster in sorted(df["Cluster"].unique()):
    print(f"\nCluster {cluster}")
    print(df[df["Cluster"] == cluster]["Driver"].tolist())