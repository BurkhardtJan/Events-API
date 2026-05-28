from models import User
def test_user_password_hashing_behaves_correctly():
    """Check the password hashing works correctly."""
    user = User(username="test")
    user.set_password("mypassword123")
    assert user.check_password("mypassword123") == True
    assert user.check_password("notmypassword123") == False
    assert user.password_hash != "mypassword123"

def test_false():
    assert False