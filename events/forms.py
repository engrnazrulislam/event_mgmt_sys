from django import forms
from events.models import Event, Participant,Category

"""Form Mixing"""
class StyleFormMixing:
    """ Mixing to apply style to Form field """
    default_classes = "w-full border-2 rounded-lg"
    label_class = "text-white"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
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
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"border-2 rounded-lg p-4 text-white",
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
            'category': forms.CheckboxSelectMultiple
        }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

# class ModelForm(StyleFormMixing, forms.ModelForm):
#     class Meta:
#         model =  TaskDetail
#         fields = ['priority','notes']

#     def __init__(self,*args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_styled_widgets()