import pandas as pd
import seaborn as sns
import numpy as np
import pyodbc
import plotly.express as px
from datetime import date, timedelta
import warnings
warnings.filterwarnings('ignore')
#-----------------------------------------------------------------------------------------------------------
today = date.today().strftime("%Y-%m-%d")
last_month = (date.today()-timedelta(days=30)).isoformat()
#-----------------------------------------------------------------------------------------------------------
def query_datax(produkt, startDate, endDate, server, database):
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    try:
        df = pd.read_sql_query(                        
            '''
            SELECT t1.[Fauf] AS Lot 
            ,t1.[Auftragsstart] AS DateTime
            ,t1.[ASIC_SN] AS ASSP
            ,t1.[ErrorCode]
            ,t2.[C0_CO0]
            ,t2.[C4_CO1]
            ,t2.[C5_CO2]
            ,t2.[C1_CG0]
            ,t2.[C6_CG1]
            ,t2.[C7_CG2]
            ,t1.[TDK_SN] 
            
            FROM [DWH_PD].[dbo].[tABGL_dt_o] t1
            LEFT JOIN [DWH_PD].[dbo].[ABGL_dt_Coefficient] t2  ON  t2.[DutID] = t1.[DutID]  
            
            WHERE  t1.Auftragsstart BETWEEN '''+startDate+''' AND '''+endDate+'''
            AND  t1.sapNumber LIKE '''+produkt+'''
            ''', cnxn)
         
       
        df = df.dropna(subset = ['C0_CO0', 'C4_CO1', 'C5_CO2','C1_CG0','C6_CG1','C7_CG2']).reset_index(drop=True)
        #df = df.drop_duplicates(subset=['ASSP'], ignore_index = True )
        df = df.astype({"C0_CO0":"int","C4_CO1":"int","C5_CO2":"int","C1_CG0":"int","C6_CG1":"int","C7_CG2":"int"})
        produkt = produkt[2:6]
        df['ErrorCode'] = df['ErrorCode'].astype(str)
        df['TDK_SN'] = df['TDK_SN'].astype(object)
        
        number_of_uniqueASSPs = df['ASSP'].nunique()  
        unique_ASSPs = df['ASSP'].unique()
        DoubleRows = []
        for i in range(number_of_uniqueASSPs):          # takes time !!!
            sub_df = df[df['ASSP'] == unique_ASSPs[i]]  # sub_df contains of unique ASSPs then for each i maybe we have 2 rows with same ASSP
            maxDate = sub_df["DateTime"].max()          # then from it we take the max of date time or newest one.
    
            if len(sub_df) > 1:  # now if sub_df has more than 1 row 
                for index, row in sub_df.iterrows():
                    if row["DateTime"] < maxDate:   # here if the DateTime be less than maxDate then we append it to DoubleRows
                        DoubleRows.append(index)
        
        df.drop(DoubleRows, axis = 0 , inplace = True)
        df.reset_index( inplace = True )
        df = df.drop(columns =['index'])
        
    except:
        print("Error: Error in Query")

    print('The dataframe df has ' + str(len(df.index)) + ' rows')
    return df
#-----------------------------------------------------------------------------------------------------------
def query_data(produkt, startDate, endDate, server, database):
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    try:
        df = pd.read_sql_query(                        
            '''
            SELECT t1.[Fauf] AS Lot 
            ,t1.[DutStart] AS DateTime
            --,t1.[Auftragsstart] AS DateTimexxxxx     
            ,t1.[ASIC_SN] AS ASSP
            ,t1.[ErrorCode]
            ,t2.[C0_CO0]
            ,t2.[C4_CO1]
            ,t2.[C5_CO2]
            ,t2.[C1_CG0]
            ,t2.[C6_CG1]
            ,t2.[C7_CG2]
            ,t1.[TDK_SN] 
            
            FROM [DWH_PD].[dbo].[tABGL_dt_o] t1
            LEFT JOIN [DWH_PD].[dbo].[ABGL_dt_Coefficient] t2  ON  t2.[DutID] = t1.[DutID]  
            
            WHERE  t1.Auftragsstart BETWEEN '''+startDate+''' AND '''+endDate+'''
            AND  t1.sapNumber LIKE '''+produkt+'''
            ''', cnxn)
         
        df = df.sort_values ( by = ['DateTime'] )
        df = df.dropna(subset = ['C0_CO0', 'C4_CO1', 'C5_CO2', 'C1_CG0', 'C6_CG1', 'C7_CG2']).reset_index(drop=True)
        df = df.drop_duplicates(subset=['ASSP'], ignore_index = True , keep = 'last')                                       # innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
        df = df.astype({"C0_CO0":"int","C4_CO1":"int","C5_CO2":"int","C1_CG0":"int","C6_CG1":"int","C7_CG2":"int"})
        produkt = produkt[2:6]
        df['ErrorCode'] = df['ErrorCode'].astype(str)
        df['TDK_SN'] = df['TDK_SN'].astype(object)
    
    except:
        print("Error: Error in Query")

    print('The dataframe df has ' + str(len(df.index)) + ' rows')
    return df
