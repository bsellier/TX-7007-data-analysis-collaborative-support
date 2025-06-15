import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

aactions_df = pd.read_csv(
    "data_clean/Toutes_Seances/5_AtomicAction_Coding_Vott/DI05_A19_atomic_actions.csv"
)

aactions_df = aactions_df.loc[aactions_df["seance"] == "Seance_2_FAST_Valise/"]

aactions_df["box_center_x"] = (
    aactions_df["bounding_box_left"] + aactions_df["bounding_box_width"] / 2
)
aactions_df["box_center_y"] = (
    aactions_df["bounding_box_top"] + aactions_df["bounding_box_height"] / 2
)

fig, ax = plt.subplots()
ax.set_xlim(0, 960)
ax.set_ylim(0, 540)
plt.gca().set_aspect("equal", adjustable="box")

ax.invert_yaxis()
ax.set_xlabel("box_center_x")
ax.set_ylabel("box_center_y")
fig.set_figwidth(13)

aactions_pp_df = aactions_df.loc[
    (aactions_df["atomic_action_type"] == "personnepersonne")
    | (aactions_df["atomic_action_type"] == "personneobjet")
]
# print(aactions_df.tag_name.unique().tolist())


colors = {
    "talk to person": "tab:blue",
    "look at person": "tab:orange",
    "laugh": "tab:green",
    "listen to": "tab:red",
    "talk to group": "tab:purple",
    "point at person": "tab:brown",
    "read": "teal",
    "look at notebook or smartphone": "tab:pink",
    "look at table": "tab:gray",
    "write on the table": "tab:olive",
    "use portal": "tab:cyan",
    "point at object": "darkslategrey",
    "look at board": "goldenrod",
    "write on the board": "aqua",
    "move post-it": "darkred",
    "take notes": "midnightblue",
    "look at slide": "bisque",
}


def animate(i):
    # ax.cla()
    x_data = aactions_pp_df.loc[
        (aactions_pp_df["timestamp"] == i),
        "box_center_x",
    ]
    y_data = aactions_pp_df.loc[
        (aactions_pp_df["timestamp"] == i),
        "box_center_y",
    ]

    tag_names = aactions_pp_df.loc[
        (aactions_pp_df["timestamp"] == i),
        "tag_name",
    ]

    ax.scatter(x_data, y_data, c=tag_names.map(colors))
    handles = [
        Line2D(
            [0], [0], marker="o", color="w", markerfacecolor=v, label=k, markersize=8
        )
        for k, v in colors.items()
    ]

    ax.set_title(f"timestamp : {int(i)}")

    ax.legend(
        title="tag name", handles=handles, bbox_to_anchor=(1, 1), loc="upper left"
    )


# graph.legend(loc="center left", bbox_to_anchor=(1, 0.5))

# Pour éviter les duplicatas
# handles, labels = plt.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))
# plt.legend(
#     by_label.values(), by_label.keys(), loc="center left", bbox_to_anchor=(1, 0.7)
# )


timestamps = aactions_df["timestamp"].unique().tolist()
timestamps = sorted(timestamps)

ani = animation.FuncAnimation(fig, animate, frames=timestamps, repeat=False)

# ani.save("records/seance2/perspers_persobj_essai1.mp4", writer="ffmpeg", fps=20)

plt.show()
