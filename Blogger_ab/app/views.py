import json

from flask import g, render_template
from flask_appbuilder import widgets
from flask_appbuilder.baseviews import BaseCRUDView
from flask_appbuilder.fields import QuerySelectField
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.security.decorators import permission_name
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder import ModelView, BaseView, ModelRestApi, expose
from flask_babel import lazy_gettext as _l

from . import app, appbuilder, db
from .models import Post

def get_user():
    return g.user
def get_username():
    return g.user.username

@permission_name('MyRole')
class PostListUserView(ModelView):
    datamodel = SQLAInterface(Post,db.session)
    route_base = '/post'
    list_template = 'post_list.html'
    
    base_filters = [['author', FilterEqualFunction, get_user]]

    add_form_query_rel_fields={
        'author': [['username',FilterEqualFunction,get_username]]
    }
    add_form_extra_fields={
        'Author': QuerySelectField(
                'User',
                widget=Select2Widget()
        )
    }
    show_fieldsets = [
        (
            'information about Post',
            {'fields': [_l('title'),_l('content'), _l('date_posted')]}
        ),
        (
            'information about Author',
            {'fields': ['author.first_name', 'author.username']}
        )
    ]
    list_columns = ['title','content','author.username']
    edit_columns = ['title','content']
    label_columns = {'author.username':'Author'}
        

@permission_name('MyRole')
class PostListView(ModelView):
    datamodel = SQLAInterface(Post,db.session)

    route_base = '/posts'
    list_template = 'post_list.html'
    show_fieldsets = [
        (
            'info del post',
            {'fields': ['title','content', 'date_posted']}
        ),
        (
            'info del autor',
            {'fields': ['author.first_name', 'author.username']}
        )
    ]
    list_columns = ['title','content','author.username']
    label_columns = {'author.username':'Author','author.first_name':'Name'}


"""
    Posible opción
    @expose('/lista')
    def postList(self):
        post = self.datamodel.query()
        posts = []
        for articulo in list(post)[1]:
            posts.append(articulo.to_dict())
        print(posts)
        return self.render_template('post_list.html',posts=posts)
"""
"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )

db.create_all()



appbuilder.add_view(PostListUserView,'list my posts',category='articles')
appbuilder.add_view(PostListView,'list all posts',category='articles')

appbuilder.security_cleanup()
