from unittest import TestCase

from app import app
from models import db, User, Post

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test_db"
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class PostTestCase(TestCase):
    """Test for views for Post"""

    def setUp(self):
        """Add sample user & post"""
        Post.query.delete()
        User.query.delete()

        user = User(id=1, first_name="Lacey", last_name="grace", img_url="")
        db.session.add(user)
        db.session.commit()

        post = Post(
            title="Spotted a UFO",
            content="On July 15, 1997 I saw, and was abducted by, a UFO",
            user_id=1,
        )

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up an db for each test"""

        db.session.rollback()

    def test_if_post_listed_details_page(self):
        """Check if all of any given users post are listed on their individual user-details page"""
        with app.test_client() as client:
            resp = client.get(f"/user-details/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<a href="/user-details/{self.user_id}/{self.post_id}" class="list-group-item list-group-item-action">Spotted a UFO</a>',
                html,
            )

    def test_edit_post_form(self):
        """Check if user is brought to the correct edit-post form"""
        with app.test_client() as client:
            resp = client.get(f"/user-details/{self.user_id}/{self.post_id}/edit-post")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="content">Post Content</label>', html)

    def test_edit_post_form_submission(self):
        """Test if passed in post-edit form information is added to the db and that the post page is updated properly"""
        with app.test_client() as client:
            data = {
                "title": "New cat",
                "content": "This is sally the cat",
                "user_id": 1,
            }
            resp = client.post(
                f"/user-details/{self.user_id}/{self.post_id}/edit-post",
                data=data,
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="form-group">This is sally the cat</p>', html)

    def test_delete_post(self):
        """Check if deletion is successful"""
        with app.test_client() as client:
            resp = client.get(
                f"/user-details/{self.user_id}/{self.post_id}/delete-post",
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Spotted a UFO", html)
