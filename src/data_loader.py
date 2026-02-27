def load_occ_data(path:str):
    #Loading OCC enforcement dataset.##
    import pandas as pd
    df = pd.read_csv(path)
    return df