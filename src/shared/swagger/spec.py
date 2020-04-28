import textwrap
import traceback

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec
from flask_apispec.apidoc import Converter as SwaggerConverter


class Spec:
    def __init__(self, app, url, **config):
        app.config.update({
            'APISPEC_SPEC': APISpec(**config, plugins=[MarshmallowPlugin()], **self.__default_security_schema()),
            'APISPEC_SWAGGER_UI_URL': url,
            'APISPEC_SWAGGER_URL': url + '.json'
        })

        self.app = app
        self.doc = FlaskApiSpec(app)
        self.__register_security_schema()

    def register_blueprint(self, blueprint):
        try:
            for function_name, rules in self.app.url_map._rules_by_endpoint.items():
                for rule in rules:
                    if self.__belongs_to_blueprint(function_name, blueprint):
                        view_function = self.app.view_functions[function_name]
                        self.doc.register(view_function, blueprint=blueprint.name)
                        self.__prepare_routes(rule, view_function)
        except:
            traceback.print_exc()

    def __prepare_routes(self, endpoint, view_function):
        converter = SwaggerConverter(self.app, self.doc.spec)
        swagger_formatted_endpoint = converter.get_path(endpoint, view_function)['path']

        self.__remove_options_for_all_methods(swagger_formatted_endpoint)

        method_documentations = self.__get_all_method_documentations(swagger_formatted_endpoint, endpoint.methods)
        self.__prepare_tenant_header_for_methods(method_documentations)
        self.__write_security_description_for_methods(method_documentations)

    def __remove_options_for_all_methods(self, endpoint):
        path, all_path_methods = self.__documentation_path_for_endpoint(endpoint)
        self.__remove_options(path, all_path_methods)

    def __prepare_tenant_header_for_methods(self, method_documentations):
        for method_documentation in method_documentations:
            if method_documentation.get('tenant_required', True):
                self.__register_tenant_header(method_documentation)

    def __get_all_method_documentations(self, endpoint, method_names):
        path, all_methods_documentations = self.__documentation_path_for_endpoint(endpoint)
        methods_documentations = [method for method_name, method in all_methods_documentations.items() if
                                  method_name.upper() in method_names]
        return methods_documentations

    def __remove_options(self, path, methods):
        self.doc.spec._paths[path] = {
            method_name: args for method_name, args in methods.items() if method_name != 'options'
        }

    def __register_tenant_header(self, method_documentation):
        method_documentation.setdefault('parameters', []).insert(0, self.__tenant_header_parameter())

    def __register_security_schema(self):
        self.doc.spec.components.security_scheme('access_token', dict(type='http', scheme='bearer'))

    def __documentation_path_for_endpoint(self, endpoint):
        for path, methods in self.__all_documentation_paths():
            if path == endpoint:
                return path, methods

        return None, []

    def __all_documentation_paths(self):
        return self.doc.spec._paths.items()

    @staticmethod
    def __write_security_description_for_methods(method_documentations):
        for method_documentation in method_documentations:
            Spec.__write_security_description(method_documentation)

    @staticmethod
    def __write_security_description(method_documentation):
        existing_description = method_documentation.get('description', '')
        visibility = method_documentation.get("access", "N/A")

        description = textwrap.dedent(f'''
                {existing_description}
                # Security
                
                **Visibility**: ```{visibility}``` 

                ''')

        roles = method_documentation.get('roles', [])
        if roles:
            role_list = "\n".join(f'* {role}' for role in roles)
            description += f'**Roles**:\n\n{role_list}'

        method_documentation.setdefault('description', description)

    @staticmethod
    def __belongs_to_blueprint(function_name, blueprint):
        return function_name.startswith(blueprint.name)

    @staticmethod
    def __tenant_header_parameter():
        return {
            'in': 'header',
            'name': 'x-tenant',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }

    @staticmethod
    def __default_security_schema():
        return {
            "security": [dict(access_token=[])]
        }