#-----------------------------------------------------------------------------------------------------------
def query_data2(produkt, startDate, endDate, server, database):
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    try:
        df = pd.read_sql_query(                        
            '''
            SELECT t1.[Fauf] AS Lot 
            ,t1.[DutStart] AS DateTime
            ,t1.[ASIC_SN] AS ASSP
            ,t1.[ErrorCode]
            ,t2.[C0_CO0]
            ,t2.[C4_CO1]
            ,t2.[C5_CO2]
            ,t2.[C1_CG0]
            ,t2.[C6_CG1]
            ,t2.[C7_CG2]
            ,t1.[TDK_SN] 

		    ,t3.TL1_RawPressure
		    ,t3.TL2_RawPressure
		    ,t3.TM1_RawPressure
		    ,t3.TM2_RawPressure
		    ,t3.TM3_RawPressure
		    ,t3.TH1_RawPressure
		    ,t3.TH2_RawPressure
	
		    ,t3.TL1_ReferencePressure
		    ,t3.TL2_ReferencePressure
		    ,t3.TM1_ReferencePressure
		    ,t3.TM2_ReferencePressure
		    ,t3.TM3_ReferencePressure
		    ,t3.TH1_ReferencePressure
		    ,t3.TH2_ReferencePressure

            ,t3.TL1_ReferenceTemperature
		    ,t3.TL2_ReferenceTemperature
		    ,t3.TM1_ReferenceTemperature
		    ,t3.TM3_ReferenceTemperature
		    ,t3.TH1_ReferenceTemperature
		    ,t3.TH2_ReferenceTemperature

            FROM [DWH_PD].[dbo].[tABGL_dt_o] t1
            LEFT JOIN [DWH_PD].[dbo].[ABGL_dt_Coefficient] t2  ON  t2.[DutID] = t1.[DutID]  
            LEFT JOIN [DWH_PD].[dbo].[ABGL_dt_Calibrationpoints] t3 ON t3.[DutID]=t2.[DutID]
            
            WHERE  t1.Auftragsstart BETWEEN '''+startDate+''' AND '''+endDate+'''
            AND  t1.sapNumber LIKE '''+produkt+'''
            ''', cnxn)
         
        df = df.sort_values ( by = ['DateTime'] )
        df = df.dropna(subset = ['C0_CO0', 'C4_CO1', 'C5_CO2', 'C1_CG0', 'C6_CG1', 'C7_CG2']).reset_index(drop=True)
        df = df.drop_duplicates(subset=['ASSP'], ignore_index = True , keep = 'last')                                       
        df = df.astype({"C0_CO0":"int","C4_CO1":"int","C5_CO2":"int","C1_CG0":"int","C6_CG1":"int","C7_CG2":"int"})
        produkt = produkt[2:6]
        df['ErrorCode'] = df['ErrorCode'].astype(str)
        df['TDK_SN'] = df['TDK_SN'].astype(object)

        df['TL Pressure Sensivity'] = ((df['TL2_RawPressure'] - df['TL1_RawPressure']) / (df['TL2_ReferencePressure'] - df['TL1_ReferencePressure'])) /1000
        df['TM Pressure Sensivity'] = ((df['TM3_RawPressure'] - df['TM1_RawPressure']) / (df['TM3_ReferencePressure'] - df['TM1_ReferencePressure'])) /1000 
        df['TH Pressure Sensivity'] = ((df['TH2_RawPressure'] - df['TH1_RawPressure']) / (df['TH2_ReferencePressure'] - df['TH1_ReferencePressure'])) /1000
    except:
        print("Error: Error in Query")

    print('The dataframe df has ' + str(len(df.index)) + ' rows')
    return df


#------------------------------------------------------------------------------------------------------------
def vis_C0_CO0 (df,produkt):

    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C0_CO0') & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C0_CO0') & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C0_CO0') & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C0_CO0') & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = 'C0_CO0', color = 'ErrorCode', color_discrete_map = color_discrete_map, 
        category_orders = {'ErrorCode':sorted(df["ErrorCode"].unique().tolist(),key = len )},
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} C0_CO0 since {} to {}'.format(produkt,last_month,today)
        )
                    
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width =3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8  )

    fig.show() 
#------------------------------------------------------------------------------------------------------------
def vis_C4_CO1 (df,produkt):

    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C4_CO1') & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C4_CO1') & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C4_CO1') & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C4_CO1') & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = 'C4_CO1', color = 'ErrorCode', color_discrete_map = color_discrete_map, 
        category_orders = {'ErrorCode':sorted(df["ErrorCode"].unique().tolist(),key = len )},
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} C4_CO1 since {} to {}'.format(produkt,last_month,today)
        )
                    
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width =3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8  )

    fig.show() 
#------------------------------------------------------------------------------------------------------------
def vis_C5_CO2 (df,produkt):

    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C5_CO2') & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C5_CO2') & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C5_CO2') & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C5_CO2') & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = 'C5_CO2', color = 'ErrorCode', color_discrete_map = color_discrete_map, 
        category_orders = {'ErrorCode':sorted(df["ErrorCode"].unique().tolist(),key = len )},
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} C5_CO2 since {} to {}'.format(produkt,last_month,today)
        )
                    
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width =3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8  )

    fig.show()
