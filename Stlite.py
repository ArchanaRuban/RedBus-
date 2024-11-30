# importing libraries
import pandas as pd
import pymysql
import streamlit as st
from streamlit_option_menu import option_menu
import time




# kerala bus
df_K = pd.read_csv("D:\\Redbus.py\\KERALA.csv")
if "Route_name" in df_K.columns:
    lists_K = df_K["Route_name"].tolist()


#Andhra bus
df_A = pd.read_csv("D:\\Redbus.py\\ANDHRA.csv")
if "Route_name" in df_A.columns:
    lists_A = df_A["Route_name"].tolist()


#Telangana bus
df_T = pd.read_csv("D:\\Redbus.py\\TELANGANA.csv")
if "Route_name" in df_T.columns:
    lists_T = df_T["Route_name"].tolist()


#HIMACHAL bus
df_H = pd.read_csv("D:\\Redbus.py\\HIMACHAL.csv")
if "Route_name" in df_H.columns:
    lists_H = df_H["Route_name"].tolist()


#Rajastan bus
df_R = pd.read_csv("D:\\Redbus.py\\RAJASTHAN.csv")
if "Route_name" in df_R.columns:
    lists_R = df_R["Route_name"].tolist()



# South bengal bus 
df_SB = pd.read_csv("D:\\Redbus.py\\SOUTH_BENGAL.csv")
if "Route_name" in df_SB.columns:
    lists_SB = df_SB["Route_name"].tolist()


# KADAMBA bus
df_KD = pd.read_csv("D:\\Redbus.py\\KADAMBA.csv")
if "Route_name" in df_KD.columns:
    lists_KD = df_KD["Route_name"].tolist()


#Assam bus
df_AS = pd.read_csv("D:\\Redbus.py\\ASSAM.csv")
if "Route_name" in df_AS.columns:
    lists_AS = df_AS["Route_name"].tolist()


#UP bus
df_UP = pd.read_csv("D:\\Redbus.py\\UTTAR_PRADESH.csv")
if "Route_name" in df_UP.columns:
    lists_UP = df_UP["Route_name"].tolist()


#West bengal bus
df_WB = pd.read_csv("D:\\Redbus.py\\UTTAR_PRADESH.csv")
if "Route_name" in df_WB.columns:
    lists_WB= df_WB["Route_name"].tolist()




# Define routes for each state
routes = {
    "Kerala": lists_K,
    "Andhra Pradesh":lists_A,
    "Telangana":lists_T,
    "Kadamba":lists_KD,
    "Rajasthan":lists_R,
    "Uttar_Pradesh":lists_UP,
    "South_Bengal": lists_SB,
    "West_Bengal":lists_WB,
    "Himachal": lists_H,
    "Assam": lists_AS
   
}



# Function to filter data
def get_filtered_data(state, route, bus_type, fare_range, time):
    conn = pymysql.connect(host="localhost", user="root", password="Beyo@123", database="mydatabase")
    my_cursor = conn.cursor()

    # Define fare range based on selection
    if fare_range == "50-1000":
        fare_min, fare_max = 50, 1000
    elif fare_range == "1000-2000":
        fare_min, fare_max = 1000, 2000
    else:
        fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

    # Define bus type condition
    if bus_type == "sleeper":
        bus_type_condition = "Bus_type LIKE '%Sleeper%'"
    elif bus_type == "semi-sleeper":
        bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
    else:
        bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

    # SQL Query
    query = f'''
        SELECT * FROM bus_details12
        WHERE Price BETWEEN {fare_min} AND {fare_max}
        AND Route_name = "{route}"
        AND {bus_type_condition}
        AND Start_time >= '{time}'
        ORDER BY Price ASC, Start_time ASC
    '''
    my_cursor.execute(query)
    out = my_cursor.fetchall()
    conn.close()

    # Convert output to DataFrame
    df = pd.DataFrame(out, columns=[
        "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
        "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
    ])
    return df


# Streamlit UI
st.title("RedBus Booking Data Filter")

# Select state
state = st.selectbox("Select State", list(routes.keys()))

# Select route dynamically based on state
route = st.selectbox(f"Available routes in {state}", routes[state])

# Columns for bus type and fare range
col1, col2 = st.columns(2)
with col1:
    bus_type = st.radio("Choose bus type", ("sleeper", "semi-sleeper", "seater"))
with col2:
    fare_range = st.radio("Choose fare range", ("50-1000", "1000-2000", "2000 and above"))

# Time input
time = st.time_input("Select departure time")

# Fetch and display results
if st.button("Filter Buses"):
    filtered_data = get_filtered_data(state, route, bus_type, fare_range, time)
    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.write("No buses match your criteria.")


