
# coding: utf-8

# In[2]:


#Dependencies
import pandas as pd

#Read in data

data = pd.read_csv('resources/election_data.csv')
data.head()


# In[3]:


# * The total number of votes cast
total_votes = data["Voter ID"].nunique()
total_votes_str = "Total Votes: %s" %(total_votes)


# In[4]:


#  * A complete list of candidates who received votes
candidate_list = list(data['Candidate'].unique())
candidate_list


# In[31]:


#  * The percentage of votes each candidate won
vote_percent = list(data['Candidate'].value_counts(normalize=True))
vote_percent


# In[12]:


#* The total number of votes each candidate won
vote_count = list(data['Candidate'].value_counts())
data['Candidate'].value_counts()


# In[18]:


#  * The winner of the election based on popular vote.
winner_str = "Winner: %s" %(candidate_list[0])
winner_str


# In[34]:


#Results
Khan_str = "%s: %s (%s)" % (candidate_list[0], "{0:.0%}".format(vote_percent[0]), vote_count[0])
Correy_str = "%s: %s (%s)" % (candidate_list[1], "{0:.0%}".format(vote_percent[1]), vote_count[1])
Li_str = "%s: %s (%s)" % (candidate_list[2], "{0:.0%}".format(vote_percent[2]), vote_count[2])
Tooley_str = "%s: %s (%s)" % (candidate_list[3], "{0:.0%}".format(vote_percent[3]), vote_count[3])



# In[39]:


output = f"Election Results\n----------------------------\n{total_votes_str}     \n----------------------------\n{Khan_str}\n{Correy_str}\n{Li_str}\n{Tooley_str}     \n----------------------------\n{winner_str}     \n----------------------------"


print(output)


# In[40]:


#Export to text file
 
file1 = open("PyPoll.txt","w") 

file1.writelines(output)

file1.close() 

