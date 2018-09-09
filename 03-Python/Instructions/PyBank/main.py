
# coding: utf-8

# In[37]:


#Dependencies
import pandas as pd


#Bringing in csv file
file = pd.read_csv('resources/budget_data.csv')


# In[45]:


#The total number of months included in the dataset
total_months = file['Date'].nunique()
total_months_str = "Total Months: %s" %(total_months)


# In[46]:


#The total net amount of "Profit/Losses" over the entire period
total = file['Profit/Losses'].sum()
total_str = "Total: %s" %('${:,.2f}'.format(total))


# In[47]:


#The average change in "Profit/Losses" between months over the entire period
file['Monthly Change'] = file['Profit/Losses'].diff()
avg_change = file['Monthly Change'].mean()
avg_change_str = "Average Change: %s" %('${:,.2f}'.format(avg_change))


# In[82]:


#The greatest increase in profits (date and amount) over the entire period
max_profit = file['Monthly Change'].max()
max_month = file.loc[file['Monthly Change'] == max_profit, 'Date' ].item()
max_profit_str = "Greatest Increase in Profits: %s (%s)" %(max_month, '${:,.2f}'.format(max_profit))
max_profit_str


# In[ ]:


#The greatest decrease in losses (date and amount) over the entire period


# In[83]:


min_profit = file['Monthly Change'].min()
min_month = file.loc[file['Monthly Change'] == min_profit, 'Date' ].item()
min_profit_str = "Greatest Decrease in Profits: %s (%s)" %(min_month, '${:,.2f}'.format(min_profit))
min_profit_str


# In[100]:

output = f"Financial Analysis\n----------------------------\n{total_months_str}\n{total_str}\n{avg_change_str}\n{max_profit_str}\n{min_profit_str}"


print(output)

#Export to text file
 
file1 = open("PyBank.txt","w") 

file1.writelines(output)

file1.close() 

