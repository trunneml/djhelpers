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

import logging
logger = logging.getLogger(__name__)


class AppContextError(Exception):
    pass


class ObjectDefinitionNotFound(AppContextError):
    '''
    Raised when no object definition for the requested object_id is
    found.
    '''


class Inject(object):
    '''
    Marker to define a injection keyword argument.
    '''

    def __init__(self, object_id):
        '''
        Creates a new inject definition object

        :param object_id:
        :type object_id:
        '''
        self.object_id = object_id

    def __call__(self, ioc_container):
        '''
        Injects the object with the defined object_id from
        the given container.

        :param ioc_container: The ioc container for the object look up
        :type ioc_container: ApplicationContext
        '''
        return ioc_container.get(self.object_id)


class ObjectDefinition(object):
    '''
    Represents a configuration of a service implementation
    '''

    SCOPE_SINGLETON = 'singleton'
    SCOPE_PROTOTYPE = 'prototype'
    SCOPE_REQUEST = 'request'
    SCOPE_SESSION = 'session'

    def __init__(self, object_id, factory, args=None, kwargs=None, inject=None,
                 scope=SCOPE_SINGLETON):
        '''
        ObjectDefinition Constructor

        :param object_id: the id of the defined object
        :type object_id: object
        :param factory: the implementation class
        :type factory: callable
        :param args: the args for the object initialisation
        :type args: list
        :param kwargs: the kwargs for the object initialisation
        :type kwargs: dict
        :param scope: scope of the defined object
        :type scope: str
        '''
        self.object_id = object_id
        self.factory = factory
        self.args = list(args) if args else []
        self.kwargs = dict(kwargs) if kwargs else {}
        self.scope = scope


class ApplicationContext(object):
    '''
    An IoC container to create defined objects.
    '''

    def __init__(self, config=None):
        '''
        Constructor

        :param config: Initial configuration of the new
                       application context object
        :type config: tuple or list
        '''
        logger.info('Creating new app context object')
        self._config = {}
        self._singeltons = {}
        if config:
            self.load_config(config)

    def load_config(self, config):
        for c in config:
            self.register(*c)

    def register(self, object_id, factory, args=None, kwargs=None,
                 inject=None, singelton=True):
        '''
        Registers an implementation class for the given interface.
        The interface is normally a python abc class.

        :param object_id: the interface of the implementation
        :type object_id: object
        :param factory: factory of the object
        :type factory: callable or type or func
        :param args: the args for the object factory
        :type args: tuple, list or None
        :param kwargs: the kwargs for the object factory
        :type kwargs: dict or None
        :param inject: the interface of the implemetations that should
                       be injected as a keyword argument.
        :type inject: dict or None
        '''
        logger.info('Registered new object definition: %s', object_id)
        self._config[object_id] = ObjectDefinition(
            object_id, factory, args, kwargs, inject, singelton)

    def reset(self):
        '''
        Resets the configuration and the singleton cache of the
        container.
        '''
        logger.info('Reseting application context')
        self._config.clear()
        self._singeltons.clear()

    def _eval_arg(self, arg):
        # TODO: Improve the return type
        if isinstance(arg, Inject):
            return arg(self)
        elif isinstance(arg, (list, tuple, set)):
            return [self._eval_arg(a) for a in arg]
        elif isinstance(arg, dict):
            return dict((k, self._eval_arg(arg[k])) for k in arg)
        else:
            return arg

    def _create(self, object_def):
        '''
        Creates a object for the configured concrete interface
        implementation.

        :param object_def: the configuration for the new object
        :type object_def: ObjectDefinition

        :return: a new object of the configured class.
        :rtype: object
        '''
        logger.debug('Creating new instance of: %s', object_def)
        impl_class = object_def.factory
        args = self._eval_arg(object_def.args)
        kwargs = self._eval_arg(object_def.kwargs)
        return impl_class(*args, **kwargs)

    def get(self, object_id):
        '''
        Returns the configured object with the given object_id.

        :param object_id: the identifier of the requested object
        :type object_id: object or type

        :return: a object that has the requested object_id
        :rtype: object

        :raise ObjectDefinitionNotFound: When no definition is found
        '''
        logger.debug('Quering object: %s', object_id)
        if object_id in self._singeltons:
            logger.debug('Found object "%s" in the singleton cache', object_id)
            return self._singeltons[object_id]

        object_def = self._get_object_def(object_id)
        obj = self._create(object_def)

        if object_def.scope == ObjectDefinition.SCOPE_SINGLETON:
            logger.debug('Adding "%s" to the singleton cache', object_id)
            self._singeltons[object_id] = obj
        return obj

    def get_scope(self, object_id):
        '''
        Returns the scope of the object with the given id.

        :param object_id: the object id
        :type object_id: object or type

        :return: the scope of the object
        :rtype: object

        :raise ObjectDefinitionNotFound: When no definition is found
        '''
        return self._get_object_def(object_id).scope

    def _get_object_def(self, object_id):
        '''
        Returns the object definition for the given id.

        :param object_id: the object id
        :type object_id: object or type

        :return: the object defintion
        :rtype: ObjectDefintion

        :raise ObjectDefinitionNotFound: When no definition is found
        '''
        try:
            return self._config[object_id]
        except KeyError:
            raise ObjectDefinitionNotFound(
                'No defintion for "%s" found.' % object_id)


class RequestApplicationContext(object):
    '''
    Extends the application context with session and request scope
    support.
    '''

    SESSION_KEY = 'app_context_store'

    def __init__(self, application_context, request):
        self._app_context = application_context
        self.request = request
        self._request_store = {}

    def _get_session_store(self):
        if self.SESSION_KEY not in self.request.session:
            self.request[self.SESSION_KEY] = dict()
        return self.request[self.SESSION_KEY]

    def _get_request_store(self):
        return self._request_store

    def _add_to_store(self, object_id, obj):
        scope = self._app_context.get_scope(object_id)
        if scope == ObjectDefinition.SCOPE_REQUEST:
            self._get_request_store()[object_id] = obj
        elif scope == ObjectDefinition.SCOPE_SESSION:
            self._get_session_store()[object_id] = obj

    def get(self, object_id):
        '''
        Returns the configured object with the given object_id.

        :param object_id: the identifier of the requested object
        :type object_id: object

        :return: a object that has the requested object_id
        :rtype: object
        '''
        for store in [self._get_request_store(), self._get_session_store()]:
            if object_id in store:
                return store[object_id]

        obj = self._app_context.get(object_id)
        self._add_to_store(object_id, obj)
        return obj


class ApplicationContextMiddleware(object):
    """
    Middleware that sets `app_context` attribute to request object.
    """

    def __init__(self):
        self._app_context = ApplicationContext()  # TODO: Load config

    def process_request(self, request):
        def _get(object_id):
            return self._app_context.get(object_id)
        request.app_context = _get
