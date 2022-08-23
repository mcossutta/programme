import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
data_prof = pd.read_csv("professeur.csv")
data_classe = pd.read_csv("classe.csv")

data_classe = data_classe.astype({"id_professeur": int})



for index, row in data_classe.iterrows():
    data_classe["id_professeur"][index] = data_prof[data_prof.trigramme ==row['trigramme']].id

data_classe.to_csv("classe_new.csv")



 