#------------------------------------------------------------------------------------------------------------
def vis_C1_CG0 (df,produkt):

    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C1_CG0') & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C1_CG0') & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C1_CG0') & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C1_CG0') & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = 'C1_CG0', color = 'ErrorCode', color_discrete_map = color_discrete_map, 
        category_orders = {'ErrorCode':sorted(df["ErrorCode"].unique().tolist(),key = len )},
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} C1_CG0 since {} to {}'.format(produkt,last_month,today)
        )
                    
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width =3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8  )

    fig.show()
#------------------------------------------------------------------------------------------------------------
def vis_C6_CG1 (df,produkt):
    
    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C6_CG1') & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C6_CG1') & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C6_CG1') & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C6_CG1') & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = 'C6_CG1', color = 'ErrorCode', color_discrete_map = color_discrete_map, 
        category_orders = {'ErrorCode':sorted(df["ErrorCode"].unique().tolist(),key = len )},
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} C6_CG1 since {} to {}'.format(produkt,last_month,today)
        )
                    
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width =3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8  )

    fig.show()
#------------------------------------------------------------------------------------------------------------
def vis_C7_CG2 (df,produkt):
    
    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C7_CG2') & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C7_CG2') & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C7_CG2') & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == 'C7_CG2') & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = 'C7_CG2', color = 'ErrorCode', color_discrete_map = color_discrete_map, 
        category_orders = {'ErrorCode':sorted(df["ErrorCode"].unique().tolist(),key = len )},
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} C7_CG2 since {} to {}'.format(produkt,last_month,today)
        )
                    
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width =3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width =4, line_color ='red')

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8  )

    fig.show()
#-----------------------------------------------------------------------------------------------------------
def box_plot(df):
    import plotly.express as px
    for i in ['TL1_RawPressure','TL2_RawPressure','TM1_RawPressure','TM2_RawPressure','TM3_RawPressure', 'TH1_RawPressure', 'TH2_RawPressure']:
        fig = px.box( data_frame = df, x = 'Lot' , y = i , color = 'ErrorCode' , hover_data = ['Lot','DateTime'])   
        #if i in ['TL1_RawPressure','TM1_RawPressure','TH1_RawPressure']:
        #    fig.update_layout (yaxis_range= [   3000 ,  8000  ])
        #elif i in ['TL2_RawPressure','TM3_RawPressure','TH2_RawPressure']:                      # control the y-axis range manually
        #    fig.update_layout (yaxis_range= [  11000 , 19000   ])
        #else: 
        #    fig.update_layout (yaxis_range= [ 8000 , 13000 ])
        fig.show()

#------------------------------------------------------------------------------------------------------------ 
def vis_all_coeff(df,produkt):
    #print(df.columns[df.columns.str[2] == '_'])
    for coeff in df.columns[df.columns.str[2] == '_']:
        x = vis_coeff(df,produkt,coeff)
    return(x) 
#------------------------------------------------------------------------------------------------------------    
def vis_coeff(df,produkt,coeff):
    
    df['ErrorCode'] = df['ErrorCode'].astype(object)
    tol = coeff_limit(produkt)
    color_discrete_map = color_discrete_map_function()
   
    
    upper_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == coeff) & (tol['Type']=='War'),'Upper']
    lower_warning_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == coeff) & (tol['Type']=='War'),'Lower']
    upper_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == coeff) & (tol['Type']=='Aus'),'Upper']
    lower_Aus_limit = tol.loc[(tol['SAP_Number'] == produkt) & (tol['Cofficients'] == coeff) & (tol['Type']=='Aus'),'Lower']
   
    fig = px.scatter(
        df, x = 'DateTime', y = coeff, color = 'ErrorCode', color_discrete_map = color_discrete_map, #facet_col ='Sensor_Status',
        category_orders = {'ErrorCode': sorted(df["ErrorCode"].unique().tolist(),key = len)},        
        #category_orders = {'ErrorCode':['0','1','2','3','4','5','7','9','256','257','283','4094','4098','4099','9000','9003']},
        hover_data = ["Lot", "ASSP",'TDK_SN','Coefficients_Status'],
        height = 700,
        title = '{} {} since {} to {}'.format(produkt,coeff,last_month,today)
        )
    #print(upper_warning_limit)                
    fig.add_hline(y = upper_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color = 'orange')
    fig.add_hline(y = lower_warning_limit.item(), line_dash = 'dash', line_width = 3, line_color ='orange')
    fig.add_hline(y = upper_Aus_limit.item(), line_dash = 'solid',line_width = 4, line_color ='red')
    fig.add_hline(y = lower_Aus_limit.item(), line_dash = 'solid',line_width = 4, line_color ='red')   

    fig.update_layout(yaxis_range=[lower_Aus_limit.item()-3000 ,upper_Aus_limit.item()+3000 ])
    fig.update_traces(marker_size = 8)

    fig.show()
