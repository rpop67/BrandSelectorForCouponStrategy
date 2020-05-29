from flask import Flask,request
import pip
from pip._internal import main as pipmain

pipmain(['install', 'pytrends'])
# from flask_cors import CORS
import hellyeah
app = Flask(__name__)
import trendAnalyser
# CORS(app)

@app.route('/timeBlock')
def get_current_time():
    return {'block':
        {
        'time': "hululu",
        'dataList':[70.0, 45.0, 34.0, 33.0, 46 ]
        }
    }

@app.route('/resultPost',methods=['POST'])
def result():
    recv_data=request.json
    print(recv_data)
    for item in recv_data:
        res=trendAnalyser.findTopSites(recv_data,3,"lala")
    
    return {
        'block':
        {
            'list':recv_data,
            'dataList':[100.0, 2.0, 84.0, 13.0, 60 ]
        }
    }
