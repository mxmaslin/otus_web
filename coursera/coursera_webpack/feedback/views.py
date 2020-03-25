from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import FeedbackForm


class FeedbackView(FormView):
    template_name = 'feedback/feedback.html'
    form_class = FeedbackForm
    success_url = '/feedback/thanks/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def thanks(request):
    return render(request, 'feedback/thanks.html', {})
