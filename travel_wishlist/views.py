from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
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
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)  # if not found, will raise DoesNotExist error
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
