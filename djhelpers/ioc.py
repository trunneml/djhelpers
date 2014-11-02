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

import inspect

import logging
logger = logging.getLogger(__name__)


class IoCConfigError(Exception):
    ''' Raised when a wrong IoCConfig is detected '''


class IoCConfig(object):
    '''
    Represents a configuration of a service implementation
    '''

    def __init__(self, impl_cls, args=None, kwargs=None, inject=None,
                 singelton=True):
        '''
        IoCConfig Constructor

        :param impl_cls: the implementation class
        :type impl_cls: type
        :param args: the args for the object initialisation
        :type args: list
        :param kwargs: the kwargs for the object initialisation
        :type kwargs: dict
        :param inject: the services that should be injected as kwargs
        :type inject: dict
        :param singelton: True when the should be only one object for
                          the service
        :type singelton: bool

        :raise IoCConfigError: When impl_cls is not a class
        '''
        if not inspect.isclass(impl_cls):
            raise IoCConfigError("impl_cls must be a class")
        self.impl_cls = impl_cls
        self.args = list(args) if args else []
        self.kwargs = dict(kwargs) if kwargs else {}
        self.inject = dict(inject) if inject else {}
        self.singelton = singelton


class IoCContainer(object):
    '''
    An IoC container to create object for given interface classes.
    '''

    def __init__(self):
        '''
        '''
        self._config = {}
        self._singeltons = {}

    def register(self, interface_class, interface_impl, args=None, kwargs=None,
                 inject=None, singelton=True):
        '''
        Registers an implementation class for the given interface.
        The interface is normally a python abc class.

        :param interface_class: the interface of the implementation
        :type interace_class: type
        :param interface_impl: the concrete implementation
                              (sub type of interface_class)
        :type interface_impl: type
        :param args: the args for the object creation of the impl
        :type args: tuple, list or None
        :param kwargs: the kwargs for the object creation of the impl
        :type kwargs: dict or None
        :param inject: the interface of the implemetations that should
                      be injected as a keyword argument.
        :type inject: dict or None
        '''
        self._config[interface_class] = IoCConfig(
            interface_impl, args, kwargs, inject, singelton)

    def reset(self):
        '''
        Resets the configuration and the singelton cache of the container.
        '''
        self._config.clear()
        self._singeltons.clear()

    def _create(self, ioc_config):
        '''
        Creates a object for the configured concrete interface implementation.

        :param ioc_config: the configuration for the new object
        :type ioc_config: IoCConfig

        :return: a new object of the configured class.
        :rtype: object
        '''
        impl_class = ioc_config.impl_cls
        args = ioc_config.args
        kwargs = {}
        kwargs.update(ioc_config.kwargs)
        for kwarg_name, interface in ioc_config.inject:
            kwargs[kwarg_name] = self.get(interface)
        return impl_class(*args, **kwargs)

    def get(self, interface):
        '''
        Returns an object of the configured implementation for
        the given interface class.

        :param interface: the (interface class of the) requested serve
        :type interface: type

        :return: a object that has the requested interface
        :rtype: object
        '''
        if interface in self._singeltons:
            return self._singeltons[interface]

        service_conf = self._config[interface]
        service = self._create(service_conf)

        if service_conf.singelton:
            self._singeltons[interface] = service
        return service
