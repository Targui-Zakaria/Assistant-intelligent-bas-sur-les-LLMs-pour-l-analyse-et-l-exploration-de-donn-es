import streamlit as st
import pandas as pd


def render_dataframe(df: pd.DataFrame, *, show_download: bool = False) -> None:
    if df is None or df.empty:
        st.caption("Aucune donnée à afficher.")
        return

    st.dataframe(df, use_container_width=True, height=min(320, 35 * len(df) + 38))

    if show_download:
        st.download_button(
            label="Télécharger CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="resultats_olist.csv",
            mime="text/csv",
            use_container_width=True,
        )
