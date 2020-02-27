from flask import Flask
from withings_api import WithingsAuth, WithingsApi, AuthScope
from withings_api.common import get_measure_value,MeasureType
from urllib import parse

app=Flask(__name__)

clientid="7f5486f78731e761c99878e8e37d540f5868a99c12a16089be227b372a366c36"
consumer_secrete="efa34f8ae8542f4de35ce0a4b7108421e3d32a6bd9ae8eecc0d8efcb6ff29d7a"

@app.route("/",methods=["POST","GET"])
def index():
    return "helo world"

if __name__=="__main__":
    app.run()
