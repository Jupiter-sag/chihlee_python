import matplotlib.pyplot as plt
import streamlit as st

labels = ['A', 'B', 'C', 'D']
values = [30, 25, 20, 25]

st.title('Pie Chart')
st.subheader('Sample Data Distribution')

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')

st.pyplot(fig)

