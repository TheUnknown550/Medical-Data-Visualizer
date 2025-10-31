import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import data
df = pd.read_csv("medical_examination.csv")

# 2. Add 'overweight' column
# calculate BMI = weight / (height/100)^2
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2)).apply(lambda x: 1 if x > 25 else 0)

# 3. Normalize cholesterol(0:good, 1:bad)
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
# Normalize gluc (0:good, 1:bad)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# 4. Draw Plot
def draw_cat_plot():
    # 5. Create DataFrame for category plot using pd.melt
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    )


    # 6. Group and reformat catplot
    df_cat = df_cat.groupby(['cardio', 'variable'])['value'].mean().reset_index()
    

    # 7. Create the catplot
    fig = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        col='cardio',
        hue='value',   
        kind='bar'
    ).fig


    # 8. Save and return figure
    fig.savefig('catplot.png')
    return fig


# 10. Draw the heat map
def draw_heat_map():
    # 11. Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. Calculate the correlation matrix
    corr = df_heat.corr()

    # 13. Create the mask
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Create the figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15. Draw the heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        vmax=0.3,
        vmin=-0.1,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )

    # 16. Save and return figure
    fig.savefig('heatmap.png')
    return fig
