from django import forms
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView
)


# Create your views here.
class ProfileAll(ListView):
    # In the 'ProfileDetail' I managed authentication and permissions using
    # custom coded rules via information in GET request. This is not
    # 'Django-ish' way of doing it for class-based views. There are mixins and
    # inherited attributes for that. I'll implement permission functionality 
    # for this view and 'ProfileDelete' and 'ProfileUpdate' using them, 
    # but later. As of now I want to realise other features of the site.
    # But I sure will!!!
    queryset = User.objects.all()
    context_object_name = 'users_list'
    template_name = 'profiles/all.html'

class ProfileCreate(CreateView):
    model = User
    template_name = 'profiles/create.html'
    fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(self.request, user)
        return redirect('profiles-detail', pk=user.id)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form

class ProfileDetail(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # This is a, what is called in Russian development process, a
            # 'костыль' to get the requested user id. If we just type
            # request.user.id then the user will be auto redirected to his
            # own user ID. It is intended behaviour for normal users and 
            # for workers. But if a superuser or an admin would want to
            # check some user's profile, then it won't be available to him,
            # because, as stated above, admin/superuser will be redirected to
            # his own (id=1, for example) profile. 
            # So, the idea behind this 'костыль' is we GET, for example,
            # URL 'profiles/2212/', remove 'profiles/' and the leading slash,
            # to get the ID (2212). Then we compare the user's actual id 
            # (request.user.id) with the requested one (2212). If they are
            # the same, we return the user his profile, 
            # if not, we look if the user.is_superuser, and if not, we 404,
            # otherwise we return the profile's page to the superuser.
            # After getting the profile_id we just search against it for other
            # fields.
            profile_id = int(request.path[10:len(request.path)-1])

            g = Group.objects.get(name='Workers')
            workers_username = [
                key.get('username') for key in g.user_set.values()
            ]

            if profile_id == request.user.id or request.user.is_superuser:
                context = {
                    'workers_username': 
                        workers_username,
                    'profile_id': 
                        profile_id,
                    'profile_first_name': 
                        User.objects.get(id=profile_id).first_name,
                    'profile_last_name': 
                        User.objects.get(id=profile_id).last_name,
                    'profile_email': 
                        User.objects.get(id=profile_id).email,
                    'profile_username': 
                        User.objects.get(id=profile_id).username,
                    'profile_date_joined': 
                        User.objects.get(id=profile_id).date_joined
                }
            else:
                # You can actually return the user's actual profile
                # instead of 404 if you duplicate the 'context' but 
                # change first field with {'profile_id: request.user.id}
                raise Http404
            return render(request, 'profiles/detail.html', context)
        else:
            raise Http404



class ProfileDelete(DeleteView):
    model = User
    template_name = 'profiles/delete.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        # I actually found out how to get profile_id out of URL, so now I can
        # Actually remake the 'костыль' in 'ProfileDetail'. But I won't. I want
        # it to remain there as a reminder of what I came up with, even though
        # it wasn't the best solution. So, the "ProfileDetail"'ll remain like
        # that for historical reasons.
        profile_id = self.kwargs.get('pk')
        user = self.request.user

        if self.request.user.is_authenticated and (
            user.id == profile_id or user.is_superuser):
            return get_object_or_404(self.model, id=profile_id)
        else:
            raise Http404

class ProfileUpdate(UpdateView):
    template_name = 'profiles/update.html'
    fields = ['username', 'email', 'first_name', 'last_name']
    model = User
    success_url = '../'

    def get_context_data(self, **kwargs):
        # Same logic as 'profile_id' in 'def get(self, request, ...)' above
        # but here we also remove 'update' to the right of the profile's ID
        profile_id = int(self.request.path[10:len(self.request.path)-8])
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.id == profile_id or user.is_superuser:
            context.update({
                'profile_id': profile_id, 
                'object':User.objects.get(id=profile_id)
            })
            return context
        else:
            raise Http404

    def form_valid(self, form):
        return super().form_valid(form)
