# Team-6 - Data Streaming

## Current agenda:

### Step 1

Pick and setup data source: 
DOE generator: http://apps1.eere.energy.gov/buildings/energyplus/
Pecan Street: https://dataport.pecanstreet.org
Preferrably, Raspberry Pi

Determine how to generate and extract data from data source

### Step 2

Pick which parts of the data to package into streaming information
Communicate JSON structure to other teams reliant on our data
Determine how we will authenticate (keys)

### Step 3

Pick application to use to stream the data, set up raspberry pi to act as server

### Step 4

Deploy application to read data from data generator (Pi sensors, DOE, etc.)
Format application data into JSON as specified in Step 2
Set up API endpoints for application
Stream data using application

### Step 5

Authentication
Filtering
Buffering, Networking concerns
