from unittest import TestCase

from app import app
from models import db, User

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test_db"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Test for views for Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(
            first_name="Lacey",
            last_name="grace",
            img_url="https://images.pexels.com/photos/2773977/pexels-photo-2773977.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        )
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up an db for each test"""

        db.session.rollback()

    def test_user_details(self):
        """Check that Porper user info is displayed on details page"""
        with app.test_client() as client:
            resp = client.get(f"/user-details/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 id="details-name" class="form-group">Lacey grace</h1>', html
            )

    def test_edit_user(self):
        """Test route that takes user to an editing form"""
        with app.test_client() as client:
            resp = client.get(f"/user-details/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<label for='first_name'>First Name</label>", html)

    def test_user_edit_form(self):
        """Check if new information passed into user-edit form is properly added to the db and displayed on the updated user details page"""
        with app.test_client() as client:
            data = {
                "first_name": "Sally",
                "last_name": "brooks",
                "img_url": "https://images.pexels.com/photos/634021/pexels-photo-634021.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            }
            resp = client.post(
                f"/user-details/{self.user_id}/edit", data=data, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 id="details-name" class="form-group">Sally brooks</h1>', html
            )

    def test_delete_user(self):
        """Check if deletion is successful"""
        with app.test_client() as client:
            resp = client.get(
                f"/user-details/{self.user_id}/delete", follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Lacey", html)
