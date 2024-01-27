# pip install prophet

import pandas as pd 
from prophet import Prophet

# Load the data into a Pandas dataframe
df = pd.read_csv('2018-3-2023.csv')

# Set the 'Date' column as the index of the dataframe
df.set_index('Date', inplace=True)

# Convert the index to a DatetimeIndex
df.index = pd.to_datetime(df.index)
  
# Create a new dataframe for each weather variable we want to forecast
humidity_df = pd.DataFrame({'ds': df.index, 'y': df['Humidity (%)'].values})
dew_point_df = pd.DataFrame({'ds': df.index, 'y': df['Dew Point (°C)'].values})
wind_speed_df = pd.DataFrame({'ds': df.index, 'y': df['Wind Speed (km/h)'].values})
pressure_df = pd.DataFrame({'ds': df.index, 'y': df['Pressure (hPa)'].values})

# Instantiate a Prophet object for each weather variable
humidity_model = Prophet()
dew_point_model = Prophet()
wind_speed_model = Prophet()
pressure_model = Prophet()

# Create a new dataframe with the dates we want to make predictions for
future_dates = pd.date_range(start=df.index[-1], periods=30, freq='D')

# Fit the Prophet model to each dataframe
humidity_model.fit(humidity_df)
dew_point_model.fit(dew_point_df)
wind_speed_model.fit(wind_speed_df)
pressure_model.fit(pressure_df)

# Create a new dataframe with the 'ds' column for the future dates
humidity_future = pd.DataFrame({'ds': future_dates})
dew_point_future = pd.DataFrame({'ds': future_dates})
wind_speed_future = pd.DataFrame({'ds': future_dates})
pressure_future = pd.DataFrame({'ds': future_dates})

# Use the Prophet object to make predictions for the future dates

humidity_forecast = humidity_model.predict(humidity_future)
dew_point_forecast = dew_point_model.predict(dew_point_future)
wind_speed_forecast = wind_speed_model.predict(wind_speed_future)
pressure_forecast = pressure_model.predict(pressure_future)



humidity_forecast["yhat"]
newpd = pd.DataFrame({"Dew Point (°C)":dew_point_forecast["yhat"].values,"Humidity (%)":humidity_forecast["yhat"].values ,"Wind Speed (km/h)": wind_speed_forecast["yhat"].values,"Pressure (hPa)":pressure_forecast["yhat"].values})

newpd.to_csv("april.csv", index=False, header=True)