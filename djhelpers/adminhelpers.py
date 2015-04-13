# Copyright 2014 Michael Trunner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Some django admin helper classes and decorators.
"""

# The shot_description decorator can be helpful in the django admin, too.
from djhelpers.modelhelpers import short_description  # pylint: disable=unused-import


class ActionDecorator(list):
    """
    This class is a easy way to create a list of django admin actions.

    Just create a actions field of that class in our model admin and
    write @actions.action('Nice description') on top of every admin
    action method in your model admin class.

    Usage:

    >>> from django.contrib import admin
    >>>
    >>> class SomeModelAdmin(admin.ModelAdmin):
    ...
    ...     actions = ActionDecorator()
    ...
    ...     @actions.action("Mark selected stories as published")
    ...     def make_published(self, request, queryset):
    ...         queryset.update(status='p')
    ...
    >>>
    """

    def action(self, description):
        """
        Adds a short_description field to the decorated method and
        adds it to the (admin actions) list.

        :param description: the value for the short description attribute
        :type description: str or unicode

        :return: the decorator function
        :rtype: function
        """
        def wrap(func):  # pylint: disable=missing-docstring
            # set description
            func.short_description = description
            # add function to admin actions
            self.append(func)
            # we do not need to modify the function
            return func
        return wrap


class NoDeleteSelectedModelAdminMixin(object):
    """
    This mixin removes the delete_selected admin action from the
    admin action drop down, when show_delete_selected is set to False.
    """

    show_delete_selected = False

    def get_actions(self, request):
        # pylint: disable=missing-docstring
        actions = super(NoDeleteSelectedModelAdminMixin,
                        self).get_actions(request)
        if not self.get_show_delete_selected():
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_show_delete_selected(self):
        # pylint: disable=missing-docstring
        return self.show_delete_selected
