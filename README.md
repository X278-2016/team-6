# Team-6 - Data Streaming

## Current agenda:

### Step 2

Pick which parts of the data to package into streaming information - (temperature, humidty, dew point, coordinates) - doing this over the weekend once the server is set up<br />
Communicate JSON structure to other teams reliant on our data - email Freddie<br />
Determine how we will authenticate (keys) <br />

### Step 3<br />

Communicate server information<br />

### Step 4

Set up API endpoints for application <br />
Stream data using application <br />

### Step 5 (extra goals) <br />

Authentication <br />
Filtering <br />
Buffering, Networking concerns <br />
etc. <br />

### Current Status:
Have bash script to automatically generate data using EnergyPlus (with static parameters <br />
Have python script to parse output and convert output to JSON <br />
Waiting on other teams to determine what we should actually output <br />
Ready to start working on networking 

### Todo:
Find 2-3 more sources of input (different sites) - simple bash script modification <br />
Find important data to send out - filter our own JSON (it's too big)<br />
Send information to server (doing this weekend)<br />
