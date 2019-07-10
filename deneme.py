import matplotlib.pyplot as plt
import pandas as pd
import six
import numpy as np


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors)])
    plt.savefig('deneme.png')




def splitDataFrameIntoSmaller(df, chunkSize = 10000):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        dd = df[i*chunkSize:(i+1)*chunkSize]
        if dd.empty:
            break
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])

    return listOfDf


list_of_dicts2 = [
            {'pid': 1, 'name': 'System Process'},
            {'pid': 4, 'name': 'System123'},
            {'pid': 110, 'name': 'svchost.exe'},
            {'pid': 20, 'name': 'smss.exe'},
            {'pid': 36, 'name': 'WSE.exe'},
            {'pid': 24, 'name': 'csrss.exe'}
        ]

df = pd.DataFrame(list_of_dicts2)






liste = splitDataFrameIntoSmaller(df, int(len(df)/3))

df1 = liste[0].reset_index(drop=True)
df2 = liste[1].reset_index(drop=True)
df3 = liste[2].reset_index(drop=True)

df = pd.concat([df1, df2, df3], axis=1)

render_mpl_table(df, header_columns=0, col_width=5.0)

fig, ax = plt.subplots(figsize=(12, 20)) # set size frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis
ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
tabla = pd.plotting.table(ax, df, loc='upper right', colWidths=[0.17]*len(df.columns))  # where df is your data frame
tabla.auto_set_font_size(True) # Activate set fontsize manually
#tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
tabla.scale(1.2, 1.2) # change size table

plt.savefig('table.png', transparent=True)



