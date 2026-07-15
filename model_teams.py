import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/f1_teams_complete_full_names.csv")

df['constructor_championships'] = df['constructor_championships'].fillna(0)
df["total_podiums"] = df["total_podiums"].fillna(0)
df["total_points"] = df["total_points"].fillna(
    df['total_points'].mean()
)
df["last_year"] = df["last_year"].fillna(
    df['last_year'].mode()[0]
)
df["first_year"] = df["first_year"].fillna(
    df['first_year'].mode()[0]
)
df["win_rate"] = df["win_rate"].fillna(
    df['win_rate'].mean()
)
df["podium_rate"] = df["podium_rate"].fillna(
    df['podium_rate'].mean()
)

current_year = 2026
df['last_year'] = df['last_year'].replace(
    "Still on the goddamn grid",
    current_year
)
df['last_year'] = pd.to_numeric(df['last_year'])

total_years = df['last_year'] - df['first_year'] + 1
championship_per_year = df['constructor_championships'] / total_years
points_per_year = df['total_points'] / total_years
podiums_per_year = df['total_podiums'] / total_years

df["total_years"] = total_years
df["championship_per_year"] = championship_per_year
df["points_per_year"] = points_per_year
df["podiums_per_year"] = podiums_per_year

data = df[["total_years", "championship_per_year", "points_per_year", "podiums_per_year"]]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(scaled_data)

plt.scatter(
    df["points_per_year"],
    df["podiums_per_year"],
    c=df["Cluster"],
    s=100,
    alpha=0.8
)

plt.xlabel("Points Per Year")
plt.ylabel("Podiums Per Year")
plt.title("F1 Constructor Clusters")

plt.grid(alpha=0.3)

plt.show()

result = pd.DataFrame({
    "Team": df["name"],
    "Group": "Group " + (df["Cluster"] + 1).astype(str)
    })

result.to_csv("data/Team_clusters.csv", index=False)