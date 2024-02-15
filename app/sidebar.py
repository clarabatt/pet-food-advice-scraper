import streamlit as st


def sidebar(df):

    total_products = df["name"].count()

    with st.sidebar:
        st.markdown(
            """
            **Developed by:** [Clara Battesini](https://www.linkedin.com/in/clara-battesini/)
            
            **Source:** [PetSmart](https://www.petsmart.com/)
            
            **Description:** The dataset contains information about pet food products such as price, rating, brand, and animal type.
            
            **Size:** {total_products} products
            
            **Columns:** {columns}
            """.format(
                total_products=total_products, columns=", ".join(df.columns)
            )
        )

        st.write("**Data Sample:**")
        st.dataframe(df.tail())

        st.download_button(
            "Download Data",
            df.to_csv(index=False),
            "petsmart_products.csv",
        )

        st.write(
            "[Github Repository](https://github.com/clarabatt/pet-food-advice-scraper/tree/main)"
        )
