from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# mixins for class based views

class LoginRequiredMixin():
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/archiva/login/')

"""class LoginRequiredMixin(object):
   
    View mixin which requires that the user is authenticated.
   
    @method_decorator(login_required(login_url='/archiva/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            self, request, *args, **kwargs)"""