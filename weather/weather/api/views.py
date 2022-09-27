from json import JSONDecodeError
from statistics import mean, median as median_calc

import requests
from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from weather.api.serializers import ForecastSerializer


class ForecastViewSet(viewsets.GenericViewSet):
    """
    API endpoint that gets data from weather_api and returns minimum, average, maximum and min temperature
    """
    serializer_class = ForecastSerializer
    @action(methods=['GET'],
            detail=False,
            url_path=r'location/(?P<city>\w+)'
            )
    def location(self, request, **kwargs):
        # Validate city parameter
        city = kwargs.get("city")
        if not city.isalpha():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data="City parameter must be a string")

        # Validate days parameter
        days = request.GET.get('days')
        if not days:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data="Please provide number of days in your url parameters")
        try:
            days = int(days)
        except NameError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data="Days parameter must be an int")

        if 0 < days > 15:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data="Days must be greater than 0 and less than 15")

        # Construct url
        url = f"https://api.weatherapi.com/v1/forecast.json?key={settings.WEATHER_API_KEY}&q={city}&aqi=no&days={days}"
        # fetch weather data
        response = requests.get(url)
        if response.status_code == 200:
            try:
                response_data = response.json()
            except JSONDecodeError:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="Error retrieving weather data")
            try:
                forecast_days = response_data['forecast']['forecastday']
            except KeyError:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="Error retrieving weather data")
            # Process data
            maximum, minimum, average, median = self.process_weather_data(forecast_days)
            serializer_data = {'maximum':maximum, 'minimum':minimum, 'average':average, 'median':median}
            serializer = ForecastSerializer(data=serializer_data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=response.text)

    def process_weather_data(self, forecast_days):
        """
        Calculate the maximum, minimum, average and median temperature for given forecast_days

        :param forecast_days - weather api response
        """
        # Retrieve all maximum temperatures for the days
        combined_maximum_temp = []
        for forecast_day in forecast_days:
            try:
                combined_maximum_temp.append(forecast_day['day']['maxtemp_c'])
            except KeyError:
                continue

        # Retrieve all minimum temperatures for the days
        combined_minimum_temp = []
        for forecast_day in forecast_days:
            try:
                combined_minimum_temp.append(forecast_day['day']['mintemp_c'])
            except KeyError:
                continue

        # Retrieve all average temperatures for the days
        combined_average_temp = []
        for forecast_day in forecast_days:
            try:
                combined_average_temp.append(forecast_day['day']['avgtemp_c'])
            except KeyError:
                continue

        # Get mean value for each
        mean_maximum_temp = mean(combined_maximum_temp)
        mean_minimum_temp = mean(combined_minimum_temp)
        mean_average_temp = mean(combined_average_temp)

        # median temperature = mean value of maximum and minimum tempreratures
        median_temp = median_calc([mean_maximum_temp, mean_minimum_temp])

        return mean_maximum_temp, mean_maximum_temp , mean_average_temp , median_temp


