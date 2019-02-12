import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=7f02573b45cf92e716b5987d50aa812e'
    s='0'

    if request.method == 'POST':
        form = CityForm(request.POST)
        s=form.data['name']
        #form.save()
        if (City.objects.filter(name__iexact=s.upper()).count() )> 0:
           form=CityForm()
           #print(City.objects.all())
        else:
           form.save()
           #cities = City.objects.filter(name=form.data['name']).order_by('-id')
           #print(City.objects.all())
    form = CityForm()

    cities = City.objects.filter(name__iexact=s.upper())[:1]
    #print(City.objects.all())
    #print(City.objects.filter)
    
    
    
    
    weather_data = []
    c=chr(176)

    city_weather=None

    for city in cities:

        r = requests.get(url.format(city)).json()
        print(r)
        if r=={'cod':'404','message':'city not found',}:
        	city_weather={
        	    'city' : 'City Not Found',
        	   	'icon' :'#',
         	}
        else:
        	city_weather = {
            	'city' : city.name,
            	'temperature' : r['main']['temp'],
            	'description' : r['weather'][0]['description'],
            	'icon' : r['weather'][0]['icon'],
        	}

    weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form, 'c':c}
    return render(request, 'weather/weather.html', context)