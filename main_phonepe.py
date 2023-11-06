import streamlit as st
import mysql.connector

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go # or plotly.express as px

# setting page config and Title

st. set_page_config(layout="wide")

st.markdown("# :violet[Phonepe-pulse Data Visualization and Exploration :bar_chart:]")
st.write("### :violet[-by Gokul Ram]")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)
# print(mydb)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("USE Phonepe_pulse")

agg_trans_df = pd.read_csv(r'/Users/gokul/My Apple/vs_code_practice/phonepe_project/agg_trans.csv')
map_trans_df = pd.read_csv(r'/Users/gokul/My Apple/vs_code_practice/phonepe_project/map_trans.csv')

agg_users_df = pd.read_csv(r'/Users/gokul/My Apple/vs_code_practice/phonepe_project/agg_users.csv')
agg_users_summ_df = pd.read_csv(r'/Users/gokul/My Apple/vs_code_practice/phonepe_project/agg_users_summ.csv')

map_users_df = pd.read_csv(r'/Users/gokul/My Apple/vs_code_practice/phonepe_project/map_users.csv')

geo_states_df = pd.read_csv(r'/Users/gokul/My Apple/vs_code_practice/phonepe_project/geo_states.csv')


# ============================================= GEO MAP VISUAL =============================================

st.write('# :orange[GEO MAP VISUALIZATION :earth_asia:]')

column1, column2 = st.columns(2)

fig_1 = px.choropleth(
    geo_states_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations= 'Geo_states',
    color= 'Transaction_count',
    color_continuous_scale='gnbu'
)

fig_1.update_geos(fitbounds="locations", visible=False)

fig_2 = px.choropleth(
    geo_states_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations= 'Geo_states',
    color= 'Transaction_amount',
    color_continuous_scale='purpor'
)

fig_2.update_geos(fitbounds="locations", visible=False)

with column1:

    st.write ('##### :orange[TRANSACTION COUNT STATE MAP ]')

    st.plotly_chart(fig_1,  use_container_width = True)

    st.info(
    """
    Details of Map:
    - Hover data will show the details like Total transactions of that state
    - By the gradient of color scale we can recognize the transaction count range
    """
    )

with column2:

    st.write ('##### :orange[TRANSACTION AMOUNT STATE MAP ]')

    st.plotly_chart(fig_2,  use_container_width = True)

    st.info(
    """
    Details of Map:
    - Hover data will show the details like Total transactions of that state
    - By the gradient of color scale we can recognize the transaction amount range
    """
    )


# ============================================= STATE WISE PAYMENT TYPE ANALYSIS =============================================

st.write('# :blue[PAYMENT TYPE ANALYSIS :credit_card:]')


c1,c2,c3 = st.columns(3)
with c1:
    Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022','2023'))
    
with c2:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'))

with c3:
    Type = st.selectbox(
            'Please select the Type',
            ('Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments','Financial Services','Others'))
    
year=int(Year)
quarter=int(Quarter)


mycursor.execute(f"SELECT State, Transaction_count FROM agg_trans WHERE year = {Year} and quarter = {Quarter} and Transaction_type = '{Type}' ORDER BY State")
df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_count'])
# df = pd.read_csv("/Users/gokul/My Apple/vs_code_practice/phonepe_project/agg_trans.csv")
# dataset  = df.sort_values(by= Year)
fig = px.bar(df, x='State', y='Transaction_count',title = "Transaction count of " + Type + " in "+ str(year) + " Q-" + str(quarter))
st.plotly_chart(fig, use_container_width = True)
st.info(
"""
Details of Bar Graph:
- This graph displays the total transaction count of all the states for the above selected parameters
- X Axis denotes all the states in order
- Y Axis represents total transactions count       
"""
)

# ================================================= TRANSACTION ANALYSIS ===================================================

st.write('# :green[TRANSACTIONS ANALYSIS :currency_exchange:]')
tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS", "YEAR ANALYSIS", "OVERALL ANALYSIS"])

