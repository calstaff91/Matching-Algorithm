#This a matching algorithm using an adapted version the Levenshtein distance. It allows the weighting of deletions,
#insertions, and replacements to be altered, as opposed to just all adding a score of 1 to the Levenshtein distance.
#The algorithm has been used here to match business names from two datasets, using a lowercase, punctuation-removed 
#and space-removed version of the business name concatenated with a lowercase, space-removed version of the business' 
#postcode. Here deletions have been weighted lower in order to cater for differences in businesses name such as 'ltd'
# versus 'limited'.

#Import required modules
import pandas as pd
from fuzzywuzzy import fuzz
import os
import timeit
import csv
import string
import difflib
#-----------------------------------------------------------------------------

#Define the adapted version of the Levenshtein distance
def score_match(editops_list, scores_dict):
            """
            takes a score_list from the Levenshtein distance
            function and applies weighted scoring according
            to the scores specified in the scores_dict
            """
            total_score = 0
            for this_tuple in editops_list:
                        total_score += scores_dict[this_tuple[0]]
            return total_score
#Here you can define the scores you attribute to each alteration operation
scores_dict = {
            "replace": 1,
            "delete": 0.1,
            "insert": 10
}
#-----------------------------------------------------------------------------

#This is the basic Levenshtein distance function. The score_match function will read all the operations this function
#has done, using 'editops' and attribute the scores to them
def levenshtein(s, t):
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
 
        return v1[len(t)]
#-----------------------------------------------------------------------------

#Setup timers for reference when algorithm is running
start = timeit.default_timer()
time = 0
#-----------------------------------------------------------------------------

#Create blank list for appending matched entities to
matched_set=[]
#-----------------------------------------------------------------------------

#Import lists of business names from csv to a dataframe
os.chdir('Directory Name Here')
df1 = pd.read_csv("File Here.csv")
df2 = pd.read_csv("File Here.csv")
#-----------------------------------------------------------------------------

#Define a function to turn all characters in a string are lowercase
def normalise_strings(x):
    """
    takes a string and ensures that all
    characters are lowercase
    """
    if type(x) is str:
        x = x.lower()
    return x
#-----------------------------------------------------------------------------

#Creates lists to be matched from dataframes
df1.var1 = df1['Variable 1']
df2.var2 = df2['Variable 2'] 
df1.var1 = df1.var1.apply(normalise_strings)
df2.var2 = df2.var2.apply(normalise_strings)
#-----------------------------------------------------------------------------

#Creates variable which will work its way through the the first dataset and find the entry in the second 
#dataset which is most similar
k = 0
df1_live = df1.var1[k]

for k in range(0,len(df1.var1)-1):
    
    h = 0
    
    #Creates two variables, the score of the first will be compared to the score of the second and the highest
    #scoring variable retained to be compared to the entity next in the list
    i=0
    first_comparison = df2.var2[i]
    j=1
    second_comparison = df2.var2[j]
    df1_live = df1.var1[k]
    
    #Performs above comparison for entirety of second dataset
    for h in range(0,len(df2.var2)-1):
        
        #Creates scores for comparison: 1-Weighted Levenshtein Score/Length of String (Expressed as a %)
        name_ratio1 = round((1-score_match(Levenshtein.editops(TA_Live, first_comparison), scores_dict)/len('TA_Live'))*100,1)
        name_ratio2 = round((1-score_match(Levenshtein.editops(TA_Live, second_comparison), scores_dict)/len('TA_Live'))*100,1)

        #If the first string has higher score, retains this string for comparison to next entity down
        if name_ratio1>=name_ratio2:
            if i<j:
                j=j+1
                second_comparison = df2.var2[j]              
            else:
                i=i+1
                second_comparison = df2.var2[i]        
            if name_ratio1>=name_ratio2:              
                name_score = name_ratio1
            else:
                name_score = name_ratio2
        
        #If the second string has higher score, this becomes the string for comparison to next entity down
        else:
            if i<j:
                i=j+1
                first_comparison = df2.var2[j]
                second_comparison = df2.var2[i]
            else:
                j=i+1
                first_comparison = df2.var2[i]
                second_comparison = df2.var2[j]
            if name_ratio1>=name_ratio2:              
                name_score = name_ratio1
            else:
                name_score = name_ratio2
        
        #Goes to next entity in second dataset for comparison
        h+=1
    
    #Once all entities in second dataset are compared, moves to next entities in first dataset
    k+=1
    
    #Calculates time for each comparison
    stop = timeit.default_timer()
    time_run = stop - start
    time = round(time + time_run,2)
    start = stop
    
    #Prints counter for which number entity in first dataset has been matched, time it took, the entity
    #in the first dataset, the entity in the second dataset and their score
    print '%r, %r, TA: %r, FHRS: %r, Ratio: %r' %(k, time, TA_Live,first_comparison,name-score) 
    
    #Creates dictionary entry for match and appends to list
    match_dict = {"TA": TA_Live, 
             "FHRS": first_comparison, 
             "Ratio": name_score
             }
    matched_set.append(match)
#-----------------------------------------------------------------------------

#Once completed, turns into csv
pd.DataFrame(matched_set).to_csv(r"/Users/datascientist1/Documents/Analysis/Matching/London/London_Matched.csv",encoding="utf-8")
#-----------------------------------------------------------------------------

#Prints overall time for process
stop = timeit.default_timer()
print stop - start