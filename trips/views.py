from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Destination, TravelPlan
from .serializers import DestinationSerializer, TravelPlanSerializer
from .utils import get_lat_long, get_weather_forecast, generate_travel_plan
from ..travel_planner.settings import GOOGLE_API_KEY, WETHER_API_KEY

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

# class TravelPlanViewSet(viewsets.ViewSet):

#     @action(detail=False, methods=['post'])
#     def generate_plan(self, request):
#         destination_name = request.data.get('destination')
#         days = int(request.data.get('days'))
#         google_api_key = 'AIzaSyDpQAtscnjMjAZBEfYqCtKhpDvpUHYkhPU'     #自分のAPIキー
#         weather_api_key = '55051f34ce9141a55394b7f13ca0640a'    #自分のAPIキー
#         openai_key = 'YOUR_OPENAI_API_KEY'    #自分のAPIキー
        
#         lat, lon = get_lat_long(destination_name, google_api_key)
        
#         if lat and lon:
#             weather = get_weather_forecast(lat, lon, weather_api_key)
#             weather_summary = " ".join([f"{item['dt_txt']}: {item['weather'][0]['description']}" for item in weather['list'][:days]])
#             plan = generate_travel_plan(destination_name, weather_summary, days, openai_key)
            
#             destination = Destination.objects.create(name=destination_name, latitude=lat, longitude=lon)
#             travel_plan = TravelPlan.objects.create(destination=destination, days=days, weather_forecast=weather_summary, plan_details=plan)
            
#             serializer = TravelPlanSerializer(travel_plan)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Location not found'}, status=400)


        
class TravelPlanViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def generate_plan(self, request):
        destination_name = request.data.get('destination')
        days = int(request.data.get('days'))
        google_api_key = GOOGLE_API_KEY
        weather_api_key = WETHER_API_KEY
        
        lat, lon = get_lat_long(destination_name, google_api_key)
        
        if lat and lon:
            weather = get_weather_forecast(lat, lon, weather_api_key)
            weather_summary = " ".join([f"{item['dt_txt']}: {item['weather'][0]['description']}" for item in weather['list'][:days]])
            
            # GPT-2を使用して旅行プランを生成
            plan = generate_travel_plan(destination_name, weather_summary, days)
            
            destination = Destination.objects.create(name=destination_name, latitude=lat, longitude=lon)
            travel_plan = TravelPlan.objects.create(destination=destination, days=days, weather_forecast=weather_summary, plan_details=plan)
            
            serializer = TravelPlanSerializer(travel_plan)
            return Response(serializer.data)
        else:
            return Response({'error': 'Location not found'}, status=400)
