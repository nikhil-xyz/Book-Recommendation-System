import streamlit as st
import pickle

def pick():
    df = pickle.load(open('final_ratings.pkl', 'rb'))

    num_df = df.groupby('Book-Title').count()['Book-Rating'].reset_index()
    num_df.rename(columns={'Book-Rating': 'num-rating'}, inplace=True)

    avg_df = df.groupby('Book-Title').mean()['Book-Rating'].reset_index()
    avg_df.rename(columns={'Book-Rating': 'avg-rating'}, inplace=True)

    p_df = num_df.merge(avg_df, on='Book-Title').drop_duplicates('Book-Title')

    p_df = p_df[p_df['num-rating'] > 200].sort_values('avg-rating', ascending=False).head(50).reset_index()
    popular = p_df.merge(df, on='Book-Title').drop_duplicates('Book-Title')

    for i in range(10):
        col1, col2 = st.columns(2)
        title = popular.iloc[i]['Book-Title']
        author = popular.iloc[i]['Book-Author']
        publisher = popular.iloc[i]['Publisher']
        cover = popular.iloc[i]['Image-URL-M']
        year = popular.iloc[i]['Year-Of-Publication']
        rating = round(df.loc[df['Book-Title'] == title]['Book-Rating'].mean(), 1)
        rate_cnt = popular.iloc[i]['num-rating']

        with col1:
            st.image(cover)
        with col2:
            st.header(title)
            st.text(author)
            st.text(publisher)
            rating = str(rating) + "⭐ (" + str(rate_cnt) + " ratings)"
            st.text(rating)
            st.text(year)

