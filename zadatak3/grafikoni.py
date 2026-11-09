import matplotlib.pyplot as plt

def napravi_grafikone(df_grupe, najvece_promene):
    top_5 = najvece_promene.index

    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    axes = axes.flatten()

    for ax, group_id in zip(axes, top_5):
        podaci = df_grupe[
            df_grupe["group_id"] == group_id
        ].sort_values("mesec")

        ax.plot(
            podaci["mesec"],
            podaci["prosek_poseta_po_oglasu"],
            marker="o"
        )

        kategorija = podaci["category_name"].dropna()

        if len(kategorija) > 0:
            ax.set_title(
                f"{kategorija.iloc[0]} - grupa {group_id}"
            )
        else:
            ax.set_title(f"Grupa {group_id}")

        ax.set_xlabel("Mesec")
        ax.set_ylabel("Prosečan broj poseta po oglasu")
        ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 11, 12])

    for ax in axes[len(top_5):]:
        ax.remove()

    plt.tight_layout()

    plt.savefig(
        "zadatak3/top_5_grupa_posete.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()