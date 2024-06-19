import pandas as pd
import pvlib
from pvlib import pvsystem, modelchain, temperature
from pvlib.location import Location
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Function to load and filter weather data
def load_weather_data(file_path, start_time, end_time):
    weather_data = pd.read_csv(file_path, parse_dates=[0])
    weather_data.columns = [
        'timestamp', 'coordinates', 'model', 'elevation', 'utc_offset',
        'temperature', 'wind_speed', 'ghi', 'dhi', 'dni'
    ]
    weather_data = weather_data.set_index('timestamp')
    weather_data = weather_data[start_time:end_time]
    return weather_data

# Load weather data and filter by desired time range
weather_file = 'HistoricalWeather.csv'
start_time = '2023-06-24 14:00:00'
end_time = '2023-06-25 14:00:00'
weather = load_weather_data(weather_file, start_time, end_time)

# Define module parameters for Panasonic VBHN325KA03
module_parameters = {
    'pdc0': 325,  # DC power at standard test conditions (W)
    'v_mp': 59.2,  # Maximum power voltage (V)
    'i_mp': 5.50,  # Maximum power current (A)
    'v_oc': 70.9,  # Open circuit voltage (V)
    'i_sc': 5.94,  # Short circuit current (A)
    'alpha_sc': 3.27e-3,  # Temperature coefficient of Isc (A/C)
    'beta_oc': -0.17,  # Temperature coefficient of Voc (V/C)
    'gamma_pdc': -0.00258  # Power temperature coefficient (1/C)
}

# Define inverter parameters (assuming total system power per module)
inverter_parameters = {
    'pdc0': 325  # DC input power rating (W) per module
}

# Temperature model parameters
temperature_model_parameters = temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# Define each segment
segments = [
    {'tilt': 32, 'azimuth': 90, 'modules': 3, 'pdc0': 0.975e3},
    {'tilt': 50, 'azimuth': 180, 'modules': 3, 'pdc0': 0.975e3},
    {'tilt': 32, 'azimuth': 90, 'modules': 6, 'pdc0': 1.95e3},
    {'tilt': 30, 'azimuth': 270, 'modules': 30, 'pdc0': 9.75e3}
]

# Define the location
latitude, longitude = 40.43093, -86.911617
site = Location(latitude, longitude)

# Function to model each segment
def model_segment(segment, weather, site):
    system = pvsystem.PVSystem(
        surface_tilt=segment['tilt'],
        surface_azimuth=segment['azimuth'],
        module_parameters=module_parameters,
        temperature_model_parameters=temperature_model_parameters,
        modules_per_string=1,
        strings_per_inverter=segment['modules'],
        inverter_parameters=inverter_parameters
    )

    # Create the model chain
    mc = modelchain.ModelChain(system, site, dc_model='pvwatts', ac_model='pvwatts', aoi_model='physical', spectral_model='no_loss')

    # Debug: print the PVSystem parameters
    print(f"Modeling segment with parameters: {segment}")

    # Run the model and print intermediate steps
    try:
        mc.run_model(weather)

        # Debug: Check intermediate results
        '''
        print("MC Results:", mc.results)
        print("DC Power:", mc.results.dc)
        print("AC Power:", mc.results.ac)
        '''
        # Check if model chain has run successfully
        if mc.results.ac is None:
            print(f"ModelChain did not produce 'ac' for segment: {segment}")
            return pd.Series(0, index=weather.index)  # return zero power if error

        # Return AC power
        return mc.results
    except Exception as e:
        print(f"Error modeling segment {segment}: {e}")
        return pd.Series(0, index=weather.index)  # return zero power if error


# Model each segment and sum their outputs
dc_power_total = sum(model_segment(segment, weather, site).dc for segment in segments)
ac_power_total = sum(model_segment(segment, weather, site).ac for segment in segments)
# Print the total DC power
print(f"Total DC Power: {dc_power_total}")

# Print the total AC power
print(f"Total AC Power: {ac_power_total}")

print(f"Weather Data: {weather}")
# Plot the results
ac_power_total.plot()
plt.xlabel('Time')
plt.ylabel('Total AC Power (W)')
plt.title('Total Solar PV Output')
plt.show()

# Plot the results
dc_power_total.plot()
plt.xlabel('Time')
plt.ylabel('Total DC Power (W)')
plt.title('Total Solar PV Output')
plt.show()

fig,ax1 = plt.subplots()

ax1.plot(weather['temperature'], label='Temperature', color = 'blue')
ax1.set_xlabel('Time (Hour of Day)')
ax1.set_ylabel('Temperature (Celsius)', color = 'blue')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

ax2 = ax1.twinx()
ax2.plot(weather['ghi'], label='GHI', color='red')
ax2.set_ylabel('Irradiance (w/m^2)', color = 'red')


plt.title('Global Irradiance and Temperature')
plt.show()