#------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------ 
def sensors_classification(df,tol):
   
    '''
    This function compares the values in each row of df with the threshold limits defined in tol. 
    It then returns a list of strings indicating whether the values are within the acceptable range, then IO 
    or if they are outside the limits (NIO_Ausschus), or if they are close to 
    the limits and require attention (Warning)

    param df is a pandas DataFrame containing the values to be compared.
    param tol is a pandas DataFrame containing the threshold limits for the values for each cofficients.
    return: list of strings containing the result of the comparison for each row in df.
    '''

    final_result = []    #This empty list will be filled with the final results of each row (Sensor).                                      
    for i in df.index:   #loops through all rows of df 
        
        result = []      #This empty list will store the results of each comparison for the current row in df.
        
        for j in range(int(len(tol)/2)): 
            # This for loop iterates over the threshold limits defined in tol.
            # The range function is for number of iteration 
            # The len() function returns the number of rows in tol.  
            # The int() function is used to convert the result to an integer.    
        
            if tol.iloc[2*j][3] < df.iloc[i][j+4] < tol.iloc[2*j][4] : 
                result.append('IO') 
                    #If the value in df is within the acceptable range, 'IO' is appended to result.
               
            elif tol.iloc[2*j+1][3] < df.iloc[i][j+4] < tol.iloc[2*j+1][4] :
                result.append('Warning')
                   #If the value in df is out of above limits, 'Warning' is appended to result.
            else:
                result.append('NIO_Ausschus')
                   #If the value in df is outside the acceptable range, 'NIO_Ausschus' is appended to result. 
        
        if 'NIO_Ausschus' in result:    
            final_result.append('NIO_Ausschus')  
            #If any of the results are 'NIO_Ausschus', the final_result list will be appended with 'NIO_Ausschus'.                  
        elif 'Warning' in result:
            final_result.append('Warning')
            #If none of the results are 'NIO_Ausschus' but there is at least one 'Warning', the final_result list will be appended with 'Warning'.
        else:                             
            final_result.append('IO_Sensor')
            #If none of the results are 'NIO_Ausschus' or 'Warning', the final_result list will be appended with 'IO_Sensor'.
    
  
    return final_result   # return the final result for each row (Sensor)
    return pd.Series(Sensors_classification(df,tol))
#----------------------------------------------------------------------------------------------------------
def coefficients_classification(df,tol):
    Sensor_status=[]
    for i in df.index: 
        test=''
        for j in range(int(len(tol)/2)): 
            
        
            if   tol.iloc[2*j][3] < df.iloc[i][j+4] <tol.iloc[2*j][4] : 
                         
                    test=test+'0'
            
            elif tol.iloc[2*j+1][3] < df.iloc[i][j+4] <  tol.iloc[2*j][3]:   #lower warning
                        
                    test=test+'1'
            
            elif df.iloc[i][j+4] <  tol.iloc[2*j+1][3]: #lower Aus
                         
                    test=test+'3'
            
            elif tol.iloc[2*j][4] < df.iloc[i][j+4] <  tol.iloc[2*j+1][4]: #upper warning
                        
                    test=test+'2'
               
            else:
                       
                    test=test+'4' #upper Aus
                    
        Sensor_status.append(test)    
    return  Sensor_status
    return pd.Series(coefficients_classification(df,tol))
#----------------------------------------------------------------------------------------------------------    
def Sensor_Coeff_status(df,tol):    
    
    coeff_status = []
    sensor_status = []    # This empty list will be filled with the final results of each row (Sensor).                                      
    for i in df.index: 
        
        
        result = [] 
        test = ''
        for j in range(int(len(tol)/2)): 
            # This for loop iterates over the threshold limits defined in ToL_product.
            # The range function is for number of iteration 
            # The len() function returns the number of rows in ToL_product.  
            # The int() function is used to convert the result to an integer.    
        
            if tol.iloc[2*j][3] < df.iloc[i][j+4] < tol.iloc[2*j][4]: 
                result.append('IO')
                test = test + '0'   
                     
            elif tol.iloc[2*j+1][3] < df.iloc[i][j+4] < tol.iloc[2*j+1][4]:
                result.append('Warning')
                if tol.iloc[2*j+1][3] < df.iloc[i][j+4] < tol.iloc[2*j][3]:
                    test = test + '1'  #means Lower Warning
                elif  tol.iloc[2*j][4]< df.iloc[i][j+4] < tol.iloc[2*j+1][4]:
                    test= test + '2'  # means upper warning 
                   
            else:
                result.append('NIO_Ausschus')
                if  df.iloc[i][j+4] < tol.iloc[2*j+1][3]:
                    test = test + '3'  # lower aus
                else:
                    test = test + '4' #upper aus
                    
        
        if 'NIO_Ausschus' in result:    
            sensor_status.append('NIO_Ausschus')  
            # If any of the results are 'NIO_Ausschus', the sensor_status list will be appended with 'NIO_Ausschus'.                  
        elif 'Warning' in result:
            sensor_status.append('Warning')
            # If none of the results are 'NIO_Ausschus' but there is at least one 'Warning', the sensor_status list will be appended with 'Warning'.
        else:                             
            sensor_status.append('IO_Sensor')
            # If none of the results are 'NIO_Ausschus' or 'Warning', the sensor_status list will be appended with 'IO_Sensor'.
        
 
        coeff_status.append(test)
    
    df['Sensor_Status'] = sensor_status  # store and create sensor_status in Sensor_Status column in df 
    df['Coefficients_Status'] = coeff_status    # store and create coeff_status in Coefficient_Status column in df
    
    return df

        
