from django.shortcuts import render, get_object_or_404
from .models import Writer, Quote, Work
import random


def home(request):
    query = request.GET.get('q', '')
    epoch = request.GET.get('epoch', '')
    letter = request.GET.get('letter', '')
    writers = Writer.objects.all()
    if query:
        writers = writers.filter(name__icontains=query)
    if epoch:
        writers = writers.filter(epoch__icontains=epoch)
    if letter:
        writers = writers.filter(name__istartswith=letter)
    epochs = Writer.objects.values_list('epoch', flat=True).distinct()
    letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return render(request, 'writers/home.html', {
        'writers': writers,
        'epochs': epochs,
        'query': query,
        'selected_epoch': epoch,
        'selected_letter': letter,
        'letters': letters,
    })
def writer_detail(request, pk):
    writer = get_object_or_404(Writer, pk=pk)
    return render(request, 'writers/detail.html', {'writer': writer})


def random_writer(request):
    writers = Writer.objects.all()
    if writers.exists():
        writer = random.choice(list(writers))
        from django.shortcuts import redirect
        return redirect('writer_detail', pk=writer.pk)
    return redirect('home')    

def statistics(request):
    from django.db.models import Count
    total = Writer.objects.count()
    by_epoch = Writer.objects.values('epoch').annotate(count=Count('id')).order_by('-count')
    return render(request, 'writers/statistics.html', {
        'total': total,
        'by_epoch': by_epoch,
    })

def timeline(request):
    writers = Writer.objects.all().order_by('birth_year')
    return render(request, 'writers/timeline.html', {'writers': writers})

def about(request):
    total_writers = Writer.objects.count()
    total_works = Work.objects.count()
    total_quotes = Quote.objects.count()
    return render(request, 'writers/about.html', {
        'total_writers': total_writers,
        'total_works': total_works,
        'total_quotes': total_quotes,
    })        


    