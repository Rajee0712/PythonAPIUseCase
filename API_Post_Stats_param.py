
'''
Param File      : API_Post_Stats_param.py
Used In         : Supermetrics_API_Post_Stats.py
=========================================================================
Version     Created_date    Author      Contact_-info
1.0         25-Sep-2021     Rajee       raji.jkraj@gmail.com
=========================================================================
'''


#Parameters
slTokenUrl= "https://api.supermetrics.com/assignment/register"
postDetailUrl="https://api.supermetrics.com/assignment/posts"
clientIdVal="ju16a6m81mhid5ue1z3v2g0uh"
emailVal="raji.jkraj@gmail.com"
nameVal="Rajee"
pageNoLimit=10
workingDirectoryPath="/Users/rajee/Documents/Python_API_Usecase"
postProcessFile="postData.csv"
intermediatePostFile=workingDirectoryPath+"/"+postProcessFile

#Param body for the POST URL
postParams = {'client_id':clientIdVal,
                'email':emailVal,
                'name':nameVal
             }