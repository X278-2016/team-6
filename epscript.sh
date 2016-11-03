#!/bin/bash
PREFIX=$(date +%Y-%m-%d-%k-%M-%S)
mkdir $PREFIX
energyplus -p $PREFIX -s D -d $PREFIX -w /Applications/EnergyPlus-8-6-0/WeatherData/USA_FL_Tampa.Intl.AP.722110_TMY3.epw -r CoolingTower.idf 
python to_json.py /Applications/EnergyPlus-8-6-0/$PREFIX/$PREFIX-table.htm
