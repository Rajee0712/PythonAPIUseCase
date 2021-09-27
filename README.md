# PythonAPIUseCase
Python API UseCase

The program consists of two files:
1. The main program - Supermetrics_API_Post_Stats.py
2. Parameter File used in the above program - API_Post_Stats_param.py

High Level Flow of the Program
1. The Post API is called to generate the SL Token 
2. The GET API uses the SL Token generated above as one of the input, page number as another input and retrieves the posts.
3. Program iterates through all the pages, few columns required for processing like the Month_Year and Week_No are added along and written into an intermediate file
4. Then Intermediate file is read and all the statistics are calculated.
