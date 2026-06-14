from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RouteRequestSerializer
from .services.route_service import RouteService
from fuel.optimizer import FuelOptimizer

# Create your views here.

class OptimizeRouteAPIView(APIView):
    def post(self, request):
        data = request.data 

        serializer = RouteRequestSerializer(data=data)

        if serializer.is_valid():
            start = serializer.validated_data["start"]
            destination = serializer.validated_data["destination"]

            # Get Route
            route_service = RouteService()
            route_data = route_service.get_route(start=start, destination=destination)

            # print(route_data, "Printing from routing views")

            # Fuel Optimizer
            optimizer = FuelOptimizer()
            fuel_data = optimizer.optimize(route_data=route_data)

            return Response(fuel_data)
        
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST 
            )
