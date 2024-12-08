from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image  # To handle image
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# Set the title of the app and customize the page layout
st.set_page_config(page_title="22oz Rupido Food Hub", layout="wide", page_icon="☕",)



# Display Logo and Title
col1, col2 = st.columns([1, 5])  # Create two columns for logo and title
with col1:
    # Replace 'logo.png' with the actual file path or URL of your logo image
    logo = Image.open("22oz.jpg")  # Adjust the path to your logo file
    st.image(logo, width=150)  # Adjust logo size (resize to 150px width)

    

    

with col2:
    st.title("☕ 22oz Rupido Food Hub")

df = pd.read_excel("22ozdataset.xlsx")

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    import datetime
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated by:  \n {box_date}")

with col4:
    total_revenue = df['Net Sales'].sum()
    col4.metric("Total Sales Revenue in a year", f"₱{total_revenue:,.2f}")
    fig = px.bar(df, x = "Coffee", y = "Total Sales for Coffee", labels={"Total Sales for Coffee" : "Total Sales for Coffee"},
                 title = "Total Sales for Coffee", hover_data=["Total Sales for Coffee"],
                 template="gridon",height=500)

    fig.update_layout(
    plot_bgcolor="#e9ecef",  # Plot area background
    paper_bgcolor="#e9ecef",  # Chart area background
    font=dict(color="black"),  # Text color
    title_font=dict(size=20, color="#333333")  # Title font customization
)
    st.plotly_chart(fig,use_container_width=True)
    

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Coffee Hot and Iced Sales")
    data = df[["Coffee","Total Sales for Coffee"]].groupby(by="Coffee")["Total Sales for Coffee"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["Date"].dt.strftime("%b'%y")
result = df.groupby(by = df["Month_Year"])["Net Sales"].sum().reset_index()

with col5:

    # Total Orders
    total_orders = df['Total Quantity'].sum()
    col5.metric("Total Orders", f"{total_orders:,}")
    
    fig1 = px.line(result, x = "Month_Year", y = "Net Sales", title="Total Sales Over Time",
                   template="gridon")
    fig1.update_layout(
    plot_bgcolor="#e9ecef",  # Plot area background
    paper_bgcolor="#e9ecef",  # Chart area background
    font=dict(color="black"),  # Text color
    title_font=dict(size=20, color="#333333")  # Title font customization
)
    st.plotly_chart(fig1,use_container_width=True)

    
with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data = result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")

st.divider()

result1 = df.groupby(by="Date")[["Total Sales for Coffee","Total Sales for Milktea & Mogu Refresher"]].sum().reset_index()

# add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = result1["Date"], y = result1["Total Sales for Coffee"], name = "Total Sales for Coffee"))
fig3.add_trace(go.Scatter(x=result1["Date"], y = result1["Total Sales for Milktea & Mogu Refresher"], mode = "lines",
                          name ="Total Sales for Milktea & Mogu Refresher", yaxis="y2"))
fig3.update_layout(
    title = "Total Sales for Both Coffee and Refresher",
    xaxis = dict(title="Date"),
    yaxis = dict(title="Total Sales for Coffee", showgrid = False),
    yaxis2 = dict(title="Total Sales for Milktea & Mogu Refresher", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.1)
)

fig3.update_layout(
    plot_bgcolor="#e9ecef",  # Plot area background
    paper_bgcolor="#e9ecef",  # Chart area background
    font=dict(color="black"),  # Text color
    title_font=dict(size=20, color="#333333")  # Title font customization
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("View Data for Sales for Coffee and Refresher")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data = result1.to_csv().encode("utf-8"), 
                       file_name = "Sales_by_CoffeeandRefresher.csv", mime="text/csv")

st.divider()

