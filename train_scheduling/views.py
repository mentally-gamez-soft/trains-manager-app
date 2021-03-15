import json
import requests
import datetime
from django.http import JsonResponse
from django.shortcuts import render


categories = {'IC': 'Intercity', 'SPR': 'Sprinter'}


def home(request):
    template = "train_scheduling/home-trains.html"
    api_call_url = ""

    lstations = []

    api_call_url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations?subscription-key=9501613007cd41398976a63b0a5bd925"

    response = requests.get(api_call_url).json()

    for r in response['payload']:
        lstations.append({'station': {'code': r['code'], 'name': r['namen']['lang']}})

    context = {'stations': lstations}

    return render(request, template, context)


def departures(request):
    # print(request.body)
    data = json.loads(request.body)
    station_code = data['station_code']

    api_call_url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/departures?subscription-key=9501613007cd41398976a63b0a5bd925&station={}"

    response = requests.get(api_call_url.format(station_code)).json()
    # print(response)

    l_departures = []

    for departure in response['payload']['departures']:
        tmp_depart = {}

        if 'plannedDateTime' in departure:
            #tmp_depart['date_departure'] = departure['plannedDateTime']
            # print(departure['plannedDateTime'])
            #print(datetime.datetime.strptime(departure['plannedDateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d-%b-%Y, %Hh%M'))
            tmp_depart['date_departure'] = datetime.datetime.strptime(departure['plannedDateTime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d-%b-%Y, %Hh%M')
        else:
            tmp_depart['date_departure'] = ''

        if 'direction' in departure:
            tmp_depart['direction'] = departure['direction']
        else:
            tmp_depart['direction'] = ''

        if 'plannedTrack' in departure:
            tmp_depart['platform_bench'] = departure['plannedTrack']
        else:
            tmp_depart['platform_bench'] = ''

        if 'trainCategory' in departure:
            tmp_depart['train_category'] = categories.get(departure['trainCategory'], departure['trainCategory'])
        else:
            tmp_depart['train_category'] = ''

        l_departures.append(tmp_depart)

    # l_departures.append({'date_departure': 'Today', 'direction': 'Amsterdam', 'platform_bench': '3B', 'train_category': 'IC'})
    return JsonResponse({'departures': l_departures})
