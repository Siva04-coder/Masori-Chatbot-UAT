#region packages
import configparser, os, sys
#endregion

#region declarations
config = configparser.ConfigParser()
#endregion

class Config:
    #region declarations
    configFilePath = 'app.cfg'
    #endregion

    def get_database_configs(self):
        self.cfgDict = {}

        try:
            config.read(self.configFilePath)

            db_user = str(config.get('Database', 'db_user'))
            db_pass = str(config.get('Database', 'db_pass'))
            db_host = str(config.get('Database', 'db_host'))
            db_name = str(config.get('Database', 'db_name'))
            db_port = str(config.get('Database', 'db_port'))

            self.cfgDict.update({'db_user': db_user})
            self.cfgDict.update({'db_pass': db_pass})
            self.cfgDict.update({'db_host': db_host})
            self.cfgDict.update({'db_name': db_name})
            self.cfgDict.update({'db_port': db_port})
        except Exception as e:
            pass

        return self.cfgDict

    def get_app_configs(self):
        self.cfgDict = {}

        try:
            config.read(self.configFilePath)

            chat_clear_buffer_min = str(config.get('AppConfigs', 'chat_clear_buffer_min'))

            self.cfgDict.update({'chat_clear_buffer_min': chat_clear_buffer_min})
            
        except Exception as e:
            pass

        return self.cfgDict

    def get_ui_configs(self):
        self.cfgDict = {}

        try:
            config.read(self.configFilePath)

            chat_timeout_sec = str(config.get('UIConfigs', 'chat_timeout_sec'))

            self.cfgDict.update({'chat_timeout_sec': chat_timeout_sec})
            
        except Exception as e:
            pass

        return self.cfgDict