#---------------------------------------------------------------------------------------------------------
def coefficients_visualization(df,produkt):

    dff = df.groupby('Coefficients_Status').agg({'Coefficients_Status':'count'})
    dff.columns = ['Count']
    dff.reset_index(inplace = True)
    
    barchart = px.bar(                                                                  
    dff[dff.Coefficients_Status != '000000'].sort_values(by=['Count'], ascending=False).iloc[:7],
    x = 'Coefficients_Status',
    y = 'Count',
    hover_data=['Coefficients_Status'],
    height = 600, width = 1800,
    template = 'ggplot2',
    #template = 'seaborn',
    text='Count',
    title ='{} Number of coefficients status since {} up to {}'.format(produkt, last_month, today)
    )
       
    barchart.update_layout(
    xaxis_tickangle = -55,
    xaxis_tickfont = dict(size=14),
    xaxis_nticks = 170,
    )

    barchart.update_xaxes(
    tickmode = 'array',
    dtick = 1,
    tick0 = 1   
    )   
   
    barchart.update_traces(textfont_size = 14, textposition = 'outside', cliponaxis = False)
    #barchart.write_image('{}-Coefficients since {} to {}.png'.format(produkt[2:6],last_month,today))
            
    return barchart
#---------------------------------------------------------------------------------------------------------
def sensor_visualization(df,produkt):

    df['TDK_SN'] = df['TDK_SN'].astype(object)
    df = df.groupby(['Lot','Sensor_Status']).agg({'Sensor_Status':'count','DateTime':'max','TDK_SN':'min'})
    df.columns=['Count','Date & Time','TDK_SN'] #changing the name of the columns
    df.reset_index(inplace=True)
    
    category_orders = {'Sensor_Status':['IO_Sensor','Warning','NIO_Ausschus']}
    #color_map = {'IO_Sensor':'green','Warning':'orange','NIO_Ausschus':'red'}         #give the color names manualy
    color_map = {'IO_Sensor':'rgb(141,182,60)','Warning':'rgb(255,160,0)','NIO_Ausschus':'rgb(253,51,51)'}    # give the colors by rgb and control the colors      
    
    
    barchart = px.bar(                                                               
        data_frame =  df.sort_values(by = ['Date & Time'], ascending = True),
        x = 'Lot',
        y = 'Count',                           
        color ='Sensor_Status',
        category_orders = category_orders,                                                                
        color_discrete_map = color_map,
        hover_data=['Date & Time','TDK_SN'],
        text_auto = True, # shows the number of each sensor status in top of bar plot 
        height = 600, width = 1750,
        template = 'ggplot2',
        #text='Count',
        title ='{} since {} to {}'.format(produkt,last_month,today),
        )  
    barchart.update_traces(textfont_size = 18, textangle = 0, textposition="outside", cliponaxis = False)    
    
    barchart.update_layout(
        xaxis_tickangle = -45,
        xaxis_tickfont = dict(size=14),
        xaxis_nticks = 50
        )

    
    barchart.update_xaxes(    # shows all the ticks on x-axis
        tickmode = 'linear',
        tick0 =  0,
        dtick = 1
        )
    #barchart.update_traces(textfont_size = 14, textposition = 'outside', cliponaxis = False)
    
    #barchart.write_image('{} since {} to {}.png'.format(produkt[2:6],last_month,today))
    
    return barchart
#---------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
def optional_sensors_visualization(df, status):   ##############

    df = df.groupby(['Lot','Sensor_Status']).agg({'Sensor_Status':'count','DateTime':'max'}) # keep the main df   
    df.columns=['Count','Date & Time'] #changing the name of the columns
    df.reset_index(inplace = True) 
    
    barchart = px.bar(                                                               
        data_frame=df[df['Sensor_Status'] == status].sort_values(by=['Date & Time'], ascending=True),
        x='Lot',
        y='Count',
        height=600, 
        width=900,
        hover_data=['Date & Time'],
        template='ggplot2',
        title='{} {} since {} to {}'.format(produkt, status, last_month, today)
        ) 
    barchart.update_layout(
        xaxis_tickangle=-60,
        xaxis_tickfont=dict(size=14),
        xaxis_nticks=170,
        )
    barchart.update_xaxes(
        tickmode='linear',
        dtick= 2
    )
    barchart.write_image('{} {} since {} to {}.png'.format(produkt, status, last_month, today))
    return barchart 
#-----------------------------------------------------------------------------------------------------------------


def R_square_TM(df):
    #df.index.to_numpy()
    
    for i in range(len(df)):
        x = df[['TM1_ReferencePressure','TM2_ReferencePressure','TM3_ReferencePressure']].iloc[i]
        y = df[['TM1_RawPressure','TM2_RawPressure','TM3_RawPressure']].iloc[i]
        p = np.polyfit(x,y,2)
        print(p)
        #correlation_mat = np.corrcoef(x,y)
        #correlation_r = correlation_mat[0,1]
        #R_squared = correlation_r**2
        #df.at[i,'R_Square_Reference_P_for_TM'] = R_squared 
        #df.at[i,'Coeff x= ref P/ y=raw P'] = p
