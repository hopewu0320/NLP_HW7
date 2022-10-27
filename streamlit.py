import streamlit as st
from SpellChecker import correction
from SpellChecker import randomly_choose
st.title("Spellchecker Demo")
option=st.selectbox('Choose a word or...',['apple','speling','lamon','hapy','language','greay','sussess'])

user_input=st.text_input('type your own!!',value=option)

st.write('Original word:', user_input)


if option==correction(option):
    if option==user_input:
        st.success('{} is the correct spelling!'.format(option))
    else:
        st.error('Correction:{}'.format(correction(user_input)))
else:
    if user_input==correction(option):
        st.success('{} is the correct spelling!'.format(correction(option)))
    else:
        st.error('Correction:{}'.format(correction(user_input)))
