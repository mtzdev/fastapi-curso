from fast_zero.models import TodoState
from tests.conftest import TodoFactory

def test_create_todo(client, token):
    response = client.post('/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'This is a test todo item.',
            'state': 'draft'
        }
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'This is a test todo item.',
        'state': 'draft'
    }

def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

def test_list_todos_pagination_should_return_2_todos(session, user, client, token):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

def test_list_todos_filter_title_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

def test_list_todos_filter_description_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='description')
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

def test_list_todos_filter_combined_should_return_5_todos(session, user, client, token):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done
        )
    )

    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json() == {'message': 'Task deleted successfully.'}

def test_delete_todo_error(session, client, user, token):
    response = client.delete(f'/todos/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}

def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Teste',
            'description': 'Nova descrição',
            'state': 'doing'
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': todo.id,
        'title': 'Teste',
        'description': 'Nova descrição',
        'state': 'doing'
    }

def test_patch_todo_error(client, token):
    response = client.patch(f'/todos/{10}', json={}, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}