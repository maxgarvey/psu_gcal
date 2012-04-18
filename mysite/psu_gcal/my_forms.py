from django import forms

#the calendar form, just a couple requestors and a cal name
class CalendarForm( forms.Form ):
    calendar_name = forms.CharField(max_length=100) #cal name
    calendar_requestor_1 = forms.CharField(max_length=100,required=False) #requestor 1
    calendar_requestor_2 = forms.CharField(max_length=100,required=False) #requestor 2

class GroupForm( forms.Form ):
    group_email = forms.CharField(max_length=100) #group email
    group_name = forms.CharField(max_length=100) #group name
    group_description = forms.CharField(max_length=100) #group description
    group_requestor_1 = forms.CharField(max_length=100,required=True) #group requestor 1
    group_requestor_2 = forms.CharField(max_length=100,required=True) #group requestor 2
