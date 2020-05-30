from flask import Flask,request
import pip
from pip._internal import main as pipmain

pipmain(['install', 'pytrends'])
# from flask_cors import CORS
import hellyeah
app = Flask(__name__)
from trendAnalyser import findTopSites,CouponSelection
# CORS(app)

eCommerceSites=['ASOS', 'Amazon', 'eBay', 'Argos','Currys', 'Forever 21', 'John Lewis', 'Marks and Spencer']
foodDeliverySites=['Deliveroo','Just Eat','UberEats','One Delivery','Foodhub','SUPPER','Macro Meals','HelloFresh','Prep Perfect']
groceryDeliverySites=['Morrisons','Amazon Fresh','ocado','British Corner Shop', 'Tesco','riverford organic farmers','Planet Organic']
streamingSites=['Disney+','Netflix','Amazon Prime','mubi','now tv','talk talk','sky store','roku','BT']
eLearningSites=['learndirect','udemy','titus learning','Udacity','Virtual College','Brightwave','Kallidus','looop']

dict_map={"Ecommerce sites":eCommerceSites,"Streaming sites":streamingSites,"Food Delivery sites":foodDeliverySites,"Grocery Delivery sites":groceryDeliverySites,"E-Learning sites":eLearningSites}

@app.route('/timeBlock')
def get_current_time():
    return {'block':
        {
        'time': "Brand Analyser for UK Base",
        'dataList':[10.0, 10.0, 10.0, 10.0, 10.0 ],
        'labelList':["","","","","",""]
        }
    }

@app.route('/resultPost',methods=['POST'])
def result():
    
    recv_data=request.json
    print("RECV data: ",recv_data)
    domains=len(recv_data)
    
    if domains==0:
        print("OOPs no arguments received")
    elif domains==1:
        res=findTopSites(dict_map[recv_data[0]],5,"lala")
    elif domains==2 or domains==3: 
        newList=[]
        for lists in recv_data:
            resDict=findTopSites(dict_map[lists],3,"la")
            newList=newList+list(resDict.keys())
        res=findTopSites(newList,5,"lala")
    else:
        newList=[]
        for lists in recv_data:
            resDict=findTopSites(dict_map[lists],3,"la")
            newList=newList+list(resDict.keys())
        res=CouponSelection(newList,5)
    print(list(res.keys()),list(res.values()))

    resValue=list(res.values())
    maxVal=resValue[0]
    for i in range(len(resValue)):
        resValue[i]=round(resValue[i]/maxVal*100)
        

    
    return {
        'block':
        {
            'list':recv_data,
            'labelList':list(res.keys()),
            'dataList':resValue
        }
    }
