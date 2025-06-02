from django.shortcuts import render, redirect 
from django.views import View
from django.http import JsonResponse
from store.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SkinAssessmentForm

def index(request):
    return render(request, 'recommendation/recommendation.html')

def skin_assessment(request):
    if request.method == 'POST':
        form = SkinAssessmentForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.customer = request.user.customer
            profile.save()
            return redirect('recommendation:recomhome')  # Redirect to recommendations page
    else:
        form = SkinAssessmentForm()
    
    return render(request, 'recommendation/skin_assessment.html', {'form': form})