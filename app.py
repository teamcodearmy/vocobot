from flask import Flask,request,render_template,jsonify
import json
app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        data=request.data
        data=data.decode()
        data=json.loads(data)
        msg=data["msg"]
        return jsonify({"data":"ok...."})
if __name__=="__main__":
    app.run()
