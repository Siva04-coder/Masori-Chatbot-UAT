import pandas as pd
import mysql.connector
import config

cfg = config.Config()

config_details = cfg.get_database_configs()

db_user=config_details['db_user']
db_pass=config_details['db_pass']
db_host=config_details['db_host']
database=config_details['db_name']
db_port= config_details['db_port']

def UpdateDB(corpus_filename, corpus_sheetname):

    #Patient_Website_Data
    #HCP_Website_Data
    print(corpus_filename, corpus_sheetname)

    cnx = mysql.connector.connect(user=db_user, password=db_pass,
                                host=db_host, port=db_port,
                                database=database)
    print('con object')
    cursor = cnx.cursor()
    print('cursor created')

    corpus = pd.read_excel(corpus_filename, engine='openpyxl',
                        sheet_name=corpus_sheetname)
    print('corpus')
    Site_Area = ''
    Functionality_Area = ''
    print('Started')
    for index, row in corpus.iterrows():
        if str(row['Question']).lower() != 'nan':
            
            if str(row["Site_Area"]).lower() != 'nan':
                Site_Area = str(row["Site_Area"])

            if str(row["Functionality_Area"]).lower() != 'nan':
                Functionality_Area = str(row["Functionality_Area"])

            query = "INSERT INTO website_data " + \
            "(Site_Area,Functionality_Area,Keywords,Intents,Question,Display_Type,Output,Bullets,Video_Url,Hyperlink_Text,Hyperlink_URL,Image_URL) " + \
            "values ('"+ \
            Site_Area+"','" + \
            Functionality_Area.replace("'", "''")+"','" + \
            str(row["Keywords"]).replace("'", "''")+"','" + \
            str(row["Intents"]).replace("'", "''")+"','" + \
            str(row["Question"]).replace("'", "''")+"','" + \
            str(row["Display_Type"])+"','" + \
            str(row["Output"]).replace("'", "''")+"','" + \
            str(row["Bullets"]).replace("'", "''")+"','" + \
            str(row["Video URL"]).replace("'", "''")+"','" + \
            str(row["Hyperlink Text"]).replace("'", "''")+"','" + \
            str(row["Hyperlink URL"]).replace("'", "''")+"','" + \
            str(row["Image URL"]).replace("'", "''") + "')"

            cursor.execute(query)

            if '\n' in str(row["Entities"]):
                entities = str(row["Entities"]).split('\n')

                for entity in entities:
                    master_query = "INSERT INTO master_intent_entity_mapping (Intent, Site_Area, Entities) values ('" + \
                    str(row["Intents"]).replace("'", "''")+"','" + \
                    Site_Area+"','" + \
                    str(entity).replace("'", "''")+"')"
                    print(master_query)
                    cursor.execute(master_query)
            else:
                master_query = "INSERT INTO master_intent_entity_mapping (Intent, Site_Area, Entities) values ('" + \
                    str(row["Intents"]).replace("'", "''")+"','" + \
                    Site_Area+"','" + \
                    str(row["Entities"]).replace("'", "''")+"')"
                print(master_query)
                cursor.execute(master_query)
    cnx.commit()
    cnx.close()
    print('Completed')
    #break
