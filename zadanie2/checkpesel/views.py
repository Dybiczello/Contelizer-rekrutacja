from django.shortcuts import render
from .forms import UploadPesel


def upload_pesel(request):
    if request.method == 'POST':
        form = UploadPesel(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            birth_date = form.cleaned_data.get('birth_date')
            gender = form.cleaned_data.get('gender')
            return render(request, 'result.html', {'pesel': pesel, 'birth_date': birth_date, 'gender': gender})
    else:
        form = UploadPesel()
    return render(request, 'upload.html', {'form': form})

def result(request):
    pesel = request.GET.get('pesel')
    birth_date = request.GET.get('birth_date')
    gender = request.GET.get('gender')
    return render(request, 'result.html', {'pesel': pesel, 'birth_date': birth_date, 'gender': gender})