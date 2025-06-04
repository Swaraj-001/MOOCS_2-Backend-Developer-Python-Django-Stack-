from django.shortcuts import render
from .forms import NewMonumentForm, AddMonumentImgForm, SearchForm

from .models import users_collection, monuments_collection, cities_collection, contributions_collection
import bson
from datetime import datetime, timedelta




def landing(request):
    # Fetch monuments sorted by 'popularity' descending if available, else by _id descending
    monuments_cursor = monuments_collection.find().sort("popularity", -1).limit(5)
    monuments = list(monuments_cursor)
    if not monuments:
        # fallback to first 5 monuments
        monuments = list(monuments_collection.find().limit(5))
    for m in monuments:
        m["id"] = str(m["_id"])
        # Ensure bannerImage and title fields exist for template
        if "bannerImage" not in m:
            m["bannerImage"] = m.get("images", ["/static/img/default_banner.jpg"])[0] if m.get("images") else "/static/img/default_banner.jpg"
        if "title" not in m:
            m["title"] = m.get("name", "Unknown Monument")
    return render(request, 'landing.html', {"monuments": monuments})




def search(request):
    form = SearchForm()
    monuments = []
    isResults = False
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            monuments = [monument for monument in monuments_collection.find({'$or': [{'city': search}, {'title': search}]})]
            for monument in monuments:
                monument['id'] = str(monument['_id'])

            isResults = True
            print(monuments)
    return render(request, 'search.html', {"monuments": monuments, "isResults": isResults, "form": form})



def city(request, id):
    monuments = [monument for monument in monuments_collection.find({"city": id})]

    for m in monuments:
        m["id"] = str(m["_id"])

    return render(request, 'cityLocations.html', {"monuments": monuments, "city": id})

def loadLocation(request, id):
    return render(request, "loadLocation.html", {"id": id})

def location(request, locId, userId):

    success = False
    error = False
    locationId = bson.ObjectId(locId)
    monument = monuments_collection.find_one({"_id": locationId})

    monumentImgsLen = len(monument['images'])

    if request.method == 'POST':
        form = AddMonumentImgForm(request.POST)
        objId = bson.ObjectId(userId)
        user = users_collection.find_one({'_id': objId})
        print(monument)
        if form.is_valid():
            image = form.cleaned_data['image']

            images = monument['images']
            images.append(image)

            monuments_collection.update_one({'_id': locationId}, {"$set": {"images": images}})

            date = datetime.now()
            date = str(date.strftime('%d-%m-%y'))

            contribution = {
                'monumentId': locId,
                'contributor': user['username'],
                'contributorId': userId,
                'title': monument['title'],
                'city': monument['city'],
                'address': monument['address'],
                'contribution': "New Image added!",
                "date": date
            }

            print(contribution)
            res = contributions_collection.insert_one(contribution)

            success = True

        else:
            error = True
    else:
        form = AddMonumentImgForm()
        success = False

    context = {'form': form, 'success': success, "error": error, "monument": monument, "locId": locId, "monumentImgsLen": monumentImgsLen}

    return render(request, 'location.html', context)
