from django.shortcuts import render,redirect

from django.http import HttpResponse

import markdown

from . import util

import random

def index(request):
    entries = util.list_entries()
    if request.method == "POST": 
        query = request.POST['q']
        if query not in entries:
            searches = []
            for entry in entries:
                if query in entry:
                    searches.append(entry)
            return render(request, "encyclopedia/search.html",{
                "searches": searches
            })
        else:
            return redirect('title', name=query)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

def title(request, name):
    if request.method == "POST":
        if 'q' in request.POST:
            return index(request)
        else:
            return redirect('edit_page', request.POST['name'])
    else:
        entry = util.get_entry(name)
        html_data = markdown.markdown(entry)
        if entry:
            return render(request, "encyclopedia/entry.html",{
                "title": name,
                "content": html_data
            })
        else:
            return HttpResponse("<h1>Error proccesing request!</h1>")

def new_page(request):
    entries = util.list_entries()
    if request.method == "POST":
        if 'q' in request.POST:
            return index(request)
        name = request.POST['title']
        markdown_content = request.POST['markdown']
        if name not in entries:
            if not (name == "" or markdown_content == ""):
                util.save_entry(name,markdown_content)
                return redirect('title', name=name)
            else:
                return render(request, "encyclopedia/new_page.html")
        else:
            return HttpResponse("<h1>Error proccesing request!</h1>")
    return render(request, "encyclopedia/new_page.html")

def edit_page(request,name):
        if request.method == "POST":
            if 'q' in request.POST:
                return index(request)
            util.save_entry(name,request.POST['markdown'])
            return redirect('title', name=name)
        else:
            md_content = util.get_entry(name)
            return render(request, "encyclopedia/edit_page.html",{
                "name": name,
                "md_content": md_content
            })

def random_page(request):
        page_entries = util.list_entries()
        random_entry = random.choice(page_entries)
        return redirect(title, name=random_entry)