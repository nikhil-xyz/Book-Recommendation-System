import streamlit as st
import pickle
import numpy as np
import Calculate_sentiment as cs
import table_creation as tc
import top50 as top
import new_book as nb

from sklearn.metrics.pairwise import cosine_similarity
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options = ["Home", "Top 10", "Upload New Book"]
    )

if selected == "Home":
    st.title('Book Recommendation and Rating System')

    df = pickle.load(open('final_ratings.pkl', 'rb'))
    pt = tc.generate_pt()
    similarity = cosine_similarity(pt)


    def callback_search():
        #   Destroying old sessions
        st.session_state['search_btn'] = False
        st.session_state['post_rev'] = False


    option = st.selectbox(
        'select the book',
        pt.index,
        on_change=callback_search
    )

    search = st.button('Search')
    # adding session state fot 'Search' button
    if st.session_state.get('search_btn') != True:
        st.session_state['search_btn'] = search

    #   Selected Book Information
    index = np.where(df['Book-Title'] == option)[0][0]
    isbn = df.iloc[index]['ISBN']
    author = df.iloc[index]['Book-Author']
    publisher = df.iloc[index]['Publisher']
    cover = df.iloc[index]['Image-URL-M']
    year = df.iloc[index]['Year-Of-Publication']
    rating = round(df.loc[df['Book-Title'] == option]['Book-Rating'].mean(), 1)
    rate_cnt = df.loc[df['Book-Title'] == option]['Book-Rating'].count()

    if st.session_state['search_btn']:
        col1, col2 = st.columns(2)

        with col1:
            st.image(cover)

        with col2:
            st.header(option)
            st.text(author)
            st.text(publisher)

            if rating == 0:
                rating = "Unrated"
            else:
                rating = str(rating) + "⭐ (" + str(rate_cnt) + " reviews)"
            st.text(rating)
            st.text(year)

    if st.button('Similar Books'):
        st.session_state['post_rev'] = False
        idx = np.where(pt.index == option)[0][0]
        similar_items = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)[1:6]

        book_list = []
        posters = []
        for i in similar_items:
            book_name = pt.index[i[0]]
            book_list.append(book_name)
            idx = np.where(df['Book-Title'] == book_name)[0][0]
            posters.append(df.iloc[idx]['Image-URL-M'])

        cnt = 0
        cols = st.columns(5)
        for i in similar_items:
            with cols[cnt]:
                st.image(posters[cnt])
                st.text(book_list[cnt])
            cnt += 1

    review_post = st.button('Post the Review')

    #   Adding session state to 'review' button
    if st.session_state.get('post_rev') != True:
        st.session_state['post_rev'] = review_post

    if st.session_state['post_rev']:
        review = st.text_area('', placeholder='write your review here. Check the review score with (ctrl + enter)')

        #   Applying sentiment analysis
        score = cs.calculate(review) * 2

        if st.button('POST'):
            row = {'ISBN': isbn, 'Book-Title': option, 'Book-Author': author, 'Year-Of-Publication': year,
                   'Publisher': publisher,
                   'Image-URL-M': cover, 'User-ID': 100, 'Book-Rating': score}
            st.write("The review score was ", score)
            df = df.append(row, ignore_index=True)

            # count = df.loc[df['Book-Title'] == option]['Book-Rating'].sum()
            # st.write(count)
            pickle.dump(df, open('final_ratings.pkl', 'wb'))



if selected == "Top 10":
    st.title("Top 10 Books")
    top.pick()
if selected == "Upload New Book":
    st.title("Upload New book")
    nb.insert_new()

#
