from django import forms
from events.models import Event, Participant, Category

"""Form Mixing"""
class StyleFormMixing:
    """ Mixing to apply style to Form field """
    default_classes = "border-2 rounded-lg p-4 w-full"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':"input input-bordered input-primary w-full max-w-xs",
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 rounded-lg",
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Select):
                field.widget.attrs.update({
                    'class' : "select select-bordered w-full max-w-xs select-lg",
                    'placeholder':f"Enter {field.label}"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"checkbox-primary",
                    'placeholder':f"Enter {field.label}"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

class EventModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','location','category']
        widgets={
            'date':forms.SelectDateWidget,
            'category': forms.Select
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class ParticipantSelectionForm(StyleFormMixing, forms.Form):
        participants = forms.ModelMultipleChoiceField(
            queryset=Participant.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label="Select Participants"
            )
        class Meta:
            model = Participant
            fields = ['name','email','participants']

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.apply_styled_widgets()

class ParticipantModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()

class CategoryModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'descriptions']
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()