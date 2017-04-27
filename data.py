import pandas as pd
import numpy as np
import ast
import json
from decimal import *

audienceAssetDict = {}
currentCampaign = ""
numOfUniqueFebCampaigns = 0
plantConversions = 0
febCampaignDetected = False
totalCostOfVideoCampaigns = 0
totalViewsOfVideoCampaigns = 0

csv1 = pd.read_csv("./source1.csv")
csv2 = pd.read_csv("./source2.csv").drop_duplicates()

campaignTypeDict = dict(zip(list(csv2.campaign), list(csv2.object_type)))

def updateConversionsAndCost(actionStr,campaign):
    actions = ast.literal_eval(actionStr)
    conversionsOfTypeXorY = False
    for dic in actions:
        if dic["action"] == "conversions" and ("x" in dic or "y" in dic):
            conversionsOfTypeXorY = True
            if "x" in dic:
                audienceAssetDict[campaign[i+1:]]["conversions"] += dic["x"]
            if "y" in dic:
                audienceAssetDict[campaign[i+1:]]["conversions"] += dic["y"]
    if conversionsOfTypeXorY == True:
        audienceAssetDict[campaign[i+1:]]["spend"] += Decimal(row["spend"]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            # audienceAssetDict[campaign[i+1:]]["spend"] += row["spend"]
            # float(json.dumps(str(Decimal(row["spend"]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))))
    return None

def getAudienceAssetWithLeastExpensiveConversions():
    lowest = None
    k = None
    for key,value in audienceAssetDict.iteritems():
        if lowest == None:
            lowest = Decimal(value["spend"] / value["conversions"])
        if Decimal(value["spend"] / value["conversions"]) < lowest:
            lowest = Decimal(value["spend"] / value["conversions"])
            k = key
    return k

def getTotalCostPerVideoView():
    return Decimal(totalCostOfVideoCampaigns / totalViewsOfVideoCampaigns).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

# def getNumberOfUniqueCampaignsInFebruary(campaign,currentCampaign,numOfUniqueFebCampaigns):
#     if row["campaign"] != currentCampaign:
#         currentCampaign = row["campaign"]
#         febCampaignDetected = False
#
#     if febCampaignDetected == False:
#         date = row["date"]
#         mo = date[5:-3]
#         if mo == "02":
#             febCampaignDetected = True
#             numOfUniqueFebCampaigns += 1
#
# def getTotalNumberOfConversionsOnPlants(campaign,action,plantConversions):
#     if "plants" in campaign:
#         actions = ast.literal_eval(action)
#         for dic in actions:
#             if dic["action"] == "conversions" and ("x" in dic or "y" in dic):
#                 if "x" in dic:
#                     plantConversions += dic["x"]
#                 if "y" in dic:
#                     plantConversions += dic["y"]

for index,row in csv1.iterrows():

    # Get audience asset conversion and spend data
    for i,s in enumerate(row["campaign"]):
        if s == "_":
            if row["campaign"][i+1:] in audienceAssetDict:
                updateConversionsAndCost(row["actions"],row["campaign"])
            else:
                audienceAssetDict[row["campaign"][i+1:]] = {"spend": Decimal(0.0),"conversions": 0}
                updateConversionsAndCost(row["actions"],row["campaign"])
            break
        if row["campaign"] in campaignTypeDict and "video" == campaignTypeDict[row["campaign"]]:
            actions = ast.literal_eval(row["actions"])
            viewsOfTypeXorY = False
            for dic in actions:
                if dic["action"] == "views" and ("x" in dic or "y" in dic):
                    viewsOfTypeXorY = True
                    if "x" in dic:
                        totalViewsOfVideoCampaigns += dic["x"]
                    if "y" in dic:
                        totalViewsOfVideoCampaigns += dic["y"]
            if viewsOfTypeXorY == True:
                totalCostOfVideoCampaigns += Decimal(row["spend"]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    # getNumberOfUniqueCampaignsInFebruary(row["campaign"],currentCampaign,numOfUniqueFebCampaigns)
    # getTotalNumberOfConversionsOnPlants(row["campaign"],row["actions"],plantConversions)

    #Get number of unique February campaigns
    if row["campaign"] != currentCampaign:
        currentCampaign = row["campaign"]
        febCampaignDetected = False

    if febCampaignDetected == False:
        date = row["date"]
        mo = date[5:-3]
        if mo == "02":
            febCampaignDetected = True
            numOfUniqueFebCampaigns += 1

    #Get total number of conversions on plants
    if "plants" in row["campaign"]:
        actions = ast.literal_eval(row["actions"])
        for dic in actions:
            if dic["action"] == "conversions" and ("x" in dic or "y" in dic):
                if "x" in dic:
                    plantConversions += dic["x"]
                if "y" in dic:
                    plantConversions += dic["y"]

print numOfUniqueFebCampaigns
print plantConversions
print getAudienceAssetWithLeastExpensiveConversions()
print getTotalCostPerVideoView()
