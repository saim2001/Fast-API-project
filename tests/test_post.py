import pytest
from app import schema
def test_get_all_posts(authorized_client,add_posts):
    res = authorized_client.get('/posts/')
    print(res.json())
    def validate(post):
        return schema.AllPostResp(**post)
    map(validate,res.json())
    assert len(res.json()) == len(add_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client,add_posts):

    res = client.get('/posts/')
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client,add_posts):

    res = client.get(f'/posts/{add_posts[0].id}')
    assert res.status_code == 401

def test_get_one_posts_not_exist(authorized_client,add_posts):
    res = authorized_client.get(f'/posts/232323')
    assert res.status_code == 404

def test_get_one_post(authorized_client,add_posts):
    res = authorized_client.get(f'/posts/{add_posts[0].id}/')
    print(res.json())
    post = schema.AllPostResp(**res.json())
    assert post.post.id == add_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize('title,content,published',[
    ('first title','first content',True),
    ('second title','second content',False),
    ('third title','third content',True)        
])
def test_create_post(authorized_client,add_posts,title,content,published):
    res = authorized_client.post('/posts/',json={
        'title':title,
        'content':content,
        'published':published
    })
    created_post = schema.PostResp(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_create_post_defualt_true(authorized_client,test_user):
    res = authorized_client.post('/posts/',json={
        'title':'example title',
        'content':'example content',
    })
    created_post = schema.PostResp(**res.json())
    assert res.status_code == 201
    assert created_post.title == 'example title'
    assert created_post.content == 'example content'
    assert created_post.published == True
    assert created_post.owner.id == test_user['id']

def test_unauthorized_user_get_one_posts(client,add_posts):

    res = client.post('/posts/',json={
        'title':'example title',
        'content':'example content',
    })
    assert res.status_code == 401