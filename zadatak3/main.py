import podaci
from analiza import (
    pripremi_podatke_po_grupama,
    izracunaj_sezonalnost
)
from grafikoni import napravi_grafikone

pregledi = podaci.ucitaj_posete_iz_clickhouse()
oglasi = podaci.ucitaj_oglase_iz_mysql()

pregledi["ad_id"] = (
    pregledi["ad_id"]
    .astype(str)
    .str.strip()
)

oglasi["ad_id"] = (
    oglasi["ad_id"]
    .astype(str)
    .str.strip()
)

oglasi = oglasi.drop_duplicates(
    subset="ad_id"
)

spojeno = pregledi.merge(
    oglasi,
    on="ad_id",
    how="inner"
)

df_grupe = pripremi_podatke_po_grupama(spojeno)

(
    _,
    najvece_promene,
    najmanje_promene
) = izracunaj_sezonalnost(df_grupe)

print("\nGrupe sa najvećom promenom posećenosti:")
print(najvece_promene)

print("\nGrupe sa najmanjom promenom posećenosti:")
print(najmanje_promene)

napravi_grafikone(
    df_grupe,
    najvece_promene
)

df_grupe.to_csv(
    "zadatak3/posecenost_grupa_po_mesecima.csv",
    index=False
)