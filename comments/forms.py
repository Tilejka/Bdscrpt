from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content', )
