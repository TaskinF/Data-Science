import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""**Data Collection and preprocessing**"""

weather_data = pd.read_csv("2018-3-2023.csv")

# #checking the number of missing values
# weather_data.isnull().sum()

"""**Data Analysis**"""

#correlation between the various features
weather_data=weather_data.drop(['Precipitation (mm)'],axis=1)

# correlation= weather_data.corr()

# #constructing a heatmap to understand the correlation
# plt.figure(figsize = (16,9))
# sns.heatmap(correlation, cbar=True, square=True, 
#            fmt='.2f',annot=True, annot_kws={'size':8},
#             cmap='Oranges')

# #Correlation values of Temperature (°C)
# print(correlation['Temperature (°C)'])

# #Distribution of the Temperature (°

# sns.distplot(weather_data['Temperature (°C)'], color ='orange')

#Splitting the Features and Dependent Variable
X=weather_data.drop(['Temperature (°C)',"Date"],axis=1)
y=weather_data['Temperature (°C)']

# #Checking the features
# print(X)

# #Checking the Dependent Variable
# print(y)

"""**Splitting the dataset into the Training set and Test set**"""

from sklearn.model_selection import train_test_split
X_train, X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

# print(X_test)

# print(X_train)

"""**Feature Scaling**"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train.values)
X_test = sc.transform(X_test.values)

"""**Training the Random Forest Regression model on the whole dataset**"""

# from sklearn.model_selection import GridSearchCV
# parameters = {'n_estimators': [100,110,120,130,140,150,160,180,200]}
# grid_search = GridSearchCV(estimator = regressor,
#                            param_grid = parameters,
#                            cv = 10,
#                            n_jobs = -1)
# grid_search.fit(X_train, y_train)
# best_parameters = grid_search.best_params_
# print("Best Parameters:", best_parameters)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 200, random_state = 0)
regressor.fit(X_train, y_train)

"""**Predicting the Test set results**"""

y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)
y_pred=np.array(y_pred)
y_test=np.array(y_test)
# print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""**Evaluating The Model & R Squared**"""

from sklearn.metrics import r2_score
r2_error = r2_score(y_test, y_pred)
# print("R Squared error : ", r2_error)

"""**Applying k-Fold Cross Validation**"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = regressor , X = X_train, y = y_train, cv = 10)
# print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
# print("Standard Deviation: {:.2f} %".format(accuracies.std()*100))

"""# Compare the Actual Values and Predicted Values in a Plot"""

#Converting the y_test to list
y_test=list(y_test)

# #Actual Values in a Plot
# plt.plot(y_test, color='red', label='Actual Value')
# plt.title('Actual Weather')
# plt.xlabel('Day')
# plt.ylabel('Temperature (°C) Avg')
# plt.legend()
# plt.show()

# #Predicted Values in a Plot
# plt.plot(y_pred, color='blue' , label='Predicted Value')
# plt.title('Predicted Weather')
# plt.xlabel('Day')
# plt.ylabel('Temperature (°C) Avg')
# plt.legend()
# plt.show()

# #Actual Values vs Predicted Values in a Plot
# plt.plot(y_test, color='red', label='Actual Value')
# plt.plot(y_pred, color='blue' , label='Predicted Value')
# plt.title('Actual Weather vs Predicted Weather')
# plt.xlabel('Day')
# plt.ylabel('Temperature (°C) Avg')
# plt.legend()
# plt.show()

forecast_range = pd.read_csv("2023-january-march.csv")
forecast_range = forecast_range.drop( ['Temperature (°C)','Date','Precipitation (mm)'], axis=1)

forecasts = []

for index, row in forecast_range.iterrows():
    # input_data = (9.4,76.9,19.7,997.3)
    
    input_data = row
    
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    # standardize the input data
    std_data = sc.transform(input_data_reshaped)
    # print(std_data)

    prediction = regressor.predict(std_data)
    # print(prediction)
    forecasts.append(round(prediction[0], 2))

#Predicting future
april = pd.read_csv("april.csv")

for index, row in april.iterrows():
    # input_data = (9.4,76.9,19.7,997.3)
    
    input_data = row
    
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    # standardize the input data
    std_data = sc.transform(input_data_reshaped)
    # print(std_data)

    prediction = regressor.predict(std_data)
    # print(prediction)
    forecasts.append(round(prediction[0], 2))

months = { 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

month_names = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def print_forecast_by_month(forecasts, forecast_day, day, month, year):
  start_index = 0
  for i in range(1, month):
    
    start_index  += months[ i]
    
  start_index+=day-1

  print("*************************")
  print("|Forecasts for "+str(forecast_day)+" days :")
  for i in range(len(forecasts[start_index:start_index+forecast_day])):
        
        if day > months[month]:
            day = 1
            month+=1
        print("|  "+ str(year)+" " +month_names[month-1]+" "+str(day)+":",forecasts[start_index+ i], '°C')
        day+=1
  print("*************************")

print("*****************************************")
print("Welcome to the Weather Forecasting System For Gaziemir, Izmir")
print("*****************************************")
print("Please Press 0 for exit\n")

while True:
  
  date = input("Please Enter The Forecast Start Date (Year-Month-Day)(Example: 2023-1-1) : ")
  print()
  

  date = date.split("-")
  if len(date)!=3:
    try: 
       if int(date[0])==0:
         print("Thank You For Using Our System!!!\n")
         break
    except:
      print("Please enter the date in specified format!!!\n")
      continue
    print("Please enter the date in specified format!!!\n")
    continue

  year = int(date[0])
  if year!=2023:
    print("Please Enter Forecast Start Date As Only First 4 months of 2023 !!!\n")
    continue

  month = int(date[1])
  if month<0 or month>12:
    print("Please Enter Valid Month !!!\n")
    continue
  day = int(date[2])
  

  if day<0 or day>31:
    print("Please Enter Valid Day !!!\n")
    continue
  elif day==0:
    break
   
  while True:
    print("Please Enter 1 : For 3 Days Forecast \n")

    print("Please Enter 2 : For 7 Days Forecast \n")

    print("Please Enter 3 : For 14 Days Forecast \n")

    forecast_day =int( input("Please Select One Of The Forecast Ranges : "))
    print()

    if forecast_day == 1:
      forecast_day = 3
      break
    elif forecast_day == 2:
      forecast_day = 7
      break
    elif forecast_day == 3:
      forecast_day = 14
      break
    else:
      print("Please enter a valid choice!!!\n")
      continue

  print_forecast_by_month(forecasts,forecast_day, day, month, year)
  print()
  print("Please Press 0 for exit\n")
