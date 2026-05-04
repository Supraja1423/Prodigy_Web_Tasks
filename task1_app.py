import streamlit as st

st.title("Temperature Converter")

st.subheader("Convert between Celsius, Fahrenheit, and Kelvin")  # 👈 ADD HERE

value = st.number_input("Enter Temperature", value=0.0)
unit = st.selectbox("Select Unit", ["Celsius", "Fahrenheit", "Kelvin"])

if st.button("Convert"):
    if unit == "Celsius":
        f = (value * 9/5) + 32
        k = value + 273.15
        st.write("Fahrenheit:", round(f,2))
        st.write("Kelvin:", round(k,2))

    elif unit == "Fahrenheit":
        c = (value - 32) * 5/9
        k = c + 273.15
        st.write("Celsius:", round(c,2))
        st.write("Kelvin:", round(k,2))

    else:
        c = value - 273.15
        f = (c * 9/5) + 32
        st.write("Celsius:", round(c,2))
        st.write("Fahrenheit:", round(f,2))