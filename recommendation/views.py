# recommendation/views.py

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import CustomerProfile
from .forms import SkinAssessmentForm
from .services import RecommendationService
from .models import SkinAssessment
from store.models import Product

@login_required
def dashboard(request):
    # Step 1: Dapatkan profil pelanggan
    customer, created = CustomerProfile.objects.get_or_create(user=request.user)
    categories = Product.objects.exclude(category__isnull=True).exclude(category__exact='').values_list('category', flat=True).distinct()


    # Step 2: Redirect jika tiada assessment
    if not customer.skin_assessments.exists():
        messages.info(request, "Please complete your skin assessment first.")
        return redirect('recommendation:take_assessment')

    # Step 3: Jana cadangan (cached atau baru)
    try:
        recs = RecommendationService().get_for_customer(customer)
    except Exception as e:
        messages.error(request, "Could not generate recommendations at this time.")
        recs = []

    # Step 4: Dapatkan parameter GET untuk filter/sort
    sort_score = request.GET.get('score_sort')
    category = request.GET.get('category')
    sort_price = request.GET.get('price_sort')

    # Step 5: Tapis kategori
    if category:
        recs = [r for r in recs if r["product"].category and r["product"].category.lower() == category.lower()]

    # Step 6: Susun ikut skor
    if sort_score == "asc":
        recs.sort(key=lambda r: r["combined_score"])
    elif sort_score == "desc":
        recs.sort(key=lambda r: -r["combined_score"])

    # Step 7: Susun ikut harga
    if sort_price == "asc":
        recs.sort(key=lambda r: r["product"].price)
    elif sort_price == "desc":
        recs.sort(key=lambda r: -r["product"].price)

    # Step 8: Hantar ke template
    context = {
        'recommendations': recs,
        'sort_score': sort_score,
        'sort_price': sort_price,
        'category': category,
        'categories': categories,
    }

    return render(request, 'recommendation/dashboard.html', context)


@login_required
def take_assessment(request):
    """
    Let the user fill out or re-fill the SkinAssessment form.
    On POST, save and redirect back to dashboard.
    """
    customer, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SkinAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.customer = customer 
            assessment.save()
            messages.success(request, "Skin assessment saved!")
            # Clear any previously cached recs so we regenerate
            from django.core.cache import cache
            cache.delete(f"makeup_recs_{customer.id}")
            return redirect('recommendation:dashboard')
        else:
            print(form.errors)
    else:
        # Prepopulate form if they already have an assessment
        if customer.skin_assessments.exists():
            latest = customer.skin_assessments.first()
            initial_data = {
                'skin_type': latest.skin_type,
                'undertone': latest.undertone,
                'concerns': latest.concerns.split(',') if latest.concerns else [],
                'hydration_level': latest.hydration_level,
                'oiliness_level': latest.oiliness_level,
                'sensitivity_level': latest.sensitivity_level,
                'acne_proneness': latest.acne_proneness,
                'aging_concerns': latest.aging_concerns,
                'finish_preference': latest.finish_preference,
                'texture_preference': latest.texture_preference,
            }
            form = SkinAssessmentForm(initial=initial_data)
        else:
            form = SkinAssessmentForm()

    return render(request, 'recommendation/assessment.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def api_recommendations(request):
    """
    Return JSON: [ {product_id, name, brand, price, combined_score, reason}, ... ]
    Accepts ?refresh=true to force a recompute (by deleting the cache key).
    """
    customer, created = CustomerProfile.objects.get_or_create(user=request.user)

    # If the caller passed ?refresh=true, clear the cache before fetching
    force_refresh = request.GET.get('refresh', 'false').lower() == 'true'
    if force_refresh:
        from django.core.cache import cache
        cache.delete(f"makeup_recs_{customer.id}")

    try:
        recs = RecommendationService().get_for_customer(customer)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Could not generate recommendations'}, status=500)

    # Build a JSON‐serializable list
    recs_data = []
    for rec in recs:
        prod = rec['product']
        recs_data.append({
            'product_id': prod.id,
            'name': prod.name,
            'brand': prod.brand,
            'price': float(prod.price),
            'combined_score': rec['combined_score'],
            'reason': rec['reason'],
        })

    return JsonResponse({'success': True, 'recommendations': recs_data})

@login_required
def skin_assessment(request):
    customer = CustomerProfile.objects.get(user=request.user)
    # Dapatkan rekod assessment user ini, atau cipta baru jika tiada
    assessment, created = SkinAssessment.objects.get_or_create(customer=customer)

    if request.method == "POST":
        form = SkinAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Skin assessment updated!")
            return redirect('recommendation:dashboard')
    else:
        # pre-fill dengan data sedia ada
        initial = {}
        if assessment.concerns:
            initial['concerns'] = assessment.concerns.split(',')
        form = SkinAssessmentForm(instance=assessment, initial=initial)

    return render(request, "recommendation/assessment.html", {"form": form})
