# coding=utf-8

from os.path import join

from guniflask.context import configuration, bean
from guniflask.oauth2_config import enable_authorization_server, enable_resource_server, \
    AuthorizationServerConfigurerAdapter, ResourceServerConfigurerAdapter, AuthorizationServerEndpointsConfigurer, \
    ClientDetailsServiceConfigurer, ResourceServerSecurityConfigurer
from guniflask.oauth2 import InMemoryClientDetailsService, TokenStore, JwtTokenStore, JwtAccessTokenConverter, \
    ClientDetails
from guniflask.config import settings
from guniflask.security import PasswordEncoder, AuthenticationManager, UserDetailsService
from guniflask.security_config import enable_web_security, WebSecurityConfigurer, AuthenticationManagerBuilder, \
    HttpSecurity

from uaa.security.password_encoder import BcryptPasswordEncoder


@configuration
@enable_authorization_server
class UaaAuthorizationConfiguration(AuthorizationServerConfigurerAdapter):

    def __init__(self, authentication_manager: AuthenticationManager):
        self._authentication_manager = authentication_manager
        self._jwt_access_token_converter = self._get_jwt_access_token_converter()

    def configure_endpoints(self, endpoints: AuthorizationServerEndpointsConfigurer):
        endpoints \
            .with_authentication_manager(self._authentication_manager) \
            .with_access_token_converter(self._jwt_access_token_converter)

    def configure_client_details_service(self, clients: ClientDetailsServiceConfigurer):
        client_details = ClientDetails(client_id='web_app',
                                       grant_types=['password', 'refresh_token'],
                                       scope=['openid'])
        client_details_store = {client_details.client_id: client_details}
        client_details_service = InMemoryClientDetailsService(client_details_store)
        clients.with_client_details_service(client_details_service)

    @bean
    def token_store(self) -> TokenStore:
        return JwtTokenStore(self._jwt_access_token_converter)

    @bean
    def jwt_access_token_converter(self) -> JwtAccessTokenConverter:
        return self._jwt_access_token_converter

    def _get_jwt_access_token_converter(self) -> JwtAccessTokenConverter:
        with open(join(settings['home'], 'public_key.pem'), 'r') as f:
            public_key = f.read()
        with open(join(settings['home'], 'private_key.pem'), 'r') as f:
            private_key = f.read()

        token_converter = JwtAccessTokenConverter()
        token_converter.signing_algorithm = 'RS256'
        token_converter.signing_key = private_key
        token_converter.verifying_key = public_key
        return token_converter


@configuration
@enable_resource_server
class UaaResourceConfiguration(ResourceServerConfigurerAdapter):

    def __init__(self, token_store: TokenStore):
        self._token_store = token_store

    def configure_security(self, resources: ResourceServerSecurityConfigurer):
        resources.with_token_store(self._token_store)


@configuration
@enable_web_security
class UaaWebSecurityConfiguration(WebSecurityConfigurer):
    def __init__(self, user_details_service: UserDetailsService,
                 authentication_manager_builder: AuthenticationManagerBuilder):
        super().__init__()
        self._password_encoder = BcryptPasswordEncoder()
        authentication_manager_builder \
            .with_user_details_service(user_details_service) \
            .with_password_encoder(self._password_encoder)

    def configure_http(self, http: HttpSecurity):
        cors = settings.get_by_prefix('guniflask.cors')
        if cors:
            http.cors(cors)

    @bean
    def password_encoder(self) -> PasswordEncoder:
        return self._password_encoder

    @bean
    def authentication_manager_bean(self) -> AuthenticationManager:
        return super().authentication_manager_bean()
