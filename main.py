import pandas as pd
import numpy as np
import plotly.graph_objs as go



# set graph variables
MARGIN = {"t": 120, "r": 250, "b": 40, "l": 40}
WIDTH = 1280
HEIGHT = 720
PLOT_BGCOLOUR = "#F8F9F9"
COLOUR_1 = '#fa6161' 
COLOUR_2 = '#faad61'
COLOUR_3 = '#fafa61'
COLOUR_4 = '#ad61fa'
COLOUR_5 = '#61fad4' 
COLOUR_6 = '#636efa' 



#import data
df = pd.read_csv("Global Electric Vehicle Market Share.csv")

#make the dataframe long so it's easier to work with
df = pd.melt(df, id_vars = ["Brands"], value_vars = ["Q2 2021", "Q3 2021", "Q4 2021", "Q1 2022", "Q2 2022", "Q3 2022"],
            value_name = "MarketShare", var_name = "Quarter")

#add on the quarter start date for each quarter
df["QuarterStartDate"] = df["Quarter"].map({"Q2 2021": "2021-04-01", "Q3 2021": "2021-07-01", "Q4 2021": "2021-10-01", "Q1 2022": "2022-01-01", "Q2 2022": "2022-04-01",
"Q3 2022": "2022-10-01"})

#convert the market share into a decimal from a string
df["MarketShareReformat"] = df["MarketShare"].str.replace("%", "").astype(int).div(100)

#filter only the most recent quarter
df_heatmap = df.loc[df["Quarter"] == "Q3 2022"].copy()

#create the order each category should appear on the heatmp
df_heatmap["Order"] = 1
df_heatmap.loc[df_heatmap["Brands"] == "Volkswagen", "Order"] = 3
df_heatmap.loc[df_heatmap["Brands"] == "GAC Motor", "Order"] = 4
df_heatmap.loc[df_heatmap["Brands"] == "Tesla", "Order"] = 2
df_heatmap.loc[df_heatmap["Brands"] == "Wuling", "Order"] = 5
df_heatmap.loc[df_heatmap["Brands"] == "Others", "Order"] = 6

#sort each brand
df_heatmap.sort_values(by = "Order", inplace = True)

#to create a waffle chart we need to do a hack-y workaround on the heatmap function
#create a 10 x 10 array where each value in the array will represent a different brand, and the number of values for each brand will be equivalent to the market share %
brand_squares = [int(perc * 100) for perc in df_heatmap["MarketShareReformat"]]
brand_array = [np.ones(squares) * (i+1) for i, squares in enumerate(brand_squares)]

data = np.concatenate(brand_array)
data = data.reshape(10, 10)
data = data.transpose() # Transpose the array

#assign a colour for each car brand
df_heatmap["Colour"] = COLOUR_1
df_heatmap.loc[df_heatmap["Brands"] == "Volkswagen", "Colour"] = COLOUR_2
df_heatmap.loc[df_heatmap["Brands"] == "GAC Motor", "Colour"] = COLOUR_3
df_heatmap.loc[df_heatmap["Brands"] == "Tesla", "Colour"] = COLOUR_4
df_heatmap.loc[df_heatmap["Brands"] == "Wuling", "Colour"] = COLOUR_5
df_heatmap.loc[df_heatmap["Brands"] == "Others", "Colour"] = COLOUR_6 


# create an array of the colours and the lower and upper bounds for each colour
colours = [    [0, df_heatmap.loc[df_heatmap["Brands"] == "BYD Auto", "Colour"].iloc[0]],
            [0.166, df_heatmap.loc[df_heatmap["Brands"] == "BYD Auto", "Colour"].iloc[0]],
            [0.166, df_heatmap.loc[df_heatmap["Brands"] == "Tesla", "Colour"].iloc[0]],
            [0.333, df_heatmap.loc[df_heatmap["Brands"] == "Tesla", "Colour"].iloc[0]],

            [0.333, df_heatmap.loc[df_heatmap["Brands"] == "Volkswagen", "Colour"].iloc[0]],
            [0.5, df_heatmap.loc[df_heatmap["Brands"] == "Volkswagen", "Colour"].iloc[0]],

            [0.5, df_heatmap.loc[df_heatmap["Brands"] == "GAC Motor", "Colour"].iloc[0]],
            [0.666, df_heatmap.loc[df_heatmap["Brands"] == "GAC Motor", "Colour"].iloc[0]],
            [0.666, df_heatmap.loc[df_heatmap["Brands"] == "Wuling", "Colour"].iloc[0]],
            [0.833, df_heatmap.loc[df_heatmap["Brands"] == "Wuling", "Colour"].iloc[0]],
            [0.833, df_heatmap.loc[df_heatmap["Brands"] == "Others", "Colour"].iloc[0]],
            [1, df_heatmap.loc[df_heatmap["Brands"] == "Others", "Colour"].iloc[0]]
]



fig = go.Figure()


fig.add_trace(go.Heatmap(z=data,
                    xgap = 3,
                    ygap = 3, 
                    colorscale = colours,
                    
                    showscale = False))

fig.update_layout(plot_bgcolor = PLOT_BGCOLOUR,
                    paper_bgcolor = PLOT_BGCOLOUR,
                    width = WIDTH,
                    height = HEIGHT,
                    margin = MARGIN,
                    )

#hide the tick marks on the x and y axes
fig.update_xaxes(showticklabels = False)
fig.update_yaxes(showticklabels = False)





# Add text annotations to the figure
for index, row in df_heatmap.iterrows():
    fig.add_annotation(
        xref = "paper",
        yref = "y",
        x = 1.13,
        y= 10 - row["Order"]-0.5,
        text=row["Brands"],
        showarrow=False,
        font=dict(size=16),
        xanchor="center",
        yanchor="middle",
    )


for index, row in df_heatmap.iterrows():
    fig.add_shape(
        type="rect",
        x0=1.07, y0=10 - row["Order"],
        x1=1.19, y1= 10 - row["Order"] - 1,
        xref = "paper", yref = "y",
        line=dict(width=3),
        fillcolor=row["Colour"],
        line_color = PLOT_BGCOLOUR
    )


fig.add_annotation(text = '<span style="color:' + COLOUR_1 +'">BYD Auto</span> is the Global Leader of Electric Car Sales',
                    xref = "paper", 
                    yref = "paper",
                    x = 0,
                    y = 1.12,
                    showarrow = False,
                    align = "left",
                    xanchor = "left",
                    yanchor = "bottom",
                    font = dict(size = 24))


fig.add_annotation(
                    # text = 'In Q3 2022, <span style="color:' + COLOUR_1 +'">BYD Auto</span> had a market share of <span style="color:' + COLOUR_1 +'">20%</span>',
                    text = 'The Chinese company <span style="color:' + COLOUR_1 +'">BYD Auto</span> had a market share of <span style="color:' + COLOUR_1 +'">20%</span> in Q3 2022, a +9pp increase since Q3 2021. Whereas <span style="color:' + COLOUR_4 +'">Tesla</span> seen it\'s market share drop <br>by -2pp to <span style="color:' + COLOUR_4 +'">13%</span>.',
                    xref = "paper", 
                    yref = "paper",
                    x = 0,
                    y = 1.03,
                    showarrow = False,
                    align = "left",
                    xanchor = "left",
                    yanchor = "bottom",
                    font = dict(size = 16))


fig.show()

# order the dataframe for the heatmp and loop over each part of it for heatmap and legend

fig.write_image("waffle.png", scale = 1, width = WIDTH, height = HEIGHT)
