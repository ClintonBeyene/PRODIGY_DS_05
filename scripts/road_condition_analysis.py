def road_condition_analysis(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # Define plot
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(nrows=4, ncols=2, figsize=(16, 20))

    # Define conditions and colors
    road_conditions = ['Bump', 'Crossing', 'Give_Way', 'Junction', 'Stop', 'No_Exit', 'Traffic_Signal', 'Turning_Loop']
    colors = [
        ('#1f77b4', '#ff7f0e'), ('#2ca02c', '#d62728'), ('#9467bd', '#8c564b'), 
        ('#e377c2', '#7f7f7f'), ('#bcbd22', '#17becf'), ('#ff9896', '#aec7e8'),
        ('#ffbb78', '#98df8a'), ('#c5b0d5', '#c49c94')
    ]

    # Function to add percentage labels
    def func(pct, allvals):
        absolute = int(round(pct/100*np.sum(allvals), 2))
        return "{:.2f}%\n({:,d} Cases)".format(pct, absolute)

    # Plotting
    count = 0
    for ax, condition, color in zip([ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8], road_conditions, colors):
        size = list(df[condition].value_counts())
        if len(size) != 2:
            size.append(0)
        labels = ['False', 'True']
        ax.pie(size, labels=labels, colors=color, autopct=lambda pct: func(pct, size),
            labeldistance=1.1, textprops={'fontsize': 12}, explode=[0, 0.2])
        title = f'\nPresence of {condition}'
        ax.set_title(title, fontsize=18, color='darkblue')
        count += 1

    plt.tight_layout()
    plt.show()