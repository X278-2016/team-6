#!/bin/bash
PREFIX=$(date +%Y-%m-%d-%k-%M-%S)
mkdir Tampa_$PREFIX
mkdir SanFran_$PREFIX
mkdir Chiraq_$PREFIX
PWD=$(pwd)

./energyplus -p Tampa_$PREFIX -s D -d Tampa_$PREFIX -w /Applications/EnergyPlus-8-6-0/WeatherData/USA_FL_Tampa.Intl.AP.722110_TMY3.epw -r /Applications/EnergyPlus-8-6-0/ExampleFiles/CoolingTower.idf > /dev/null


./energyplus -p SanFran_$PREFIX -s D -d SanFran_$PREFIX -w /Applications/EnergyPlus-8-6-0/WeatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw -r /Applications/EnergyPlus-8-6-0/ExampleFiles/CoolingTower.idf > /dev/null


./energyplus -p Chiraq_$PREFIX -s D -d Chiraq_$PREFIX -w /Applications/EnergyPlus-8-6-0/WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw -r /Applications/EnergyPlus-8-6-0/ExampleFiles/CoolingTower.idf > /dev/null

python to_json.py $PWD/Tampa_$PREFIX/Tampa_$PREFIX-table.htm $PWD/SanFran_$PREFIX/SanFran_$PREFIX-table.htm $PWD/Chiraq_$PREFIX/Chiraq_$PREFIX-table.htm


rm -rf Chiraq_$PREFIX
rm -rf SanFran_$PREFIX
rm -rf Tampa_$PREFIX
