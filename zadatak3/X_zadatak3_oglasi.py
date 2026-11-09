import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("zadatak3/category_month.csv")

print(df.head())
df.info()

print("Broj kategorija:", df["category_name"].nunique())

print("\nBroj meseci po kategoriji:")
print(df["category_name"].value_counts().head(10))

#Dodajem mesece koji nedostaju i popunjavam ih nulama
df = (
    df
    .pivot(
        index="category_name",
        columns="mesec",
        values="broj_oglasa"
    )
    .reindex(columns=range(1, 13), fill_value=0)
    .fillna(0)
    .reset_index()
)

#Iznad je izmenjena struktura tabele pa je vracam u originalni oblik
df = df.melt(
    id_vars="category_name",
    var_name="mesec",
    value_name="broj_oglasa"
)

sezonalnost_sve = df.groupby("category_name")["broj_oglasa"].agg(["max", "min", "mean"])
sezonalnost_sve["razlika"] = sezonalnost_sve["max"] - sezonalnost_sve["min"]


kategorije_sa_najvecom_promenom = (
    sezonalnost_sve
    .sort_values("razlika", ascending=False)
    .head(5)
)
print("\nKategorije sa najvećom promenom:",kategorije_sa_najvecom_promenom)

kategorije_sa_najmanjom_promenom = (
    sezonalnost_sve
    .sort_values("razlika")
    .head(5)
)

print("\nKategorije sa najmanjom promenom:", kategorije_sa_najmanjom_promenom)

top_5 = kategorije_sa_najvecom_promenom.index

#Prostor za grafikone
fig, axes = plt.subplots(3, 2, figsize=(12, 10))
axes = axes.flatten()

for ax, category in zip(axes, top_5):
    podaci = df[df["category_name"] == category]

    sns.lineplot(
        data=podaci,
        x="mesec",
        y="broj_oglasa",
        marker="o",
        ax=ax
    )

    ax.set_title(category)
    ax.set_xlabel("Mesec")
    ax.set_ylabel("Broj oglasa")
    ax.set_xticks(range(1, 13))


# Za prazno sesto mesto
for ax in axes[len(top_5):]:
    ax.remove()

plt.tight_layout()

plt.savefig(
    "zadatak3/top_5_kategorija.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()