import datetime


class CONSTANT(object):
    Tushare_Token = '06c9576b7f573a6462a9e73c1c52f8693843e75b0d8fa479ac1ae14b'
    Tiing_Token = 'b7a15eba793718ba9b06bc3d670aaef740d267e4'
    Database_Url = '127.0.0.1:3306'
    Database_User = 'programuser'
    Database_pswd = 'Abcd1234'
    Database_name = 'gina_stock02'
    Database_Url2 = 'mysql+pymysql://programuser:Abcd1234@127.0.0.1:3306/gina_stock02'
    LABEL_THRED = 0.05
    MODELSAVED_PATH='ModelSaved/'
    DATASIZE=1200
    DATE_FORMAT_US="%Y-%m-%d"
    WEIGHTS_FILEPATH='weight.h5'

def datetimestr():
    now = datetime.datetime.now()
    str =now.strftime("%Y%m%d%H%m")
    return str

def nowdatestr():
    now = datetime.datetime.now()
    str = now.strftime("%Y%m%d")
    return str

def model_filepath():
    daystr = datetimestr()
    #str = CONSTANT.MODELSAVED_PATH+daystr+"_model.h5"
    str = daystr+"_model.h5"
    return str

def weights_filepath():
    daystr = datetimestr()
    #str = CONSTANT.MODELSAVED_PATH+daystr+"_weight.h5"
    str = daystr+"_weight.h5"
    return str
