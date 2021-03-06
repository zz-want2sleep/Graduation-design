from django.shortcuts import render


def p1(request):
    return render(request, "p1.html")


def p2(request):
    if request.method == "GET":
        return render(request, "p2.html")
    elif request.method == "POST":
        city = request.POST.get("city")
        print(city)
        return render(request, "popup_response.html", {"city": city})