#-----------------------------------------------------------------------------------------------------------------------

def calculate_fit_coeffs(x,y):    # johnsen function study it----- in tabe coeff fit curve ro mide va rsq ro  va zirish 
    p = np.polyfit(x,y,2)
    correlation_mat = np.corrcoef(x,y)
    correlation_r = correlation_mat[0,1]
    Rsq = correlation_r**2
    return p, Rsq
#--------------------------------------------------------------------------------
def fit_coeffs_df(df, variable_case):    # johnsen function study it  ---------------- ro in kar kon dashti kar mikardi 

    if variable_case == "NL_Temperature_P1":
        x_vars = ['TL1_ReferenceTemperature','TM1_ReferenceTemperature','TH1_ReferenceTemperature']
        y_vars = ['TL1_RawPressure','TM1_RawPressure','TH1_RawPressure']
    
    elif variable_case == "NL_Temperature_P2":
        x_vars = ['TL2_ReferenceTemperature','TM3_ReferenceTemperature','TH2_ReferenceTemperature']
        y_vars = ['TL2_RawPressure','TM3_RawPressure','TH2_RawPressure']
        
    elif variable_case == "NL_Pressure_TM":
        x_vars = df[['TM1_ReferencePressure','TM2_ReferencePressure','TM3_ReferencePressure']]
        y_vars = df[['TM1_RawPressure','TM2_RawPressure','TM3_RawPressure']]
    
        for i in range(len(df)) :
            df.loc[i,x_vars].to_numpy()
        #for i in [0,1,2]:
            #print(df.iloc[i])
        #    x = x_vars.iloc[i]
        #    y = y_vars.iloc[i]
    
    # # create an empty dataframe
    # for i in range(len(x)):

    #     p,Rsq = calculate_fit_coeffs(x,y)
    #     df.iloc[i, "a"] = p[0]
    #     df.iloc[i, "b"] = p[1]
    #     df.iloc[i, "c"] = p[2]
    #     df.iloc[i, "Rsq"] = Rsq
    #return df
#---------------------------------------------------------------------------------------------

def R_square_T_Offset(df):
    #df.index.to_numpy()
    
    for i in range(len(df)):
        x = df[['TL1_ReferenceTemperature','TM1_ReferenceTemperature','TH1_ReferenceTemperature']].iloc[i]
        y = df[['TL1_RawPressure','TM1_RawPressure','TH1_RawPressure']].iloc[i]
        p = np.polyfit(x,y,2)
        #print(p)
        #correlation_mat = np.corrcoef(x,y)
        #correlation_r = correlation_mat[0,1]
        #R_squared = correlation_r**2
        #df.at[i,'R_Square_Reference_T_offset'] = R_squared
        #df.at[i,'Coeff x= ref T/ y = raw P'] = p
#----------------------------------------------------------------------------------------------------------------------------
def R_square_T_Gain(df):
    #df.index.to_numpy()
    
    for i in range(len(df)):
        x = df[['TL2_ReferenceTemperature','TM3_ReferenceTemperature','TH2_ReferenceTemperature']].iloc[i]
        y = df[['TL2_RawPressure','TM3_RawPressure','TH2_RawPressure']].iloc[i]
        p = np.polyfit(x,y,2)
        #print(p)
        #correlation_mat = np.corrcoef(x,y)
        #correlation_r = correlation_mat[0,1]
        #R_squared = correlation_r**2
        #df.at[i,'R_Square_Reference_T_Gain'] = R_squared 
        #df.at[i,'Coeff x=ref T/ y=raw P'] = p
#------------------------------------------------------------------------------------------------------------------------        


