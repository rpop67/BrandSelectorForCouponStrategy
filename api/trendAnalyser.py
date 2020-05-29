from pytrends.request import TrendReq
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd


def CouponSelection(listOfSites,n):
    #since n will always be 15 in this case
    length=len(listOfSites)
    middle=length//2+1
    list1=listOfSites[:middle]
    list2=listOfSites[middle:]
    topList1=findTopSites(list1,n-1,"null")
    print(topList1)
    topList2=findTopSites(list2,n-1,"null")
    print(topList2)
    finalList=topList1+topList2
    sitesForCoupons=findTopSites(finalList,n,"couponSelction.csv")
    return sitesForCoupons


def findTopSites(listOfSites,n,fileName):
    length=len(listOfSites)
    kw_list1=listOfSites[:5]
    # print(kw_list1)
    # kw_list1 = ['ASOS', 'Amazon', 'eBay', 'Tesco', 'Argos']
    pytrends1 = TrendReq(retries=10, backoff_factor=0.5)
    kw_list2=listOfSites[5:]
    # print(kw_list2)
    rand=random.randint(0,4)
    kw_list2.insert(0,kw_list1[rand])
    print(kw_list1,kw_list2)

    # kw_list2 = ['ASOS', 'Currys', 'Forever 21', 'John Lewis', 'Marks and Spencer']
    pytrends2 = TrendReq(retries=10, backoff_factor=0.5)
    pytrends1.build_payload(kw_list1, geo='GB', timeframe="today 12-m")
    pytrends2.build_payload(kw_list2, geo='GB', timeframe="today 12-m")

    # pytrends.build_payload(kw_list,geo='UK',timeframe='today 1-y')
    df1 = pytrends1.interest_over_time()
    df2 = pytrends2.interest_over_time()
    # print(df1,"\n",df2)

    averageList1 = []
    averageList2 = []
    for item in kw_list1:
        averageList1.append(df1[item].mean().round(0))

    for item in kw_list2:
        averageList2.append(df2[item].mean().round(0))
    # print(averageList1, averageList2)

    # normalizing second group using first as reference
    normalizationFactor = averageList1[rand] / averageList2[0]
    for i in range(len(averageList2)):
        normalisedVal = normalizationFactor * averageList2[i]
        averageList2[i] = normalisedVal.round(0)
    # print(averageList1, averageList2)

    # since the repeating eCommerce keyword is at index 0 in both lists hence we can omit it from second list

    averageList2.pop(0)
    kw_list2.pop(0)

    finalList = averageList1 + averageList2

    # finalList=list(set(averageList1+averageList2))
    finalKeywords = kw_list1 + kw_list2
    # print(finalList)
    # print(finalKeywords)

    y_pos = np.arange(len(finalKeywords))

    # plt.barh(y_pos,finalList,align='center',alpha=0.5)
    # plt.yticks(y_pos,finalKeywords)
    # plt.xlabel('Average popularity')
    # # plt.show()


# for dicts

    trendDict = dict(zip(finalKeywords, finalList))
    # print(trendDict)
    # sorting the Dict in descending order
    sortedDict = dict(sorted(trendDict.items(), key=lambda x: x[1], reverse=True))
    print(f'${fileName}')
    print(sortedDict)


    # DF=pd.DataFrame(sortedDict)
    # DF.to_csv(f'${fileName}')



    # in python3 dict.values returns a view of dictionary's value hence needs to be converted to list
    # print(list(sortedDict.values()),list(sortedDict.keys()))
    sortedVals = list(sortedDict.values())
    sortedKeys = list(sortedDict.keys())
    plt.barh(y_pos, sortedVals, align='center', alpha=0.5)
    plt.yticks(y_pos, sortedKeys)
    plt.xlabel('average popularity')
    # plt.show()

    # to get top 5 eCommerce sites:

    topECommerce = []
    # print(list(sortedDict))
    for site in list(sortedDict)[0:n]:
        topECommerce.append(site)
    return topECommerce

topN=3
eCommerceSites=['ASOS', 'Amazon', 'eBay', 'Argos','Currys', 'Forever 21', 'John Lewis', 'Marks and Spencer']
topECommerceSites=findTopSites(eCommerceSites,topN,'eCommerce.csv')
foodDeliverySites=['Deliveroo','Just Eat','UberEats','One Delivery','Foodhub','SUPPER','Macro Meals','HelloFresh','Prep Perfect']
topFoodDeliverySites=findTopSites(foodDeliverySites,topN,'foodSites.csv')
groceryDeliverySites=['Morrisons','Amazon Fresh','ocado','British Corner Shop', 'Tesco','riverford organic farmers','Planet Organic']
topGroceryDeliverySites=findTopSites(groceryDeliverySites,topN,'grocerySites.csv')
streamingSites=['Disney+','Netflix','Amazon Prime','mubi','now tv','talk talk','sky store','roku','BT']
topStreamingSites=findTopSites(streamingSites,topN,'streamingSites.csv')
eLearningSites=['learndirect','Day One','udemy','titus learning','Udacity','Virtual College','Brightwave','Kallidus','looop']
topELearningSites=findTopSites(eLearningSites,topN,'learningSites.csv')
# print(topECommerceSites)
# print(topFoodDeliverySites)
# print(topGroceryDeliverySites)
# print(topStreamingSites)
# print(topELearningSites)
combinedList=topGroceryDeliverySites+topFoodDeliverySites+topECommerceSites+topStreamingSites+topELearningSites
SitesForCoupons=CouponSelection(combinedList,5)
print("*************Sites for coupons*********")
print(SitesForCoupons)

