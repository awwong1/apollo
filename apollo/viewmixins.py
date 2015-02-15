from actstream import action
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(*args, **kwargs)
        return login_required(view)


class StaffRequiredMixin(object):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_staff:
            return super(StaffRequiredMixin, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to access this portion of the site.")
            return redirect('/')


class ActivitySendMixin(object):
    """
    Adds an activity message on successful form submission.
    """
    activity_verb = ''

    def form_valid(self, form):
        response = super(ActivitySendMixin, self).form_valid(form)
        activity_message = self.get_activity_verb()
        action.send(self.request.user, verb=activity_message, target=self.object)
        return response

    def get_activity_verb(self):
        return self.activity_verb
