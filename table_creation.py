import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import pickle

def generate_pt():
    final_ratings = pickle.load(open('final_ratings.pkl', 'rb'))
    pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
    pt.fillna(0, inplace=True)

    return pt


