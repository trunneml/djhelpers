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

def short_description(description, **kwargs):
    """
    This decorator adds the django short_description attribute to the
    given function.
    
    It also adds every keyword argument as extra attribute to the
    decorated function.
    
    :param description: the value for the short description attribute
    :type description: str or unicode
    
    :return: the decorator function
    :rtype: function 
    """
    def _wrapper(func):
        func.short_description = description
        for key in kwargs:
            setattr(func, key, kwargs[key])
        return func
    return _wrapper

