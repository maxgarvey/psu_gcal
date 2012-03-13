from django import forms

#the calendar form, just a couple requestors and a cal name
class NewCalendar( forms.Form ):
  calendar_name = forms.CharField(max_length=100) #cal name
  requestor_1 = forms.CharField(max_length=100,required=False) #requestor 1
  requestor_2 = forms.CharField(max_length=100,required=False) #requestor 2
