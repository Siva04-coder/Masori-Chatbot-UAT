#region packages
import pandas as pd
import mysql.connector
from config import Config
#endregion

#region declarations

#endregion

class DBProxy:
    #region declarations
    configs = Config()
    db_configs = configs.get_database_configs()
    #endregion

    #region database queries and stored procedures 
    
    #endregion

    def __init__(self):
        cnx = mysql.connector.connect(
        user=db_configs["db_user"], 
        password=db_configs["db_pass"],
        host=db_configs["db_host"], 
        port=db_configs["db_port"],
        database=db_configs["db_name"])
