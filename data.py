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
leastExpensiveConversionRate = Decimal(0.0)

csv1 = pd.read_csv("./source1.csv")

def updateConversionsAndCost(arrStr,campaign):
    actions = ast.literal_eval(arrStr)
    for dic in actions:
        if dic["action"] == "conversions" and ("x" in dic or "y" in dic):
            if "x" in dic:
                audienceAssetDict[campaign[i+1:]]["conversions"] += dic["x"]
            if "y" in dic:
                audienceAssetDict[campaign[i+1:]]["conversions"] += dic["y"]
            audienceAssetDict[campaign[i+1:]]["spend"] += Decimal(row["spend"]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            # audienceAssetDict[campaign[i+1:]]["spend"] += row["spend"]
            # float(json.dumps(str(Decimal(row["spend"]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))))
    return

def getLeastAudienceAssetWithLeastExpensiveConversions():
    for key,value in audienceAssetDict.iteritems():
        print Decimal(value["spend"] / value["conversions"]).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

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

    # Get number of unique February campaigns
    if row["campaign"] != currentCampaign:
        currentCampaign = row["campaign"]
        febCampaignDetected = False

    if febCampaignDetected == False:
        date = row["date"]
        mo = date[5:-3]
        if mo == "02":
            febCampaignDetected = True
            numOfUniqueFebCampaigns += 1

    # Get total number of conversions on plants
    if "plants" in row["campaign"]:
        actions = ast.literal_eval(row["actions"])
        for dic in actions:
            if dic["action"] == "conversions" and ("x" in dic or "y" in dic):
                if "x" in dic:
                    plantConversions += dic["x"]
                if "y" in dic:
                    plantConversions += dic["y"]

getLeastAudienceAssetWithLeastExpensiveConversions()

print audienceAssetDict
print plantConversions
print numOfUniqueFebCampaigns
