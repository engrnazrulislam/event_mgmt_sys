from django import forms
from events.models import Event, Participant, Category

"""Form Mixing"""
class StyleFormMixing:

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()

    """ Mixing to apply style to Form field """
    default_classes = "input input-bordered w-full max-w-full"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            label = field.label or field_name.replace('_', ' ').capitalize()
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': "input input-bordered w-full max-w-full",
                    'placeholder': f"Enter {label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': "textarea textarea-bordered w-full",
                    'placeholder': f"Enter {label.lower()}"
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': "input input-bordered w-full max-w-full",
                    'placeholder': f"Enter {label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "select select-bordered w-full"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': "select select-bordered w-full",
                    'placeholder': f"Select {label.lower()}"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "flex gap-2"
                })
            else:
                field.widget.attrs.update({
                    'class': getattr(self, 'default_classes', 'input input-bordered w-full'),
                    'placeholder': f"Enter {label.lower()}"
                })


class EventModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','location','category']
        widgets={
            'date':forms.SelectDateWidget,
            'category': forms.Select
        }
    
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

        
class ParticipantModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

    
class CategoryModelForm(StyleFormMixing, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'descriptions']
        
    