#~~~~~~~~~~~~~~~~~~~~ STATE ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tab1:

    data_agg_trans = agg_trans_df.copy()
    state_analysis = data_agg_trans.copy()

    col1, col2= st.columns(2)

    with col1:
        type = st.selectbox(
            'Please select the Type',
            ('Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments','Financial Services','Others'),key='a')
    
    with col2:
        state = st.selectbox(
            'Please select the state',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
             'assam', 'bihar', 'chandigarh', 'chhattisgarh',
             'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
             'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
             'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
             'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
             'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
             'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
             'uttarakhand', 'west-bengal'
            ), key = 'b')
    
    state_name = state
    year_list = [2018, 2019, 2020, 2021, 2022, 2023]
    Mode = type

    state_analysis = state_analysis.loc[(state_analysis['State'] == state_name ) & (state_analysis['Year'].isin(year_list)) & 
                                        (state_analysis['Transaction_type'] == Mode )]
    
    state_analysis = state_analysis.sort_values(by=['Year'])
    state_analysis["Quarter"] = "Q" + state_analysis["Quarter"].astype(str)
    state_analysis["Year_Quarter"] = state_analysis["Year"].astype(str) + "-" + state_analysis["Quarter"].astype(str)

    fig = px.bar(state_analysis, x = 'Year_Quarter', y = 'Transaction_count', color = "Transaction_count",
                 color_continuous_scale = "Viridis")



    colT1, colT2 = st.columns([7,3])
    with colT1:
        st.write ("#### " + state_name.upper())
        st.plotly_chart(fig, use_container_width = True)

    with colT2:
         st.info(
        """
        Details of Bar Graph:
        - This entire data belongs to the state selected
        - X Axis denotes all the years with all quarters 
        - Y Axis represents total transactions in selected type       
        """
        )

#~~~~~~~~~~~~~~~~~~~~ DISTRICT ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tab2:

    col1, col2, col3 = st.columns(3)

    with col1:

        state = st.selectbox(
            'Please select the state',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
             'assam', 'bihar', 'chandigarh', 'chhattisgarh',
             'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
             'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
             'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
             'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
             'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
             'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
             'uttarakhand', 'west-bengal'
            ), key = 'c')

    with col2:

        Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019','2020','2021','2022','2023'),key = 'd')
        
    with col3:

        Quarter = st.selectbox(
            'Please select the quarter',
            ('1', '2', '3', '4'), key = 'e')
        
        district_analysis = map_trans_df.loc[(map_trans_df["State"] == state ) & (map_trans_df["Year"] == int(Year)) &
                                             (map_trans_df["Quarter"] == int(Quarter))]
        
        l = len(district_analysis)
        fig1 = px.bar(district_analysis, x = 'District', y = 'Count', color = "Count",
                 color_continuous_scale = "Viridis")
        
    colT1, colT2 = st.columns([7,3])

    with colT1:

        if l:
            st.write("#### " + state.upper()+ ' WITH ' + str(l) + ' DISTRICTS')
            st.plotly_chart(fig1, use_container_width = True)

        else:
            st.write("#### NO DATA TO DISPLAY FOR SELECTED QUARTER")

    with colT2:

        st.info("""
                Details of BarGraph:
                - This entire data belongs to state selected
                - X Axis represents the districts of the selected state
                - Y Axis represents total transactions count """
                )

#~~~~~~~~~~~~~~~~~~~~ YEAR ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tab3:
    
    co1, co2= st.columns(2)
    
    with co1:

        T = st.selectbox(
            'Please select the Type',
            ('Merchant payments', 'Peer-to-peer payments', 'Recharge & bill payments','Financial Services','Others'), key = 'f')
        
    with co2:

        Y = st.selectbox(
            'Please select the Year',
            ('2018', '2019','2020','2021','2022','2023'),key = 'g')
    
    mycursor.execute(f"SELECT State, Transaction_count FROM agg_trans WHERE Year = '{Y}' AND Transaction_type = '{T}' GROUP BY State ORDER BY Transaction_count ASC")
    df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_count'])
    fig2 = px.bar(df1, x = 'State' , y = 'Transaction_count', color = "Transaction_count",
                 color_continuous_scale = "Viridis")
    
    coT1, coT2 = st.columns([7,3])

    with coT1:

        st.write("#### " + str(Y) + ' DATA ANALYSIS')
        st.plotly_chart(fig2, use_container_width = True)

    with coT2:

        st.info("""
                Details of BarGraph:
                - This entire data belongs to the selected Year
                - X Axis is all the states in increasing order of Total transactions
                - Y Axis represents total transactions in selected type """
                )


