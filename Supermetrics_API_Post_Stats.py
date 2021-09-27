'''
Program Name    : Supermetrics_API_Post_Stats.py
Program Desc    : Program to fetch and calculate the below statistics
                  in JSON format from fictional Supermetrics API
                    a. - Average character length of posts per month
                    b. - Longest post by character length per month
                    c. - Total posts split by week number
                    d. - Average number of posts per user per month
=========================================================================
Version     Created_date    Author      Contact_-info
1.0         25-Sep-2021     Rajee       raji.jkraj@gmail.com
=========================================================================
'''

import requests
import os
from datetime import datetime
import pandas
import json
from API_Post_Stats_param import *

# Function to get the SL token
def getSlToken():
    res = requests.post(url = slTokenUrl, data = postParams)
    tokenData = res.json()
    slTokenVal= tokenData['data']['sl_token']
    return slTokenVal

#Function to fetch Month & Year.
    #Input: Date in the format e.g. "2021-09-24T03:24:13+00:00"
    #Output: Returns value in the format e.g. "SEP-2021"
def monthYear(dt):
        dt = dt[0:dt.index("T")]
        date = datetime.strptime(dt, "%Y-%m-%d")
        findt = date.strftime("%b-%Y")
        return findt

#Function to fetch the week number.
    #Input: Date in the format e.g. "2021-09-24T03:24:13+00:00"
    #Output: Returns value ranging from 1-53 e.g. "34"
def weekNo(dt):
    dt = dt[0:dt.index("T")]
    date = datetime.strptime(dt, "%Y-%m-%d")
    finwk = int(date.strftime("%U"))
    return finwk

#Function to remove the file if exists
    #Input: Provide path of the file and filename
def remove_files(path_file_name):
    if os.path.exists(path_file_name):
        os.remove(path_file_name)

#Function to create the intermediate processing file and insert the header.
def createIntermediatePostFile():
    with open(intermediatePostFile, "w") as postFileObject:
        postFileObject.write("userid,name,created_time,message,lenofmsg,monyear,weeknum" + "\n")

#Iterate through all pages and write the post to an intermediate file to process it further
def postCollation(slToken):
    for i in range(1,pageNoLimit+1):
        #Form the input parameter to be passed for each page.
        getParams = {'sl_token':slToken,
                        'page':i
                    }
        #Hit get posts Url to get the posts data.
        postDetails= requests.get(url = postDetailUrl , params = getParams).json()
        postMsg=postDetails['data']['posts']

        #Iterate through the post message and form the data as required to be written to intermediate file.
        for j in postMsg:
            postText = j['from_id'] + "," + j['from_name'] + "," + j['created_time'] + "," + j['message'] + "," + str(len(j['message'])) + "," + monthYear(j['created_time']) + "," + str(weekNo(j['created_time'])) + "\n"

            #Append the posts data to the intermediate file created earlier with header.
            with open(intermediatePostFile, "a+") as postFileObject:
                postFileObject.write(str(postText))

#Function to read the intermediate Posts File and create a dataframe using pandas for further processing
def createPostsDF(InputCsvFile):
    postsDF = pandas.read_csv(InputCsvFile, sep= ',')
    return postsDF

#Function to convert the dataframe output to JSON.
def parseAsJson(InputDF):
    DFToJson = InputDF.to_json(orient="split")
    parsedJson = json.loads(DFToJson)
    del parsedJson['index']
    FinalJsonOuput = json.dumps(parsedJson, indent=4)
    print(FinalJsonOuput)
    return FinalJsonOuput

#scenario 1: Average character length of posts per month
def avgCharLenPostsPerMon(postsDF,inputParseJsonFunc):
    #Perform group by month and get the average of the length of message
    avgPostPerMonth = postsDF.groupby(['monyear'] ,as_index=False)['lenofmsg'].mean()
    #Rename column in a meaning ful format
    avgPostPerMonth.columns = ['Month_Year','Avg_Char_Len_Posts_Per_Month']
    #Call the parseAsJson to
    inputParseJsonFunc(avgPostPerMonth)

#Scenario b: Longest post by character length per month
def longestPostsPerMon(postsDF,inputParseJsonFunc):
    #Group by Month and get the longest post for that month
    longestPostPerMonth = postsDF.groupby(['monyear'], as_index=False)['lenofmsg'].max()
    # Rename column to a meaningful one
    longestPostPerMonth.columns = ['Month_Year', 'Length_of_Longest_Post']
    #Call the parseAsJson function & return the result
    inputParseJsonFunc(longestPostPerMonth)

#Function to calculate for scenario c: Total posts split by week number
def noOfPostsPerWeek(postsDF,inputParseJsonFunc):
    # Group by weeknum and get the count per week
    noOfPostByWeek = postsDF.groupby(['weeknum'], as_index=False)['message'].count()
    # Rename column to a meaningful one
    noOfPostByWeek.columns = ['Week_Number', 'No_of_Posts_Per_Week']
    # Call the parseAsJson function & return the result
    inputParseJsonFunc(noOfPostByWeek)

#Function to calculate for scenario d: Average number of posts per user per month
def noOfPostsPerUserPerMon(postsDF,inputParseJsonFunc):
    #Get the total count of messages per user across all months
    TotlPostPerMonth = postsDF.groupby(['userid'] ,as_index=False)['message'].count()
    #Get the total count of posts, per month per user.
    totpostperusermonth = postsDF.groupby(['monyear','userid'] ,as_index=False)['message'].count()

    #Perform a left join on both the above dataframes
    mergedf = pandas.merge(left=totpostperusermonth, right=TotlPostPerMonth, how='left', left_on='userid', right_on='userid')
    #Rename DF columns
    mergedf.columns = ['Month_Year', 'UserId', 'Tot_Posts_Per_User_Per_Mon', 'Tot_Posts_Per_Mon']
    # Average no. of posts/user/month is calculated as
    mergedf["Avg_Posts_Per_User_Per_Mon"] = mergedf['Tot_Posts_Per_User_Per_Mon'] / mergedf['Tot_Posts_Per_Mon']
    # Remove the intermediate column used for processing from dataframe
    del mergedf['Tot_Posts_Per_User_Per_Mon']
    del mergedf['Tot_Posts_Per_Mon']
    # Call the parseAsJson function & return the result
    inputParseJsonFunc(mergedf)

def main():
    #Call the function to remove the intermediate processing file if exists.
    remove_files(intermediatePostFile)

    #call the function to create the intermediate file with header
    createIntermediatePostFile()

    #Call the function to retrieve sltoken to be passed to the GET Posts URL.
    slTokenVal=getSlToken()

    #Call the function to collate all posts from the GET URL to the intermediate post file.
    postCollation(slTokenVal)

    #Call the function to read the intermediate posts file and return the dataframe with post values
    postsDFVal=createPostsDF(intermediatePostFile)

    #Call the function to get the ouput of scenario a: Average character length of posts per month
    avgCharLenPostsPerMon(postsDFVal,parseAsJson)

    #Call the function to get the ouput of scenario b: Longest post by character length per month
    longestPostsPerMon(postsDFVal,parseAsJson)

    #Call the function to get the ouput of scenario c: Total posts split by week number
    noOfPostsPerWeek(postsDFVal,parseAsJson)

    #Call the function to get the output of scenario d: Average number of posts per user per month
    noOfPostsPerUserPerMon(postsDFVal,parseAsJson)

if __name__ == "__main__":
        try:
            print("Start of the program to fetch the Posts Statsitics")
            main()
        except exceptions as e:
            print (e)