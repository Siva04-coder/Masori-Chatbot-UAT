import pandas as pd

corpus_path = 'Corpus/MLR_Corpus.xlsx'
message_path = 'Corpus/Default_Messages.xlsx'

def get_welcome_message():
    msg_corpus = pd.read_excel(message_path, engine='openpyxl', sheet_name='Sheet1')
    welcome_message = ''
    for index, row in msg_corpus.iterrows():
        if str(row['Message_Type']) == 'welcome':
            welcome_message = str(row['Message'])
    
    return welcome_message

def update_master_intent_entity_data():
    corpus = pd.read_excel(corpus_path, engine='openpyxl',
                            sheet_name='website_data')

    print('Started')

    data = []

    for index, row in corpus.iterrows():
        if str(row['Question']).lower() != 'nan':
            
            if str(row["Site_Area"]).lower() != 'nan':
                Site_Area = str(row["Site_Area"])

            if str(row["Functionality_Area"]).lower() != 'nan':
                Functionality_Area = str(row["Functionality_Area"])

            if '\n' in str(row["Entities"]):
                entities = str(row["Entities"]).split('\n')

                for entity in entities:
                    if str(row["Intents"]).replace("'", "''") != 'nan' and str(entity).replace("'", "''") != 'nan':
                        data.append([Site_Area, str(row["Intents"]).replace("'", "''"), str(entity).replace("'", "''")])
                    
            else:
                if str(row["Intents"]).replace("'", "''") != 'nan' and str(row["Entities"]).replace("'", "''") != 'nan':
                    data.append([Site_Area, str(row["Intents"]).replace("'", "''"), str(row["Entities"]).replace("'", "''")])
                            

    print(data)

    df = pd.DataFrame(data, columns = ['Site_Area', 'Intents', 'Entities'])

    print(df)

    with pd.ExcelWriter(corpus_path) as writer1:
        corpus.to_excel(writer1, sheet_name = 'website_data', index = False)
        df.to_excel(writer1, sheet_name = 'master_intent_entity_mapping', index = False)

    return 'Updated'


def get_HCP_data():
    corpus = pd.read_excel(corpus_path, engine='openpyxl',
                            sheet_name='Nuplazid HCP')

    data = []

    for index, row in corpus.iterrows():

        if str(row['Sub Functional Area']).lower() != 'nan':
            
            Site_Area = 'HCP'
            Functionality_Area = ''
            Entities = ''
            Intent = ''

            if str(row["Functional Area"]).lower() != 'nan':
                Functionality_Area = str(row["Functional Area"])

            if str(row["Keyword"]).lower() != 'nan':
                Entities = str(row["Keyword"]).replace("'", "''")

            if str(row["Sub Functional Area"]).lower() != 'nan':
                Entities = str(row["Sub Functional Area"]).replace("'", "''")

            data.append([Site_Area, Intent, Entities])

            # if '\n' in str(row["Entities"]):
            #     entities = str(row["Entities"]).split('\n')

            #     for entity in entities:
            #         if str(row["Intents"]).replace("'", "''") != 'nan' and str(entity).replace("'", "''") != 'nan':
            #             data.append([Site_Area, str(row["Intents"]).replace("'", "''"), str(entity).replace("'", "''")])
                    
            # else:
            #     if str(row["Intents"]).replace("'", "''") != 'nan' and str(row["Entities"]).replace("'", "''") != 'nan':
            #         data.append([Site_Area, str(row["Intents"]).replace("'", "''"), str(row["Entities"]).replace("'", "''")])
                

    df = pd.DataFrame(data, columns = ['Site_Area', 'Sub Functional Area', 'Keyword'])

    return corpus, df
