from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden


@login_required()
def place_list(request):

    """ If this is a POST request, the user clicked the Add button
    in the form. Check if the new place is valid, if so, save a
    new Place to the database, and redirect to this same page.
    This creates a GET request to this same route.

    If not a POST route, or Place is not valid, display a page with
    a list of places and a form to add a new place.
    """

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # creating a form from data in the request
        place = form.save(commit=False)  # creating a model object from form
        place.user = request.user
        if form.is_valid():  # validation against db constraints
            place.save()  # saves place to db
            return redirect('place_list')  # reloads homepage, redirects to GET view with name place_list

    # If not a POST, or the form is not valid, render the page with the form to
    # add a new place, and list of places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to create html
    # render combines template with data in html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required()
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)  # if not found will return 404 error
        if place.user == request.user:  # check if user belongs to place being edited
            place.visited = True
            place.save()  # needed to reflect in the db
        else:
            return HttpResponseForbidden()

    # return redirect('places_visited')  # redirect to places visited
    return redirect('place_list')  # redirect to wishlist places, name of a path


@login_required()
def place_details(request, place_pk):

    place = get_object_or_404(Place, pk=place_pk)
    # return render(request, 'travel_wishlist/place_detail.html', {'place': place})

    # does this place belong to the current user
    if place.user != request.user:
        return HttpResponseForbidden()

    # is this a GET request, or a POST request (update Place object)?

    """
    'form' in django has two meanings:
      1. When you create a TripReview'form', that's a form sent to the template and used to render HTML and web page.
      2. When a POST request is made, it's a different 'form' object, which is never shown on the page. Instead, it's
      used to encapsulate data that's been sent as part of the web request.  It's data that was filled into a form.
      Same object either way, but used in two different ways.
    """
    # if POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():  # are all fields filled that are required and are they the correct data types?
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # temporary, refine later

        return redirect('place_details', place_pk=place_pk)  # by default, a redirect is a GET request

    else:
        # if GET request, show Place info and form
        # if place is visited, show form; if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required()
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


def about(request):
    author = 'Nick'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
