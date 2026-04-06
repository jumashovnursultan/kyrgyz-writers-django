from django.shortcuts import render, get_object_or_404
from .models import Writer
import random


def home(request):
    query = request.GET.get('q', '')
    epoch = request.GET.get('epoch', '')
    writers = Writer.objects.all()
    if query:
        writers = writers.filter(name__icontains=query)
    if epoch:
        writers = writers.filter(epoch__icontains=epoch)
    epochs = Writer.objects.values_list('epoch', flat=True).distinct()
    return render(request, 'writers/home.html', {
        'writers': writers,
        'epochs': epochs,
        'query': query,
        'selected_epoch': epoch,
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