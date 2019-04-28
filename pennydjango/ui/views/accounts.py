from django.contrib.auth import login, update_session_auth_hash
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import PasswordChangeForm

from penny.models import User
from penny.forms import CustomUserCreationForm, UserProfileForm

from ui.views.base_views import BaseContextMixin


class Signup(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserProfile(BaseContextMixin, DetailView):
    model = User
    custom_stylesheet = 'user.css'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def context(self, request, *args, **kwargs):
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        redirect = False

        if request.method == 'POST':
            if request.POST.get('type') == 'edit_profile':
                profile_form = UserProfileForm(
                    request.POST,
                    request.FILES,
                    instance=request.user
                )
                # import ipdb; ipdb.set_trace()
                if profile_form.is_valid():
                    profile_form.save()
                    redirect = True

            if request.POST.get('type') == 'password_change':
                password_form = PasswordChangeForm(request.user, request.POST)
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    redirect = True

        is_me = self.object == request.user
        return {
            'is_me': is_me,
            'profile_form': profile_form,
            'password_form': password_form,
            'redirect': redirect
        }

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if context.get('redirect'):
            return HttpResponseRedirect(reverse(
                'userprofile', args=[request.user]
            ))

        return self.render_to_response(context)
