import re
from flask import Flask,request,render_template,jsonify
import json
app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        data=request.data
        data=data.decode()
        data=json.loads(data)
        msgs=data["msg"]
        print(msgs)
        data=[]
        # msg="""[3/10, 3:11 PM] Manpreet: Transaction of Rs 120.01 has been made on Kotak credit card xx7064 on 27-Dec at KFC. Available credit limit is 57522.59."""
        for msg in msgs:
            responsedic={}
            macthobj=re.search(r"[rR][sS]\.?\s[,\d]+\.?\d{0,2}|[iI][nN][rR]\.?\s*[,\d]+\.?\d{0,2}",msg,re.M|re.I)
            macthobj2=re.search(r"[0-9]*[Xx\*]*[0-9]*[Xx\*]+[0-9]{3,}",msg,re.M|re.I)
            macthobj3=re.search(r"(?i)(?:\sat\s|in\*)([A-Za-z0-9]*\s?-?\s?[A-Za-z0-9]*\s?-?\.?)",msg,re.M|re.I)
            if macthobj!=None:
                Amount=macthobj.group(0)
            else:
                Amount="Not Found..!"
            if macthobj2!=None:
                Account_no=macthobj2.group(0)
            else:
                Account_no="Not Found..!"
            if macthobj3!=None:
                Merchant_name=macthobj3.group(0)
            else:
                Merchant_name="Not Found..!"
                responsedic["Transaction Amount"]=Amount
                responsedic["Account No"]=Account_no
                responsedic["Merchant Name"]=Merchant_name
                data.append(responsedic)
                responsedic={}
        return jsonify({"data":data})
    return "ok"
if __name__=="__main__":
    app.run()
