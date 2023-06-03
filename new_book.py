import streamlit as st
import pickle

yrs = []
for i in range(1800, 2024):
    yrs.append(i)

def insert_new():
    with st.form(key='form1'):
        book_title = st.text_input("Book Name")
        author = st.text_input("Author")
        year = st.selectbox(
            'Select the Year',
            yrs)

        publisher = st.text_input("Publisher")
        rating = st.text_input("Book Rating")
        submit_btn = st.form_submit_button(label='Upload')

    if submit_btn:
        #   User_ID and book-cover
        use_id = 100
        cover = "https://images-na.ssl-images-amazon.com/images/P/0449001164.0..."

        try:
            temp = int(rating)
        except ValueError:
            st.write("Only integers between 1 to 10 are allowed for rating")
            temp = -1

        if (temp < 0) or (temp > 10):
            st.write("Only integers between 1 to 10 are allowed for rating")
            temp = -1

        if book_title == "":
            st.write("Book Title can't be Empty")
        if author == "":
            st.write("Author can't be Empty")
        if publisher == "":
            st.write("Publisher can't be Empty")

        #   Generating ISBN
        df = pickle.load(open('final_ratings.pkl', 'rb'))
        string = str(len(df))
        isbn = ((10 - len(string)) * "0") + string

        if (book_title != "") and (author != "") and (publisher != "") and (temp != -1):
            row = {'ISBN': isbn, 'Book-Title': book_title, 'Book-Author': author, 'Year-Of-Publication': year,
                   'Publisher': publisher,
                   'Image-URL-M': cover, 'User-ID': use_id, 'Book-Rating': temp}

            df = df.append(row, ignore_index=True)
            pickle.dump(df, open('final_ratings.pkl', 'wb'))

            st.write("New Book Uploaded.")
            st.write("ISBN assigned: ", isbn)
