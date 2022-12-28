
import pandas as pd



def preprocess(df,region_df):

    # filltering for the summer olympics
    df = df[df['Season'] == 'Summer']

    # merge with the region_df

    df = df.merge(region_df, on = 'NOC', how = 'left')

    #dropping duplicates
    df.drop_duplicates(inplace = True)

    # ONe hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis = 1)
    df = df.loc[~df.index.duplicated(),:].copy()
    return df