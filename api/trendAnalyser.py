from pytrends.request import TrendReq
import numpy as np
import itertools
import random
# import pandas as pd


def CouponSelection(listOfSites,n):
    #since n will always be 15 in this case
    length=len(listOfSites)
    middle=length//2+1
    list1=listOfSites[:middle]
    list2=listOfSites[middle:]
    topList1=list(findTopSites(list1,n-1,"null").keys())
    print(topList1)
    topList2=list(findTopSites(list2,n-1,"null").keys())
    print(topList2)
    finalList=topList1+topList2
    sitesForCoupons=findTopSites(finalList,n,"couponSelction.csv")
    return sitesForCoupons


def Normalize(list1,list2):
    firstHalf=list1
    secondHalf=list2
    len1=len(firstHalf)
    len2=len(secondHalf)
    pytrends1=TrendReq(retries=10,backoff_factor=0.5)
    pytrends1.build_payload(firstHalf,geo='GB',timeframe="today 12-m")
    df1=pytrends1.interest_over_time()
    averageList1 = []
    for item in firstHalf:
        averageList1.append(df1[item].mean().round(0))

    pytrends2 = TrendReq(retries=10, backoff_factor=0.5)
    pytrends2.build_payload(secondHalf, geo='GB', timeframe="today 12-m")
    df2 = pytrends2.interest_over_time()
    averageList2 = []
    for item in secondHalf:
        averageList2.append(df2[item].mean().round(0))

    #since common element is last element of first list
    #and first element of second list

        # normalizing second group using first as reference
    normalizationFactor = averageList1[len1-1] / averageList2[0]
    for i in range(len(averageList2)):
        normalisedVal = normalizationFactor * averageList2[i]
        averageList2[i] = normalisedVal.round(0)

    averageList2.pop(0)
    secondHalf.pop(0)

    finalKeywords=firstHalf+secondHalf
    finalList=averageList1+averageList2
    

    trendDict = dict(zip(finalKeywords, finalList))
    # print(trendDict)
    # sorting the Dict in descending order
    sortedDict = dict(sorted(trendDict.items(), key=lambda x: x[1], reverse=True))
    # print("printing final list : " ,sortedDict)
    return sortedDict


def findTopSites(listOfSites,n,fileName):
    length=len(listOfSites)
    kw_list1=listOfSites[:5]
    pytrends1 = TrendReq(retries=10, backoff_factor=0.5)
    pytrends1.build_payload(kw_list1, geo='GB', timeframe="today 12-m")
    df1 = pytrends1.interest_over_time()
    averageList1 = []
    for item in kw_list1:
        averageList1.append(df1[item].mean().round(0))

    dictHelper1={}
    for i in range(len(kw_list1)):
        dictHelper1[kw_list1[i]]=averageList1[i]
    # print("DICT 1: ",dictHelper1)
    # sortedDictHelper = dict(sorted(dictHelper.items(), key=lambda x: x[1], reverse=True))

    #Repeating same steps for Kw_list2
    kw_list2 = listOfSites[5:]
    pytrends2 = TrendReq(retries=10, backoff_factor=0.5)
    pytrends2.build_payload(kw_list2, geo='GB', timeframe="today 12-m")
    # pytrends.build_payload(kw_list,geo='UK',timeframe='today 1-y')
    df2 = pytrends2.interest_over_time()

    averageList2 = []
    for item in kw_list2:
        averageList2.append(df2[item].mean().round(0))

    dictHelper2 = {}
    for i in range(len(kw_list2)):
        dictHelper2[kw_list2[i]] = averageList2[i]
    # print("DICT 2 : ", dictHelper2)
    # //changes will be updated in dictHElper1
    dictHelper1.update(dictHelper2)
    # print("*****DictHelper: ",dictHelper1)

    sortedDictHelper = dict(sorted(dictHelper1.items(), key=lambda x: x[1], reverse=True))

    midIndex=int((len(kw_list1)+len(kw_list2))/2 )
    middleRangeElement=list(sortedDictHelper.keys())[midIndex]
    # print("Sorted Helper: ",sortedDictHelper," \n ","middle range item: ",middleRangeElement)
    list1=[]
    list2=[]
    for key in list(sortedDictHelper.keys())[0:midIndex+1]:
        list1.append(key)
    for key in list(sortedDictHelper.keys())[midIndex:]:
        list2.append(key)
 

    sortedDict=Normalize(list1,list2)
    resDict = dict(itertools.islice(sortedDict.items(), n))  
    return resDict
    print(resDict)
