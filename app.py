from flask import Flask,request,render_template
from withings_api import WithingsAuth, WithingsApi, AuthScope
from withings_api.common import get_measure_value,MeasureType
from urllib import parse
import requests

app=Flask(__name__)

clientid="79752e7d20f15ecc90ec3b6667d0253db3f90d199d94f5e4059986261942e6ac"
consumer_secrete="25957f167a87e73177286c8b379946e1658db6978184680f931014ba37324521"
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
        


if __name__=="__main__":
    app.run()
