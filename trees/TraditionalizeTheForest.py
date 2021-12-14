import chinese_converter as chc
import pandas as pd

forest = pd.read_csv("WikiCCD_2021-07-18.csv")
forest = forest[forest.Component == forest.Component.map(chc.to_traditional)]
forest.to_csv("WikiCCD_2021-07-18_TradOnly.csv")
