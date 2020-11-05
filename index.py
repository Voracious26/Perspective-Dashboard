from flask import Flask, render_template
from collections import OrderedDict
from operator import getitem 
import json
import urllib.request
app = Flask(__name__)


@app.route('/')
def main():
    url_cases = "https://api.covid19api.com/summary"
    response_cases = urllib.request.urlopen(url_cases)
    data_cases = response_cases.read()
    values_cases = json.loads(data_cases)

    url_population = "https://restcountries.eu/rest/v2/"
    response_population = urllib.request.urlopen(url_population)
    data_population = response_population.read()
    values_population = json.loads(data_population)

    countryData = {}

    for i in values_population:
        if int(i["population"]) > 0:
            countryData[i["alpha2Code"]] = {}
            countryData[i["alpha2Code"]]["name"] = i["name"]
            countryData[i["alpha2Code"]]["population"] = int(i["population"])
    for i in values_cases["Countries"]:
        if i["CountryCode"] in countryData:
            countryData[i["CountryCode"]]["confirmed_cases"] = int(i["TotalConfirmed"])
  
    for key,value in countryData.items():
        if not "confirmed_cases" in value.keys():
            value["confirmed_cases"] = 0
        value["percent_cases_as_float"] = 100 * value["confirmed_cases"] / value['population']
        value["percent_cases"] = "{:0.2f}%".format(100 * value["confirmed_cases"] / value['population'])

    
    countryData = OrderedDict(sorted(countryData.items(), key = lambda x: getitem(x[1], 'percent_cases_as_float'), reverse=True)) 
    return render_template('home.html', countryData=countryData)
