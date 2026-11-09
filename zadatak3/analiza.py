import pandas as pd

def pripremi_podatke_po_grupama(spojeno):
    dostupni_meseci = [1, 2, 3, 4, 5, 6, 7, 11, 12]

    broj_oglasa_po_grupi = (
        spojeno[["group_id", "ad_id"]]
        .drop_duplicates()
        .groupby("group_id")
        .size()
        .reset_index(name="broj_oglasa")
    )

    posete_po_grupama = (
        spojeno
        .groupby(["group_id", "mesec"], as_index=False)["broj_poseta"]
        .sum()
    )

    posete_po_grupama = posete_po_grupama[
        posete_po_grupama["mesec"].isin(dostupni_meseci)
    ]

    posete_po_grupama = posete_po_grupama.merge(
        broj_oglasa_po_grupi,
        on="group_id",
        how="left"
    )

    posete_po_grupama["prosek_poseta_po_oglasu"] = (
        posete_po_grupama["broj_poseta"]
        / posete_po_grupama["broj_oglasa"]
    )

    df_grupe = (
        posete_po_grupama
        .pivot(
            index="group_id",
            columns="mesec",
            values="prosek_poseta_po_oglasu"
        )
        .reindex(columns=dostupni_meseci, fill_value=0)
        .fillna(0)
        .reset_index()
    )

    df_grupe = df_grupe.melt(
        id_vars="group_id",
        var_name="mesec",
        value_name="prosek_poseta_po_oglasu"
    )

    kategorije_grupa = (
        spojeno[["group_id", "category_name"]]
        .dropna()
        .drop_duplicates("group_id")
    )

    df_grupe = df_grupe.merge(
        kategorije_grupa,
        on="group_id",
        how="left"
    )

    return df_grupe

def izracunaj_sezonalnost(df_grupe):
    sezonalnost = (
        df_grupe
        .groupby("group_id")["prosek_poseta_po_oglasu"]
        .agg(["max", "min", "mean"])
    )

    sezonalnost["razlika"] = (
        sezonalnost["max"] - sezonalnost["min"]
    )

    najvece_promene = (
        sezonalnost
        .sort_values("razlika", ascending=False)
        .head(5)
    )

    najmanje_promene = (
        sezonalnost
        .sort_values("razlika")
        .head(5)
    )

    return sezonalnost, najvece_promene, najmanje_promene