from flask import Flask
import json
import urllib.request
app = Flask(__name__)


@app.route('/')
def main():
    url_cases = "https://api.covid19api.com/summary"
    url_population = "https://restcountries.eu/rest/v2/"
    response_cases = urllib.request.urlopen(url_cases)
    response_population = urllib.request.urlopen(url_population)
    data_cases = response_cases.read()
    data_population = response_population.read()
    values_cases = json.loads(data_cases)
    values_population = json.loads(data_population)

    dict_cases = {}
    dict_population = {}

    for i in values_cases["Countries"]:
        dict_cases[i["CountryCode"]] = i["TotalConfirmed"]
    for i in values_population:
        dict_population[i["alpha2Code"]] = i["population"]

    out = "COVID-19 cases:<br />"
    out += str(dict_cases)
    out += "<br /><br />"
    out += "Populations:<br />"
    out += str(dict_population)

    return out
