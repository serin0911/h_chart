# chart/views.py
from django.shortcuts import render
from .models import Passenger
from django.db.models import Count, Q
import json, arrow  # ***json 임포트 추가***


def home(request):
    return render(request, 'home.html')


def world_population(request):
    return render(request, 'world_population.html')


def ticket_class_view(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()             # for xAxis
    survived_series = list()        # for series named 'Survived'
    not_survived_series = list()    # for series named 'Not survived'
    survival_rate_series = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])    # for xAxis
        survived_series.append(entry['survived_count'])          # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'
        survival_rate_series.append(entry['survived_count']/(entry['survived_count']+entry['not_survived_count'])*100)

    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series),
        'survival_rate_series': json.dumps(survival_rate_series)
    })


def covid_cases(request):
    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]

    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df = df.pivot(index='Date', columns='Country', values='Cases')

    Germany_Series = df.Germany.tolist()
    US_Series = df.US.tolist()
    France_Series = df.France.tolist()
    Korea_Series = df['Korea, South'].tolist()
    UK_Series = df['United Kingdom'].tolist()

    date = df.index.tolist()
    datee = list()
    for i in date:
        datee.append(i.strftime('%Y-%m-%d'))

    return render(request, 'covid_cases.html', {
        'date': json.dumps(datee),
        'Germany_Series': json.dumps(Germany_Series),
        'US_Series': json.dumps(US_Series),
        'France_Series': json.dumps(France_Series),
        'Korea_Series': json.dumps(Korea_Series),
        'UK_Series': json.dumps(UK_Series)
    })


def covid_cases_per_capita(request):
    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]

    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df = df.pivot(index='Date', columns='Country', values='Cases')

    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = df.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    Germany_Series = percapita.Germany.tolist()
    US_Series = percapita.US.tolist()
    France_Series = percapita.France.tolist()
    Korea_Series = percapita['Korea, South'].tolist()
    UK_Series = percapita['United Kingdom'].tolist()

    date = percapita.index.tolist()
    datee = list()
    for i in date:
        datee.append(i.strftime('%Y-%m-%d'))

    return render(request, 'covid_cases_per_capita.html', {
        'date': json.dumps(datee),
        'Germany_Series': json.dumps(Germany_Series),
        'US_Series': json.dumps(US_Series),
        'France_Series': json.dumps(France_Series),
        'Korea_Series': json.dumps(Korea_Series),
        'UK_Series': json.dumps(UK_Series)
    })

