from django.shortcuts import render
from django.views import View


class HomePage(View):
    def get(self, request):
        return render(request, 'home/index.html', {})

    def post(self, request):
        return render(request, 'home/index.html', {})