def color_discrete_map_function():
    color_discrete_map = {'0':'rgb(141,182,0)','4':'rgb(25,30,50)','4094':'rgb(226,109,109)','4095':'rgb(239,222,205)', '4096':'rgb(145,92,131)', '4097':'rgb(255,191,0)',
                      '4098':'rgb(165,42,42)', '4099':'rgb(255,153,102)', '4100':'rgb(178,190,181)', '256':'rgb(229,43,80)',
                      '257':'rgb(153,102,204)', '258':'rgb(233,214,107)', '259':'rgb(110,127,128)','260':'rgb(0,127,255)',
                      '261':'rgb(137,207,240)','262':'rgb(161,202,241)','263':'rgb(244,194,194)', '264':'rgb(33,171,205)',
                      '265':'rgb(250,231,181,)','266':'rgb(255,255,53)', '267':'rgb(132,132,130)', '268':'rgb(152,119,123)',   
                      '269':'rgb(188,212,230)', '270':'rgb(159,129,112)', '271':'rgb(245,245,220)','272':'rgb(255,228,196)',
                      '273':'rgb(61,43,31)', '274':'rgb(254,111,94)','275':'rgb(255,235,205)', '277':'rgb(49,140,231)',
                      '278':'rgb(172,229,238)', '280':'rgb(250,240,190)','281':'rgb(162,162,208)','282':'rgb(102,153,204)',
                      '283':'rgb(255,191,10)','1000':'rgb(13,152,186)','1024':'rgb(138,43,226)','2000':'rgb(222,93,131)',
                      '3000':'rgb(131,68,59)','4000':'rgb(0,149,182)','5000':'rgb(227,218,201)','6000':'rgb(204,0,0)',
                      '7000':'rgb(0,106,78)', '8000':'rgb(135,50,96)','8001':'rgb(255,3,62)','8002':'rgb(181,166,66)',
                      '9000':'rgb(203,65,84)','9001':'rgb(29,172,214)','9002':'rgb(191,148,228)','9003':'rgb(100,140,150)',
                      '9261':'rgb(255,0,127)','9262':'rgb(8,232,222)','9263':'rgb(209,159,232)','9264':'rgb(244,187,255)',
                      '9265':'rgb(255,85,163)','9266':'rgb(254,96,127)','9267':'rgb(0,66,37)','9268':'rgb(205,127,50)',
                      '9269':'rgb(165,42,42)','9270':'rgb(255,193,204)','9271':'rgb(240,220,130)','9272':'rgb(72,6,7)',
                      '9273':'rgb(128,0,32)','9274':'rgb(222,184,135)','9275':'rgb(204,85,0)','9276':'rgb(233,116,81)',
                      '9278':'rgb(138,51,36)','9279':'rgb(189,51,164)','10000':'rgb(112,41,99)','10001':'rgb(0,122,165)',
                      '10002':'rgb(224,60,49)','10003':'rgb(83,104,114)','10004':'rgb(95,158,160)','10005':'rgb(145,163,176)',
                      '10006':'rgb(237,135,45)','10007':'rgb(227,0,34)','10008':'rgb(166,123,91)','1':'rgb(20,20,70)'}  
    return color_discrete_map
#---------------------------------------------------------------------------------------------------------------------------------
def coeff_limit(produkt):
    tol = pd.DataFrame(data =[['B632','C0_CO0','War',-12248,-8276],['B632','C0_CO0','Aus',-16220,-4304],   
                          ['B632','C4_CO1','War',1365,3333],['B632','C4_CO1','Aus',-603,5301],
                          ['B632','C5_CO2','War',-1078,-406],['B632','C5_CO2','Aus',-1750,266],
                          ['B632','C1_CG0','War',17927,24139],['B632','C1_CG0','Aus',11715,30351],
                          ['B632','C6_CG1','War',-14554,-10160],['B632','C6_CG1','Aus',-18948,-5766],
                          ['B632','C7_CG2','War',2198,3676],['B632','C7_CG2','Aus',721,5153],
                          ['B701','C0_CO0','War',-16374,-12956],['B701','C0_CO0','Aus',-19793,-9537],
                          ['B701','C4_CO1','War',4254,7246],['B701','C4_CO1','Aus',1262,10238],
                          ['B701','C5_CO2','War',-1914,-1106],['B701','C5_CO2','Aus',-2721,-299],
                          ['B701','C1_CG0','War',18207,24553],['B701','C1_CG0','Aus',11861,30899],
                          ['B701','C6_CG1','War',-15376,-11952],['B701','C6_CG1','Aus',-18799,-8529],
                          ['B701','C7_CG2','War',2550,4268],['B701','C7_CG2','Aus',831,5987],
                          ['B722','C0_CO0','War',466,4697],['B722','C0_CO0','Aus',-3765,8928],
                          ['B722','C4_CO1','War',-10475,-4199],['B722','C4_CO1','Aus',-16831,2237],
                          ['B722','C5_CO2','War',611,3272],['B722','C5_CO2','Aus',-2050,5933],
                          ['B722','C1_CG0','War',16000,23000],['B722','C1_CG0','Aus',9000,30000],
                          ['B722','C6_CG1','War',-12000,-9000],['B722','C6_CG1','Aus',-15000,-6000],
                          ['B722','C7_CG2','War',1549,2700],['B722','C7_CG2','Aus',398,3851],
                          ['B602','C0_CO0','War',-7840,-5470],['B602','C0_CO0','Aus',-10220,-3090],
                          ['B602','C4_CO1','War',1320,2430],['B602','C4_CO1','Aus',210,3540],
                          ['B602','C5_CO2','War',-850,220],['B602','C5_CO2','Aus',-1920,1290],
                          ['B602','C1_CG0','War',5780,9000],['B602','C1_CG0','Aus',2550,12230],
                          ['B602','C6_CG1','War',-1390,2390],['B602','C6_CG1','Aus',-5180,6180],
                          ['B602','C7_CG2','War',900,3860],['B602','C7_CG2','Aus',-2060,6820],
                          ['B657','C0_CO0','War',5245,6799],['B657','C0_CO0','Aus',3691,8353],
                          ['B657','C4_CO1','War',2593,4163],['B657','C4_CO1','Aus',1023,5733],
                          ['B657','C5_CO2','War',1282,2684],['B657','C5_CO2','Aus',-120,4086],
                          ['B657','C1_CG0','War',16014,19208],['B657','C1_CG0','Aus',12820,22402],
                          ['B657','C6_CG1','War',7381,9305],['B657','C6_CG1','Aus',5457,11229],
                          ['B657','C7_CG2','War',2616,3654],['B657','C7_CG2','Aus',1578,4692],
                          ['B  6','C0_CO0','War',1480,2530],['B  6','C0_CO0','Aus',440,3580],
                          ['B  6','C4_CO1','War',-450,4060],['B  6','C4_CO1','Aus',-4950,8560],
                          ['B  6','C5_CO2','War',-2340,1000],['B  6','C5_CO2','Aus',-5680,4330],
                          ['B  6','C1_CG0','War',8780,12850],['B  6','C1_CG0','Aus',4710,16920],
                          ['B  6','C6_CG1','War',-10780,-2110],['B  6','C6_CG1','Aus',-19460,6570],
                          ['B  6','C7_CG2','War',5950,23490],['B  6','C7_CG2','Aus',-11600,41040],
                          ['B631','C0_CO0','War',-1090,1260],['B631','C0_CO0','Aus',-3450,3620],
                          ['B631','C4_CO1','War',-500,-110],['B631','C4_CO1','Aus',-900,280],
                          ['B631','C5_CO2','War',-700,-390],['B631','C5_CO2','Aus',-1020,-70],
                          ['B631','C1_CG0','War',11980,13770],['B631','C1_CG0','Aus',10190,15560],
                          ['B631','C6_CG1','War',5560,6780],['B631','C6_CG1','Aus',4350,7990],
                          ['B631','C7_CG2','War',2690,3510],['B631','C7_CG2','Aus',1870,4320],
                          ['B714','C0_CO0','Aus',-4178,1909],
                          ['B714','C4_CO1','Aus',-3071,-153],
                          ['B714','C5_CO2','Aus',-4625,2633],
                          ['B714','C1_CG0','Aus',7879,15831],
                          ['B714','C6_CG1','Aus',2401,9495],
                          ['B714','C7_CG2','Aus',-5038,11598],
                          ['B569','C0_CO0','War',-4871,1909],
                          ['B569','C4_CO1','War',-3071,-153],
                          ['B569','C5_CO2','War',-4625,2633],
                          ['B569','C1_CG0','War',7879,15831],
                          ['B569','C6_CG1','War',2401,9495],
                          ['B569','C7_CG2','War',-5038,11598]],                      
             
                          columns=['SAP_Number','Cofficients','Type','Lower','Upper'])
                          
    return tol[tol["SAP_Number"] == produkt]
