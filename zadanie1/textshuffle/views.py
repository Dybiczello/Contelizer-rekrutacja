import re
import random
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFile
from django.contrib import messages

def shuffle_word(word):
    if len(word) <= 3:
        return word
    first = word[0]
    last = word[-1]
    middle = list(word[1:-1])
    random.shuffle(middle)
    return first + ''.join(middle) + last

word_re = re.compile(r"\b\w+(?:-\w+)*\b", re.UNICODE)

def shuffle_text(text):
    def replace(match):
        return shuffle_word(match.group(0))
    return word_re.sub(replace, text)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            raw_file = uploaded_file.read()
            try:
                content = raw_file.decode('utf-8')
            except UnicodeDecodeError:
                content = raw_file.decode('utf-8', errors='replace')

            shuffled_content = shuffle_text(content)
            request.session['shuffled_content'] = shuffled_content
            return redirect('textshuffle:result')
    else:
        form = UploadFile()
    return render(request, 'upload.html', {'form': form})

def result(request):
    shuffled_content = request.session.get('shuffled_content')
    if not shuffled_content:
        messages.error(request, "No shuffled content found. Please upload a file first.")
        return redirect('textshuffle:upload_file')
    return render(request, 'result.html', {'shuffled_content': shuffled_content})