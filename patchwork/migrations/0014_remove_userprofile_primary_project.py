# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patchwork', '0013_slug_check_context'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='primary_project',
        ),
    ]