#------------------------------------------------------------------------------------------------------------------------------   


def vis_RawPressure(df,produkt): 
    import plotly.express as px
    color_map = {'IO_Sensor':'rgb(141,182,60)','Warning':'rgb(255,160,0)','NIO_Ausschus':'rgb(253,51,51)'} 
    
    for i in ['TL1_RawPressure','TL2_RawPressure','TM1_RawPressure','TM3_RawPressure','TH1_RawPressure','TH2_RawPressure']:
        fig =px.scatter(df,x='DateTime', y=i
                ,color ='Sensor_Status' ,color_discrete_map = color_map  
                ,hover_data = ["Lot", "ASSP",'TDK_SN','ErrorCode','Coefficients_Status']  
                ,title = '{} for {} since {} to {}'.format(i,produkt,last_month,today)        
                )
        
        #if i in ['TL1_RawPressure','TM1_RawPressure','TH1_RawPressure']:
        #    fig.add_hline(y = -550, line_dash = 'dash', line_width =3, line_color ='orange')
        #    fig.add_hline(y = 2440, line_dash = 'dash', line_width =3, line_color ='orange')
        #else:
        #    fig.add_hline(y = 5690, line_dash = 'dash', line_width =3, line_color ='orange')
        #    fig.add_hline(y = 11370, line_dash = 'dash', line_width =3, line_color ='orange')
        
        fig.update_traces(marker_size=8)

        #if i in ['TL1_RawPressure','TM1_RawPressure','TH1_RawPressure']:
        #    fig.update_layout(yaxis_range=[-1000 , 3000])
        #else:
        #    fig.update_layout(yaxis_range=[4000 , 12500])
       
        fig.show()
#--------------------------------------------------------------------------------------------------------------------------------
def  vis_oven_Sensivity(df,produkt):
    import plotly.express as px
    color_map = {'IO_Sensor':'rgb(141,182,60)','Warning':'rgb(255,160,0)','NIO_Ausschus':'rgb(253,51,51)'} 

    for i in ['TL Pressure Sensivity','TM Pressure Sensivity','TH Pressure Sensivity']:
        fig =px.scatter (df,x='DateTime',y = i
                ,color ='Sensor_Status', color_discrete_map = color_map   
                ,hover_data = ["Lot", "ASSP",'TDK_SN','ErrorCode','Coefficients_Status']   
                ,title = '{} for {} since {} to {}; Unit--> digit / mbar'.format(i,produkt,last_month,today))

        fig.update_traces(marker_size=8)
        #fig.update_layout(yaxis_range=[-0.1 , 2])
        fig.show()