from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .utils import get_mongo_db


# Create your views here.
def main(request, page=1):
    db = get_mongo_db()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})

    return render(request, 'quotes/quote.html', context={"tags": tags, "authors": authors, 'form': QuoteForm()})


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='quotes:main')


def detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quotes/detail.html', {"quote": quote})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, name=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    return render(request, 'quotes/tags.html', {"quotes": quotes, "tag_id": tag_id})


def author_detail(request, author_id):
    author = get_object_or_404(Author, fullname=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/authors.html', {"quotes": quotes, "author_id": author_id, "author": author})


@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = QuoteForm(instance=quote)
    return render(request, 'quotes/edit_quote.html', {'form': form})

