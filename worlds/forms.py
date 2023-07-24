from django import forms

from worlds.models import WComment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here',
        'rows': '4',
    }))

    class Meta:
        model = WComment
        fields = ('content', )
