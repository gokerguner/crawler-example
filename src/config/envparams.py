import json


class Params(object):
    """
    Define class wide objects to __dict__

    see here https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide

    """

    DEBUG = None
    DEBUG_LOG_FILE = None
    DEBUG_LOG_LEVEL = None
    DB_HOST_IP = None
    DB_HOST_PORT = None
    MAXSEVSELDELAY = None
    DB_NAME = None
    DB_HEPSIBURADA_COLLECTION = None
    DB_REPLICA_SET_NAME = None
    DB = None

    def __init__(self, param_file_path="./params.json"):
        # in object level this class wide objects can be changed
        self._jparams = None
        self.load_params(param_file_path)

    def set_debug_status(self, status):
        self.DEBUG = status

    def set_param(self, param_name, new_val):
        if param_name in self._jparams:
            setattr(self, param_name, new_val)
            return True
        else:
            return False

    def load_params(self, param_file_path):
        """
        parameter initialization (param.json and defaults)

        """
        self._jparams = self.load_json_obj(param_file_path)
        if "DB" in self._jparams:
            self.DB = self._jparams["DB"]
        else:
            self.DB = "ecomm"
        if "DB_HEPSIBURADA_COLLECTION" in self._jparams:
            self.DB_HEPSIBURADA_COLLECTION = self._jparams["DB_HEPSIBURADA_COLLECTION"]
        else:
            self.DB_HEPSIBURADA_COLLECTION = "hepsiburada"
        if "DB_HEPSIBURADA_COMMENTS_COLLECTION" in self._jparams:
            self.DB_HEPSIBURADA_COMMENTS_COLLECTION = self._jparams["DB_HEPSIBURADA_COMMENTS_COLLECTION"]
        else:
            self.DB_HEPSIBURADA_COMMENTS_COLLECTION = "hepsiburada_comments"

        if "DB_HOST_IP" in self._jparams:
            self.DB_HOST_IP = self._jparams["DB_HOST_IP"]
        else:
            self.DB_HOST_IP = "127.0.0.1"

        if "DB_HOST_PORT" in self._jparams:
            self.DB_HOST_PORT = self._jparams["DB_HOST_PORT"]
        else:
            self.DB_HOST_PORT = 27017

        if "MAXSEVSELDELAY" in self._jparams:
            self.MAXSEVSELDELAY = self._jparams["MAXSEVSELDELAY"]
        else:
            self.MAXSEVSELDELAY = 1000

    @staticmethod
    def load_json_obj(param_file_path):
        '''Load json object from PARAM_FILE_PATH file'''
        json_data = open(param_file_path)
        _jparams = json.load(json_data)
        json_data.close()
        return _jparams
