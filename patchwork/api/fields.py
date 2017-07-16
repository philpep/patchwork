# Patchwork - automated patch tracking system
# Copyright (C) 2017 Linaro Corporation
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Patchwork; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django.utils.translation import ugettext_lazy as _
from rest_framework.relations import RelatedField

from patchwork.models import State


def format_state_name(state):
    return ' '.join(state.split('-'))


class StateField(RelatedField):
    """Avoid the need for a state endpoint.

    NOTE(stephenfin): This field will only function for State names consisting
    of alphanumeric characters, underscores and single spaces. In Patchwork
    2.0+, we should consider adding a slug field to the State object and make
    use of the SlugRelatedField in DRF.
    """
    default_error_messages = {
        'required': _('This field is required.'),
        'invalid_choice': _('Invalid state {name}. Expected one of: '
                            '{choices}.'),
        'incorrect_type': _('Incorrect type. Expected string value, received '
                            '{data_type}.'),
    }
    queryset = ''  # django 1.6, rest_framework 3.2 require this

    def to_internal_value(self, data):
        try:
            data = format_state_name(data)
            return self.get_queryset().get(name__iexact=data)
        except State.DoesNotExist:
            self.fail('invalid_choice', name=data, choices=', '.join([
                format_state_name(x.name) for x in self.get_queryset()]))
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, obj):
        return obj.slug

    def get_queryset(self):
        return State.objects.all()
