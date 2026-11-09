import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pregledi = pd.read_csv("zadatak3/ad_views_by_month.csv")
kategorije = pd.read_csv("zadatak3/ad_categories.csv")

# Id u oba fajla mroa da bude istog tipa i bez razmaka ili zareza
pregledi["ad_id"] = (
    pregledi["ad_id"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

kategorije["ad_id"] = (
    kategorije["ad_id"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

spojeno = pregledi.merge(
    kategorije,
    on="ad_id",
    how="inner"
)

print(spojeno.head())


posete_po_kategorijama = (
    spojeno
    .groupby(
        ["category_name", "mesec"],
        as_index=False
    )["broj_poseta"].sum()
)

print("\nPosete po kategorijama i mesecima:")
print(posete_po_kategorijama.head())

# U app_hits_v2 postoje podaci samo za ove mesece
dostupni_meseci = [1, 2, 3, 4, 5, 6, 7, 11, 12]

posete_po_kategorijama = posete_po_kategorijama[
    posete_po_kategorijama["mesec"].isin(dostupni_meseci)
]


df_posete = (
    posete_po_kategorijama
    .pivot(
        index="category_name",
        columns="mesec",
        values="broj_poseta"
    )
    .reindex(columns=dostupni_meseci, fill_value=0)
    .fillna(0)
    .reset_index()
)

df_posete = df_posete.melt(
    id_vars="category_name",
    var_name="mesec",
    value_name="broj_poseta"
)

print("\nTabela sa posetama:")
print(df_posete.head(15))

sezonalnost_posete = (
    df_posete
    .groupby("category_name")["broj_poseta"]
    .agg(["max", "min", "mean"])
)

sezonalnost_posete["razlika"] = (
    sezonalnost_posete["max"]
    - sezonalnost_posete["min"]
)

kategorije_sa_najvecom_promenom = (
    sezonalnost_posete
    .sort_values("razlika", ascending=False)
    .head(5)
)

print("\nKategorije sa najvećom promenom posećenosti:")
print(kategorije_sa_najvecom_promenom)

kategorije_sa_najmanjom_promenom = (
    sezonalnost_posete
    .sort_values("razlika")
    .head(5)
)

print("\nKategorije sa najmanjom promenom posećenosti:")
print(kategorije_sa_najmanjom_promenom)

top_5 = kategorije_sa_najvecom_promenom.index

fig, axes = plt.subplots(3, 2, figsize=(12, 10))
axes = axes.flatten()

for ax, category in zip(axes, top_5):
    podaci = df_posete[
        df_posete["category_name"] == category
    ].sort_values("mesec")

    sns.lineplot(
        data=podaci,
        x="mesec",
        y="broj_poseta",
        marker="o",
        ax=ax
    )

    ax.set_title(category)
    ax.set_xlabel("Mesec")
    ax.set_ylabel("Broj poseta")
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 11, 12])

for ax in axes[len(top_5):]:
    ax.remove()

plt.tight_layout()

plt.savefig(
    "zadatak3/top_5_kategorija_posete.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Za Data Studio
df_posete.to_csv(
    "zadatak3/category_month_visits.csv",
    index=False
)