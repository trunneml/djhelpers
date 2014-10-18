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
import unittest
import mock

from djhelpers.adminhelpers import ActionDecorator
from djhelpers.modelhelpers import short_description


class ShortDescriptionDecoratorTest(unittest.TestCase):

    def test_decorator(self):
        # Arrange
        description = 'description'
        # Act
        @short_description(description)
        def tfunc(x):
            return x
        result = tfunc(mock.sentinel.func_test_parameter)
        # Assert
        self.assertEqual(result, mock.sentinel.func_test_parameter)
        self.assertEqual(tfunc.short_description, description)
        self.assertFalse(hasattr(tfunc, 'boolean'))
    
    def test_decorator_with_kwargs(self):
        # Arrange
        description = 'description'
        # Act
        @short_description(description, boolean=mock.sentinel.kwarg)
        def tfunc(x):
            return x
        result = tfunc(mock.sentinel.func_test_parameter)
        # Assert
        self.assertEqual(result, mock.sentinel.func_test_parameter)
        self.assertEqual(tfunc.short_description, description)
        self.assertEqual(tfunc.boolean, mock.sentinel.kwarg)


class ActionDecoratorTest(unittest.TestCase):
    
    def test_admin_action(self):
        # Arrange
        actions = ActionDecorator()
        # Act
        desc = 'test description'
        @actions.action(desc)
        def _t(x):
            return x
        # Assert
        self.assertIsInstance(actions, list)
        self.assertIn(_t, actions)
        self.assertEqual(len(actions), 1)
        self.assertEqual(_t.short_description, desc)


if __name__ == '__main__':
    suite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(suite)        
        
