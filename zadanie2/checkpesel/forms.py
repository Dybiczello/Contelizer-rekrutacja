from django import forms
import datetime

class UploadPesel(forms.Form):
    pesel = forms.CharField(label="Enter your PESEL number", max_length=11)

    def clean_pesel(self):
        pesel = self.cleaned_data['pesel'].strip()
        if len(pesel) != 11 or not pesel.isdigit():
            raise forms.ValidationError("PESEL must be exactly 11 digits.")
        
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = 0
        for i in range(10):
            checksum += int(pesel[i]) * weights[i]

        checksum = (10 - (checksum % 10)) % 10

        if checksum != int(pesel[10]):
            raise forms.ValidationError("Invalid PESEL number.")
        
        return pesel
    
    def clean(self):
        cleaned_data = super().clean()
        pesel = cleaned_data.get("pesel")
        if not pesel:
            return cleaned_data
        
        day = int(pesel[4:6])
        month = int(pesel[2:4])
        year = int(pesel[0:2])

        if 1 <= month <= 12:
            century = 1900
            month = month
        elif 21 <= month <= 32:
            century = 2000
            month = month - 20
        elif 41 <= month <= 52:
            century = 2100
            month = month - 40
        elif 61 <= month <= 72:
            century = 2200
            month = month - 60
        elif 81 <= month <= 92:
            century = 1800
            month = month - 80
        else:
            raise forms.ValidationError("Invalid month in PESEL number.")
        
        year = century + year
        try:
            birth_date = datetime.date(year, month, day)
        except ValueError:
            raise forms.ValidationError("Invalid date in PESEL number.")
        
        gender_digit = int(pesel[9])
        if gender_digit % 2 == 0:
            gender = 'Female'
        else:
            gender = 'Male'

        cleaned_data['birth_date'] = birth_date
        cleaned_data['gender'] = gender

        return cleaned_data