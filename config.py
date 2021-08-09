import os


def getUploadPass():
    return '1'  # os.environ.get('SENHA_UPLOAD')


def getDBConnectionString():
    DB_USER = os.environ.get('DB_USER')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PASS = os.environ.get('DB_PASS')
    DB_SCHEMA = os.environ.get('DB_SCHEMA')

    return """mysql+mysqldb://{}:{}@{}/{}?charset=utf8mb4""".format(
        DB_USER, DB_PASS, DB_HOST, DB_SCHEMA)
