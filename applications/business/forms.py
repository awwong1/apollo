from applications.business.models import BusinessMembership, Business
from django.forms import ModelForm


class BusinessMembershipForm(ModelForm):
    class Meta:
        model = BusinessMembership
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        business_id = kwargs.pop('business_pk', None)
        super(BusinessMembershipForm, self).__init__(*args, **kwargs)
        if business_id is not None:
            self.fields['business'].queryset = Business.objects.filter(pk=business_id)
        elif kwargs.get('instance', None) is not None:
            self.fields['business'].queryset = Business.objects.filter(pk=kwargs['instance'].business.pk)
        self.fields['user'].empty_label = None
        self.fields['business'].empty_label = None
        self.fields['business'].widget.attrs['readonly'] = 'readonly'