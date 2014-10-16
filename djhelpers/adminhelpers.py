'''
Created on 16.10.2014

@author: trunneml
'''

from . import modelhelpers


short_description = modelhelpers.short_description


class ActionDecorator(list):
    """
    This class is a easy way to create a list of django admin actions.
    
    Just create a actions field of that class in our model admin and
    write @actions.action('Nice description') on top of every admin
    action method in your model admin class.
    """
    
    def action(self, desc):
        """
        Adds a short_description field to the decorated method and
        adds it to the (admin actions) list.
        """
        def wrap(f):
            # set description
            f.short_description = desc
            # add function to admin actions
            self.append(f)
            # we do not need to modify the function
            return f
        return wrap
