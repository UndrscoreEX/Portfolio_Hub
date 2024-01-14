from django.shortcuts import render

# Create your views here.

def home(req):

    return render(req,'portfolio/portfolio.html')

def about(req):

    return render(req,'portfolio/about.html')

def graphicD(req):

    return render(req,'portfolio/graphicD.html')

def it(req):

    return render(req,'portfolio/IT.html')

def personalCoach(req):

    return render(req,'portfolio/personalCoach.html')

def projects(req):

    return render(req,'portfolio/projects.html')
