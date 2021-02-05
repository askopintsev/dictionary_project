from django.db import models


class Dictionary(models.Model):
    """
    Class provides model for Dictionary entity.
    Attributes:
        name: str - contains dictionary name text
        short_name: str - contains dictionary short name text
        description: str - contains dictionary text
        version: str - contains dictionary version (!in string)
        start_date: datetime - date from which version of dictionary become actual
    """

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    description = models.TextField()
    version = models.CharField(max_length=50, blank=False)
    start_date = models.DateTimeField()

    class Meta:
        unique_together = ('id', 'version')
        db_table = 'dictionary'
        ordering = ('name',)

    def __str__(self):
        return str(self.name) + ' v.' + str(self.version)


class Element(models.Model):
    """
    Class provides model for Dictionary entity.
    Attributes:
        parent: foreign key to Dictionary entity - contains parent dictionary Id
        element_code: str - contains code of element of dictionary
        value: str - contains text of element of dictionary
    """

    parent = models.ManyToManyField(Dictionary,
                                    related_name='elements')
    element_code = models.CharField(max_length=50, blank=False)
    value = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = 'element'

    def __str__(self):
        return str(self.element_code)