#~~~~~~~~~~~~~~~~~~~~ OVERALL ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tab4:

    # years = data_agg_trans.groupby('Year')
    # years_list = data_agg_trans['Year'].unique()
    # years_data = years.sum()

    # years_data["Year"] = years_list

    mycursor.execute(f"SELECT Year, SUM(Transaction_count) FROM agg_trans GROUP BY Year ORDER BY Transaction_count ASC")
    df3 = pd.DataFrame(mycursor.fetchall(), columns=['Year', 'Transaction_count'])

    mycursor.execute(f"SELECT Year, SUM(Transaction_amount) FROM agg_trans GROUP BY Year ORDER BY Transaction_amount ASC")
    df4 = pd.DataFrame(mycursor.fetchall(), columns=['Year', 'Transaction_amount'])

    fig3 = px.pie(df3, values='Transaction_count', names = 'Year', color_discrete_sequence = px.colors.sequential.Viridis, title = 'TOTAL TRANSACTIONS (2018 TO 2023)')
    fig4 = px.pie(df4, values='Transaction_amount', names = 'Year', color_discrete_sequence = px.colors.sequential.Viridis, title = 'TOTAL AMOUNT (2018 TO 2023)')

    colum1, colum2 = st.columns(2)

    with colum1:

        st.write('### :green[ OVERALL COUNT :1234:]')
        st.plotly_chart(fig3)

    with colum2:

        st.write('### :green[ OVERALL AMOUNT:moneybag:]')
        st.plotly_chart(fig4)



# ================================================ USER ANALYSIS ===================================================


st.write('# :orange[USERS DATA ANALYSIS :busts_in_silhouette:]')
tabs1, tabs2, tabs3, tabs4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS", "BRAND ANALYSIS", "OVERALL ANALYSIS"])


#~~~~~~~~~~~~~~~~~~~~ USER STATE ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

users_summ = agg_users_summ_df.copy()

