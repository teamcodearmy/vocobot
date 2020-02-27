from flask import Flask,request,render_template
from withings_api import WithingsAuth, WithingsApi, AuthScope
from withings_api.common import get_measure_value,MeasureType
from urllib import parse

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
        credentials = auth.get_credentials(auth_code)
        api = WithingsApi(credentials)
        meas_result = api.measure_get_meas()
        return "he "+str(meas_result)
    return "credentials"
        


if __name__=="__main__":
    app.run()
