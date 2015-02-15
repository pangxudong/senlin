# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import collections
import six

from senlin.common import exception


class BaseConstraint(object):
    def __str__(self):
        '''Utility method for generating schema docs.'''
        return self.desc()

    def validate(self, value, context=None):
        '''Base entry for validation.
        :param value: value for validation.
        :param schema: the schema that may provide customized validation.
        :param context: optional argument in case validation needs a context.
        '''
        # The actual validation is implemented by subclasses
        if not self._validate(value, context):
            raise ValueError(self._error(value))


class AllowedValues(BaseConstraint):
    def __init__(self, allowed_values):
        if (not isinstance(allowed_values, collections.Sequence) or
                isinstance(allowed_values, six.string_types)):
            msg = _('AllowedValues must be a list or a string')
            raise exception.InvalidSchemaError(message=msg)

        self.allowed = tuple(allowed_values)

    def desc(self):
        values = ', '.join(str(v) for v in self.allowed)
        return _('Allowed values: %s') % values

    def _error(self, value):
        values = ', '.join(str(v) for v in self.allowed)
        return _('"%(value)s" must be one of the allowed values: '
                 '%(allowed)s') % dict(value=value, allowed=values)

    def _validate(self, value, context=None):
        if isinstance(value, collections.Sequence):
            return all(v in self.allowed for v in value)

        return value in self.allowed
