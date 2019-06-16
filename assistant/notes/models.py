from django.db import models
from ckeditor.fields import RichTextField


class Note(models.Model):
    TYPES = (
        (0, 'Plain note'),
        (1, 'Link'),
        (2, 'Idea'),
        (3, 'Document'),
        (4, 'Article'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPES)
    title = models.CharField(max_length=200)
    body = RichTextField()

    def __str__(self):
        return f'[{self.get_type_display()}] {self.title}'