with tabs1:

    state = st.selectbox(
        'Please select the state',
        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal'
        ), key = 'h')


    agg_users_summ_df["state_year"] = agg_users_summ_df["State"] + "-" + agg_users_summ_df["Year"].astype(str)
    agg_users_summ_df["state_year_1"] = agg_users_summ_df["State"] + "-" + agg_users_summ_df["Year"].astype(str)

    analysis = agg_users_summ_df.groupby(['state_year_1'])

    # display(analysis)

    state_analysis_1 = analysis.sum().reset_index()

    state_analysis_1 = state_analysis_1.loc[(state_analysis_1["state_year_1"].str[:-5] == state) ]
    
    # display(state_analysis_1)
    # print(type(state_analysis_1))


    fig = go.Figure(data=[
        go.Bar(name = 'App Openings', y = state_analysis_1['Registered_users'], x = state_analysis_1['state_year_1'], marker = {'color': 'red'}),
        go.Bar(name = 'Registered Users', y = state_analysis_1['App_openings'], x = state_analysis_1['state_year_1'],marker={'color': 'orange'})
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')

    colT1,colT2 = st.columns([7,3])
        
    with colT1:
        st.write("#### ",state.upper())
        st.plotly_chart(fig, use_container_width=True, height=200)
    with colT2:
        st.info(
        """
        Details of BarGraph:
        - This graph shows the App openings and Registered users 
          count for the state selected
        - The X Axis shows both Registered users and App openings 
        - The Y Axis shows the Percentage of Registered users and App openings""")


#~~~~~~~~~~~~~~~~~~~~ USER DISTRICT ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tabs2:

    col1, col2, col3 = st.columns(3)

    with col1:

        state = st.selectbox(
            'Please select the state',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
             'assam', 'bihar', 'chandigarh', 'chhattisgarh',
             'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
             'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
             'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
             'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
             'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
             'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
             'uttarakhand', 'west-bengal'
            ), key = 'i')

    with col2:

        Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019','2020','2021','2022','2023'),key = 'j')
        
    with col3:

        Quarter = st.selectbox(
            'Please select the quarter',
            ('1', '2', '3', '4'), key = 'k')

    districts = map_users_df.loc[(map_users_df['state'] == state ) & (map_users_df['year'] == int(Year))
                                          & (map_users_df['quarter'] == int(Quarter))]

    l=len(districts)

    fig6 = px.bar(districts, x = 'district', y = 'registered_users', color = "registered_users",
                 color_continuous_scale = "reds")
        
    colT1, colT2 = st.columns([7,3])

    with colT1:

        if l:
            st.write("#### " + state.upper()+ ' WITH ' + str(l) + ' DISTRICTS')
            st.plotly_chart(fig6, use_container_width = True)

        else:
            st.write("#### NO DATA TO DISPLAY FOR SELECTED STATE")

    with colT2:

        st.info("""
                Details of BarGraph:
                - This entire data belongs to the state & year selected
                - X Axis represents the districts of the selected state
                - Y Axis represents registered users count """
                )

#~~~~~~~~~~~~~~~~~~~~ USER BRAND ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tabs3:

    st.write('### :orange[Brand Share Data ] ')
    cols1, cols2 = st.columns(2)

    with cols1:

        state = st.selectbox(
            'Please select the state',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
             'assam', 'bihar', 'chandigarh', 'chhattisgarh',
             'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
             'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
             'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
             'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
             'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
             'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
             'uttarakhand', 'west-bengal'
            ), key = 'l')
        
    with cols2:

        Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019','2020','2021','2022','2023'),key = 'm')
        
    y = int(Year)
    s = state

    brand = agg_users_df[agg_users_df["Year"] == y]
    brand=agg_users_df.loc[(agg_users_df['Year'] == y) & (agg_users_df['State'] == s)]

    mybrand = brand['Brand'].unique()
    x = sorted(mybrand).copy()
    b = brand.groupby('Brand').sum()    #new df
    b['brand'] = x                      #assigning sorted brand column data
    br = b['Count'].sum()
    labels = b['brand']
    values = b['Count']

    fig3 = go.Figure(data = [go.Pie(labels = labels, values = values, hole = .4, textinfo = 'label+percent', texttemplate = '%{label}<br>%{percent:1%f}',
                                    insidetextorientation='horizontal', textfont = dict(color='#000000'), marker_colors = px.colors.qualitative.Prism)])
    
    colT1,colT2 = st.columns([7,3])

    with colT1:

        st.write("#### ", 'BRAND SPLIT-UP OF '+ state.upper()+' IN ' + Year )
        st.plotly_chart(fig3, use_container_width = True)
    
    with colT2:

        st.info("""
        Details of Donut Chart:        
        - Donut chart is displayed for selected State and Year
        - Percentage of registered users is represented by Device Brand"""
        )

        st.info("""
        Observations:
        - User can observe the top leading brands in a particular state and year
        - Brand derails of the registered users"""
        )

    b = b.sort_values(by=['Count'])
    fig4= px.bar(b, x = 'brand', y = 'Count',color = "Count",
                title = 'Brand wise registered users count of ' + state +' in '+ str(y),
                color_continuous_scale = "mint")
    with st.expander("Show Bar graph for the above data"):
        st.plotly_chart(fig4,use_container_width = True) 

#~~~~~~~~~~~~~~~~~~~~ USER OVERALL ANALYSIS ~~~~~~~~~~~~~~~~~~~~~~

