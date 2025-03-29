from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Event, Review
from django.contrib import messages

def review_page(request):
    events = Event.objects.all()

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        review_text = request.POST.get('review_text')

        if event_id and review_text:
            event = Event.objects.get(id=event_id)
            Review.objects.create(event=event, text=review_text)
            messages.success(request, 'Review submitted successfully!')

        return redirect('review')  # Reload the same page after submission

    return render(request, 'Review.html', {'events': events})
