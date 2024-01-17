
import streamlit as st
import psycopg2

#conn = st.connection("postgresql", type="sql")

dbconn = psycopg2.connect(
    host = st.secrets.host,
    user = "postgres",
    password = st.secrets.password,
    database = "postgres")

dbconn.autocommit = True

curssor = dbconn.cursor()