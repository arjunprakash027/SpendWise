#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[6]:


get_ipython().system('pip install emoji')


# In[9]:


import pandas as pd
import emoji

# Load the Excel file
file_path = r"C:\Users\sushm\OneDrive\Desktop\expense.xlsx"


data = pd.read_excel(file_path)

# Function to remove emojis from a string
def remove_emoji(string):
    return emoji.replace_emoji(string, replace='')

# 1. Remove all emojis from the Category column
data['Category'] = data['Category'].apply(remove_emoji)

# 2. Remove the Subcategory column
data = data.drop(columns=['Subcategory'])

# 3. Remove the Description column
data = data.drop(columns=['Description'])

# 4. Remove the Currency column
data = data.drop(columns=['Currency'])

# Display the cleaned dataframe
data.head(30)


# In[10]:


data = data.drop(columns=['Account'])


# In[12]:


data.head(50)


# In[13]:


total_income = data[data['Income/Expense'] == 'Income']['Amount'].sum()
total_expense = data[data['Income/Expense'] == 'Expense']['Amount'].sum()


# In[16]:


summary_df = pd.DataFrame({
    'Category': ['Income', 'Expense'],
    'Amount': [total_income, total_expense]
})


# Expense vs Income

# In[18]:


import matplotlib.pyplot as plt


# In[20]:


plt.figure(figsize=(8, 6))
plt.bar(summary_df['Category'], summary_df['Amount'], color=['green', 'red'])
plt.xlabel('Category')
plt.ylabel('Amount (INR)')
plt.title('Total Income vs Total Expense')
plt.grid(True)
plt.show()


# Distribution of expense

# In[21]:


category_amount = data.groupby('Category')['Amount'].sum().reset_index()


# In[22]:


