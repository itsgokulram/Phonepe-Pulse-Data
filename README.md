# Phonepe-Pulse-Data-Visualization

I have created a dashboard to visualize Phonepe pulse Github repository data(https://github.com/PhonePe/pulse) using Streamlit and Plotly in Python

``` DATA EXTRACTION```
Data Extraction: Clone the data from pulse github repo. Then extract all the data from json files present in all the corresponding folders and form respective dataframes for the visualization purpose. 

THE MAIN COMPONENTS OF DASHBOARD ARE
```
1. GEO MAP VISUALIZATION

2. PAYMENT TYPE ANALYSIS

3. TRANSACTIONS ANALYSIS

4. USERS DATA ANALYSIS

5. TOP 5 STATES DATA
```
1. GEO MAP VISUALIZATION: The India map shows the Total Transactions count and total amount of PhonePe with all the states. It comes with zoom option and on hover displays the content related to that particular state.
```Plotlys coropleth for drawing the states in India map ```

2. PAYMENT TYPE ANALYSIS: This graph displays the total transaction count of all the states. Here we can visualize the bar graph by selecting a year, quarter and the payment type and the respective data will be displayed in bar graph

3. TRANSACTIONS ANALYSIS: The Transactions data mainly contains the total Transactions count and total amount in each state and district, I have used different graphs available in plotly to represent this data
```
1. State Analysis

2. District Analysis

3. Year Analysis

4. Overall Analysis
```
4. USERS DATA ANALYSIS: The Users data mainly contains the Registered users count and App openings via different mobile brands in each state and district,I have used different graphs available in plotly to represent this data.
```
1. State-wise user Analysis

2. District-wise user Analysis

3. Brand Analysis

4. Overall Analysis
```
5. TOP 5 STATES DATA: Here i have displayed the top 5 states data for the following
```
1. States with top 5 Registered users

2. States with top 5 App openings

3. Top 5 states with highest Transactions count

4. Top 5 states with highest Transaction amount
```
