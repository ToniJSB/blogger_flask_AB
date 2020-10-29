from flask_appbuilder.security.sqla.manager import SecurityManager

class MySecurityManager(SecurityManager):
    role_model= 'MyRole'