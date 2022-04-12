from django.shortcuts import render
from django.views.generic import FormView
from .forms import ContactsForm
from django.core.mail import EmailMessage


# Create your views here.
class ContactsMain(FormView):
    template_name = 'contacts/main.html'
    form_class = ContactsForm
    context = {
        'form': form_class
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'contacts/main.html', self.context)

    def post(self, request, *args, **kwargs):
        email_message = EmailMessage(
            subject="Message From E-Shop",
            body=(
                'Phone:\n' + 
                request.POST.get('phone') + "\n\r" +
                'Company Name:\n' +
                request.POST.get('company_name') + '\n\r' +
                'Message:\n' +
                request.POST.get('description')
            ),
            from_email=request.POST.get('email'),
            to=['slavadjango@gmail.com'],
        )
        email_message.send(fail_silently=False)
        return render(request, 'contacts/main.html', self.context)
