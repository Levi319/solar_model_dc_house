# Solar PV Output Modeling with Python

**This code simulates the total DC and AC power output of a solar photovoltaic (PV) system for a specified period. It utilizes the pvlib library to perform the modeling calculations.**

## Features:

- **Models multiple solar panel segments with varying tilt, azimuth, and number of panels.**
- **Calculates both DC power (before inverter) and AC power (after inverter) output.**
- **Only use the DC Power output as input to DC Nanogrid system.**
- **Plots the total DC and AC power output over time.**
- **Includes a plot showing temperature and global horizontal irradiance (GHI) from weather data.**

## Requirements:

- **Python 3.x**
- **pandas library**
- **pvlib library**
- **matplotlib library**
- **matplotlib.dates library**

## Instructions:

1. **Install libraries:** Ensure you have the required libraries installed using pip:
    ```bash
    pip install pandas pvlib matplotlib matplotlib.dates
    ```

2. **Update configuration:**
   - **This code assumes a weather data file named `HistoricalWeather.csv` is in the same directory. If your file name is different, update the `weather_file` variable. The CSV file should have columns for timestamp, temperature, wind_speed, ghi, dhi, and dni.**
   - **Modify `start_time` and `end_time` variables to define the desired modeling period (format: `YYYY-MM-DD HH:MM:SS`).**
   - **You can modify `inverter_parameters` if want to include an inverter model that has different characteristics or replace an efficiency loss through the DC to DC converter.**
   - **The `segments` list defines each solar panel segment with its tilt, azimuth, number of panels, and total DC power rating. These are each of the solar array segments on the DC House.**

3. **Run the script:** Execute the Python script using your preferred method (e.g., command line, IDE).


## Outputs:

- **The script will print the total DC and AC power generated during the simulation period. Only use the DC Power output for the input into the DC Nanogrid system.**
- **It will also create three plots:**
  1. **Total AC Power vs. Time**
  2. **Total DC Power vs. Time**
  3. **Temperature and Global Horizontal Irradiance (GHI) vs. Time (formatted to show hour of day)**

## Further Customization:

**Explore the pvlib documentation ([https://readthedocs.org/projects/pvlib-python/](https://readthedocs.org/projects/pvlib-python/)) for more advanced modeling options like different DC and AC modeling approaches, spectral correction models, etc. You can modify the plotting section to customize plot styles and information displayed.**
