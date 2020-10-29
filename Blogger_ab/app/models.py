from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy_serializer import SerializerMixin


class Post(Model, SerializerMixin):
    __tablename__='post'

    serialize_only = ('id', 'title', 'date_posted','content')

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    author = relationship('User', backref='posts')

    @property
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_posted' : self.date_posted,
            'content' : self.content,
            'author' : self.user_id  
        }

    def __repr__(self):
        return f"Post('{self.title}','{self.content}','{self.author}', '{self.date_posted}')"

class Comment(Model, SerializerMixin):
    serialize_only=('id','post_id','user_id','text')
    __tablename__='comment'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    post = relationship('Post', backref='comments')
    user_id = Column(Integer, ForeignKey('ab_user.id'), primary_key=True)
    user = relationship('User', backref='commentator')
    text = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.post_id}', '{self.user_id}', '{self.text}', '{self.date_posted}')"

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
