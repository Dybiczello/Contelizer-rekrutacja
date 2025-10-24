import re
import random
from django.shortcuts import render
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