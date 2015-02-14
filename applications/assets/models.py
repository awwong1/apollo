import re
from django.db import models


class Equipment(models.Model):
    name = models.CharField(
        max_length=60, unique=True, help_text="What is the name of this equipment?"
    )
    description = models.TextField(
        help_text="What is the description for this equipment?"
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name


class Service(models.Model):
    name = models.CharField(
        max_length=255, unique=True,
        help_text="What is the human display readable name of this service?"
    )
    activation_id = models.CharField(
        max_length=255, unique=True, default="",
        help_text="What is the Python re module activation regex for this service?"
    )
    activate = models.ForeignKey(
        'Equipment',
        help_text="Which equipment does this service activate?"
    )

    def activates(self, activation_id):
        """
        Checks if the provided activation_id activates this service.
        :param activation_id:
        :return: Boolean, True if activates, False otherwise.
        """
        regex = self.activation_id
        match_object = re.match(regex, activation_id)
        if match_object:
            return True
        return False

    def __str__(self):
        return "{0}: {1}".format(self.name, self.activation_id)

    def __unicode__(self):
        return u"{0}: {1}".format(self.name, self.activation_id)
