from flask import Flask, render_template
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
        countryData[i["alpha2Code"]] = {}
        countryData[i["alpha2Code"]]["population"] = i["population"]
    for i in values_cases["Countries"]:
        if i["CountryCode"] in countryData:
            countryData[i["CountryCode"]
                        ]["confirmed_cases"] = i["TotalConfirmed"]

    return render_template('home.html', countryData=countryData)