plt.figure(figsize=(10, 8))
plt.pie(category_amount['Amount'], labels=category_amount['Category'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Expense Distribution by Category')
plt.show()


# In[23]:


data['Date'] = pd.to_datetime(data['Date'])


# Daily expense

# In[24]:


data.set_index('Date', inplace=True)


# In[25]:


frequency = 'M'


# In[26]:


expenses_over_time = data.resample(frequency)['Amount'].sum()


# In[28]:


plt.figure(figsize=(12, 6))
data['Amount'].resample('D').sum().plot(marker='o', linestyle='-', label='Daily')
plt.xlabel('Date')
plt.ylabel('Total Expenses (INR)')
plt.title('Daily Trend of Expenses')
plt.grid(True)
plt.legend()
plt.show()


# Weekly expense

# In[29]:


plt.figure(figsize=(12, 6))
data['Amount'].resample('W').sum().plot(marker='o', linestyle='-', label='Weekly', color='orange')
plt.xlabel('Date')
plt.ylabel('Total Expenses (INR)')
plt.title('Weekly Trend of Expenses')
plt.grid(True)
plt.legend()
plt.show()


# Daily average

# In[30]:


daily_average = data['Amount'].resample('D').sum().mean()


# In[32]:


print(f"Average Amount Spent per Day: {daily_average:.2f} INR")
plt.figure(figsize=(10, 6))
plt.bar('Average Amount Spent per Day', daily_average, color='skyblue')
plt.ylabel('Amount (INR)')
plt.title('Average Amount Spent per Day')
plt.grid(True)
plt.show()


# weekly average

# In[33]:


weekly_average = data['Amount'].resample('W').sum().mean()


# In[35]:


print(f"Average Amount Spent per Week: {weekly_average:.2f} INR")
plt.figure(figsize=(10, 6))
data['Amount'].resample('W').sum().plot(marker='o', linestyle='-', label='Weekly', color='orange')
plt.xlabel('Date')
plt.ylabel('Total Expenses (INR)')
plt.title('Weekly Trend of Expenses')
plt.grid(True)
plt.legend()
plt.show()


# In[36]:


data['Note'].fillna('Unknown', inplace=True)


# In[38]:


note_counts = data['Note'].value_counts()


# In[40]:


plt.figure(figsize=(12, 6))
data['Note'].value_counts().plot(kind='bar', color='skyblue')
plt.xlabel('Note')
plt.ylabel('Frequency')
plt.title('Distribution of Note Column')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# In[44]:


others_data = data[data['Category'] == 'Other']


# In[46]:


if not others_data.empty:
    # Calculate total expense for 'Others' category
    total_expense = others_data['Amount'].sum()
    print(f"Total Expense for Category 'Others': {total_expense:.2f} INR")
    
    # Plotting the 'Note' column for entries categorized as 'Others'
    plt.figure(figsize=(12, 6))
    others_data['Note'].value_counts().plot(kind='bar', color='skyblue')
    plt.xlabel('Note')
    plt.ylabel('Frequency')
    plt.title('Distribution of Note for Category "Others"')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
else:
    print("No data found for Category 'Others'.")


# highest and lowest category

# In[48]:


category_expenses = data.groupby('Category')['Amount'].sum()


# In[49]:


lowest_expense_category = category_expenses.idxmin()
lowest_expense_amount = category_expenses.min()


# In[50]:


highest_expense_category = category_expenses.idxmax()
highest_expense_amount = category_expenses.max()


# In[51]:


print(f"Category with Lowest Expense: {lowest_expense_category} ({lowest_expense_amount:.2f} INR)")
print(f"Category with Highest Expense: {highest_expense_category} ({highest_expense_amount:.2f} INR)")


# In[52]:


plt.figure(figsize=(12, 6))


# In[53]:


category_expenses.plot(kind='bar', color='skyblue')


# In[54]:


plt.bar(lowest_expense_category, lowest_expense_amount, color='red', label=f'Lowest: {lowest_expense_amount:.2f} INR')


# In[55]:


plt.bar(highest_expense_category, highest_expense_amount, color='green', label=f'Highest: {highest_expense_amount:.2f} INR')

plt.xlabel('Category')
plt.ylabel('Total Expense (INR)')
plt.title('Total Expenses by Category')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()


# accounts

# In[56]:


plt.figure(figsize=(10, 6))
data['Accounts'].value_counts().plot(kind='bar', color='skyblue')
plt.xlabel('Account Type')
plt.ylabel('Count')
plt.title('Distribution of Accounts')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()


# In[57]:


plt.figure(figsize=(10, 6))
plt.hist(data['Accounts'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Account Number')
plt.ylabel('Frequency')
plt.title('Distribution of Account Numbers')
plt.grid(True)
plt.tight_layout()

plt.show()


# In[59]:


get_ipython().system('pip install wordcloud')



# In[60]:


from wordcloud import WordCloud


# In[61]:


data = pd.DataFrame({
    'Date': ['23/06/2024', '21/06/2024', '21/06/2024', '19/06/2024', '19/06/2024', 
             '18/06/2024', '17/06/2024', '16/06/2024', '16/06/2024', '16/06/2024'],
    'Category': ['Food', 'Food', 'Food', 'Other', 'Food', 'Food', 'Culture', 'Other', 'Transport', 'Social Life'],
    'Note': ['Juice', 'Tidel canteen', 'Reliance smart', 'Mobile cover', 'Momo truck', 
             'Tidel canteen - coffee', 'Meditations', 'Printouts', 'Car petrol', 'Kenny Sebastian'],
    'INR': [90, 15, 100, 1000, 159, 69, 130, 30, 200, 1700],
    'Income/Expense': ['Expense', 'Expense', 'Expense', 'Expense', 'Expense', 
                       'Expense', 'Expense', 'Expense', 'Expense', 'Expense'],
    'Amount': [90, 15, 100, 1000, 159, 69, 130, 30, 200, 1700],
    'Accounts': [0.86, 0.14, 0.95, 9.54, 1.52, 0.66, 1.24, 0.29, 1.91, 16.21]
})


# In[62]:


data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')


# In[63]:


print("Summary Statistics:")
print(data.describe())


# In[64]:


plt.figure(figsize=(12, 6))
category_expenses = data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
category_expenses.plot(kind='bar', color='skyblue')
plt.xlabel('Category')
plt.ylabel('Total Expense (INR)')
plt.title('Total Expenses by Category')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# In[65]:


note_text = ' '.join(data['Note'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(note_text)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Notes')
plt.show()


# In[66]:


plt.figure(figsize=(12, 6))
daily_expenses = data.groupby(data['Date'].dt.date)['Amount'].sum()
daily_expenses.plot(marker='o', color='blue', linestyle='-', linewidth=2, markersize=8)
plt.xlabel('Date')
plt.ylabel('Daily Expense (INR)')
plt.title('Daily Expenses Trend')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[70]:


import seaborn as sns


# In[71]:


plt.figure(figsize=(10, 6))
sns.boxplot(x='Category', y='Amount', data=data, palette='viridis')
plt.title('Box Plot of Expenses by Category')
plt.xlabel('Category')
plt.ylabel('Expense (INR)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# In[72]:


cumulative_expenses = data.sort_values('Date').groupby(data['Date'].dt.date)['Amount'].cumsum()

# Plotting cumulative expenses over time
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], cumulative_expenses, marker='o', color='purple', linestyle='-', linewidth=2, markersize=6)
plt.title('Cumulative Expenses Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Expense (INR)')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:




