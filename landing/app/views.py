from collections import Counter

from django.shortcuts import render_to_response
from django.http import HttpResponse


counter_show = Counter({'test': 0, 'original': 0})
counter_click = Counter({'test': 0, 'original': 0})


def index(request):
    from_landing = request.GET.get('from-landing')

    if from_landing == 'original':
        counter_click['original'] += 1
    elif from_landing == 'test':
        counter_click['test'] += 1

    return render_to_response('index.html')

def landing(request):
    ab_test_arg = request.GET.get('ab-test-arg')

    if ab_test_arg == 'original':
        counter_show['original'] += 1
        return render_to_response('landing.html')
    elif ab_test_arg == 'test':
        counter_show['test'] += 1
        return render_to_response('landing_alternate.html')
    else:
        return HttpResponse('Что-то пошло не так')

def stats(request):
    try:
        test = counter_click['test']/counter_show['test']
    except ZeroDivisionError:
        test = 0
    try:
        original = counter_click['original']/counter_show['original']
    except ZeroDivisionError:
        original = 0

    return render_to_response('stats.html', context={
        'test_conversion': round(test, 2),
        'original_conversion': round(original, 2),
    })
