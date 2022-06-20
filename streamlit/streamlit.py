import streamlit as st
import pandas as pd
import numpy as np

if __name__ == '__main__':
    st.title('Predicting Bus Travel Times')

    arr = np.array(
        [1.4405688333333333, 103.785777]
    )

    df = pd.DataFrame({
        'lat' : [1.4405688333333333, 1.4456981666666666],
        'lon' : [103.785777, 103.77323333333334]
    })

    print(df.head())

    st.map(df)
