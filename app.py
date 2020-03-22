from flask import Flask,request,render_template
from withings_api import WithingsAuth, WithingsApi, AuthScope
from withings_api.common import get_measure_value,MeasureType
from urllib import parse
import requests

from flask import Flask,request,render_template,jsonify
import json
app=Flask(__name__)

clientid="7f5486f78731e761c99878e8e37d540f5868a99c12a16089be227b372a366c36"
consumer_secrete="efa34f8ae8542f4de35ce0a4b7108421e3d32a6bd9ae8eecc0d8efcb6ff29d7a"
calbackuri="https://vocobot.herokuapp.com/"

auth = WithingsAuth(
    client_id=clientid,
    consumer_secret=consumer_secrete,
    callback_uri=calbackuri,
    scope=(
        AuthScope.USER_ACTIVITY,
        AuthScope.USER_METRICS,
        AuthScope.USER_INFO,
        AuthScope.USER_SLEEP_EVENTS,
    )
)

@app.route("/",methods=["POST","GET"])
@app.route("/",methods=["GET","POST"])
def index():
    authorize_url = auth.get_authorize_url()
    return render_template("index.html",url=authorize_url)

@app.route("/authorize",methods=["POST","GET"])
def authorize():
    if request.method=="POST":
        data=request.form
        urlcode=data["url"]
        redirected_uri_params = dict(
             parse.parse_qsl(parse.urlsplit(urlcode).query)
         )
        auth_code = redirected_uri_params["code"]
        text_file = open("credentials.txt", "w")
        n = text_file.write(auth_code)
        text_file.close()
        file =open("credentials.txt", "r")
        aa=file.readline()
        file.close()
        credentials = auth.get_credentials(auth_code)
        api = WithingsApi(credentials)
        meas_result = api.measure_get_meas()
        weight_or_none = get_measure_value(meas_result, with_measure_type=MeasureType.WEIGHT)
        fat=get_measure_value(meas_result,with_measure_type=MeasureType.FAT_MASS_WEIGHT)
        musle_mass = get_measure_value(meas_result, with_measure_type=MeasureType.MUSCLE_MASS)
        bone_mass = get_measure_value(meas_result, with_measure_type=MeasureType.BONE_MASS)
        body_water = get_measure_value(meas_result, with_measure_type=MeasureType.HYDRATION)
        heart_rate = get_measure_value(meas_result, with_measure_type=MeasureType.HEART_RATE)
        pluse_vave_velicity = get_measure_value(meas_result, with_measure_type=MeasureType.PULSE_WAVE_VELOCITY)
        return render_template("showdata.html",w=weight_or_none,f=fat,musle_mass=musle_mass,bone_mass=bone_mass,body_water=body_water,heart_rate=heart_rate,pvv=pluse_vave_velicity)
    return "credentials"



        data=request.data
        data=data.decode()
        data=json.loads(data)
        msg=data["msg"]
        return jsonify({"data":"ok...."})
if __name__=="__main__":
    app.run()
