from django.shortcuts import render
# Make 404.html setting


def page_not_found(request, exception):
    return render(request, '404.html')


# Make 500.html setting


def page_error(request):
    return render(request, '500.html')

# Make 500.html setting


def page_permission_denied(request, exception):
    return render(request, '403.html')