with tabs4:


    mycursor.execute(f"SELECT Year, SUM(Registered_users) FROM agg_users_summary GROUP BY Year ORDER BY Year ASC")
    df3 = pd.DataFrame(mycursor.fetchall(), columns=['Year', 'Registered_users'])

    mycursor.execute(f"SELECT Year, SUM(App_openings) FROM agg_users_summary GROUP BY Year ORDER BY Year ASC")
    df4 = pd.DataFrame(mycursor.fetchall(), columns=['Year', 'App_openings'])

    fig3 = px.pie(df3, values='Registered_users', names = 'Year', hole= 0.4, color_discrete_sequence = px.colors.sequential.Cividis, title = 'TOTAL REGISTERED USERS (2018 TO 2023)')
    fig4 = px.pie(df4, values='App_openings', names = 'Year',hole= 0.4, color_discrete_sequence = px.colors.sequential.Cividis, title = 'TOTAL APP OPENINGS (2018 TO 2023)')
    
    
    colum1, colum2 = st.columns(2)

    with colum1:

        st.write('### :orange[ OVERALL REGISTERED USERS :1234:]')
        st.plotly_chart(fig3)

    with colum2:

        st.write('### :orange[ OVERALL APP OPENINGS :moneybag:]')
        st.plotly_chart(fig4)


# ================================================ TOP DATA ANALYSIS ===================================================


st.write('# :red[TOP 5 STATES DATA]')

c1,c2 = st.columns(2)
with c1:
    Year = st.selectbox(
        'Please select the Year',
        ('2018', '2019','2020','2021','2022','2023'), key = 'n')
with c2:
    Quarter = st.selectbox(
        'Please select the Quarter',
        ('1', '2', '3','4'),key = 'o')

q = Quarter
yy = Year
# Top 5 states in registered users

mycursor.execute(f"SELECT State, SUM(registered_users) FROM `map_users` WHERE year = '{yy}' AND quarter = '{q}' \
                 GROUP BY State ORDER BY `SUM(registered_users)` DESC LIMIT 5")
df5 = pd.DataFrame(mycursor.fetchall(), columns = ['State', 'registered_users'])

# Top 5 states in app openings

mycursor.execute(f"SELECT State, SUM(app_openings) FROM `map_users` WHERE year = '{yy}' AND quarter = '{q}' \
                 GROUP BY State ORDER BY `SUM(app_openings)` DESC LIMIT 5")
df6 = pd.DataFrame(mycursor.fetchall(), columns = ['State', 'app_openings'])

# Top 5 states in Transactions count

mycursor.execute(f"SELECT State, SUM(Count) FROM `map_trans` WHERE year = '{yy}' AND quarter = '{q}' \
                 GROUP BY State ORDER BY `SUM(Count)` DESC LIMIT 5")
df7 = pd.DataFrame(mycursor.fetchall(), columns = ['State', 'Count'])


# Top 5 states in Transaction amount

mycursor.execute(f"SELECT State, SUM(Amount) FROM `map_trans` WHERE year = '{yy}' AND quarter = '{q}' \
                 GROUP BY State ORDER BY `SUM(Amount)` DESC LIMIT 5")
df8 = pd.DataFrame(mycursor.fetchall(), columns = ['State', 'Amount'])


col1, col2, col3, col4 = st.columns([2.5,2.5,2.5,2.5])


with col1:

    st.markdown("##### :orange[Registered Users :bust_in_silhouette:]")
    st.write(df5)
    # print(df5)

    fig10 = px.bar(df5, x = 'State', y = 'registered_users', color = "registered_users")
    st.plotly_chart(fig10, use_container_width = True)

with col2:

    st.markdown("##### :orange[App Openings :iphone:]")
    st.write(df6)

    fig11 = px.bar(df6, x = 'State', y = 'app_openings', color = "app_openings", color_continuous_scale = 'viridis')
    st.plotly_chart(fig11, use_container_width = True)

with col3:
    st.markdown("##### :orange[Total Transaction count :currency_exchange:]")
    st.write(df7)

    fig12 = px.bar(df7, x = 'State', y = 'Count', color = "Count", color_continuous_scale = px.colors.sequential.Agsunset)
    st.plotly_chart(fig12, use_container_width = True)


with col4:
    st.markdown("##### :orange[Total Transaction Amount :dollar:]")
    st.write(df8)

    fig13 = px.bar(df8, x = 'State', y = 'Amount', color = "Amount", color_continuous_scale = 'viridis')
    st.plotly_chart(fig13, use_container_width = True)


st.markdown("<h2 style='text-align: center; color: grey;'>Thank You..!!! </h2>", unsafe_allow_html=True)


# ================================================ END =====================================================
