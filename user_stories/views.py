from django.shortcuts import render
from django.views import View

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'user_stories/main.html')

class RoomNewView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass


class RoomModifyView(View):
    def get(self, request):
        pass
    def post(self, request):
        pass


class RoomDeleteView(View):
    def get(self, request):
        pass


class RoomView(View):
    def get(self, request):
        pass