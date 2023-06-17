from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

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
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
        PostTag.query.delete()
        user = User(id=1, first_name="Lacey", last_name="grace", img_url="")

        db.session.add(user)
        db.session.commit()

        tag = Tag(tag_name="happy")
        post = Post(
            title="Spotted a UFO",
            content="On July 15, 1997 I saw, and was abducted by, a UFO",
            user_id=1,
        )

        post.tags.append(tag)
        db.session.add(post)
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.tag_id
        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up an db for each test"""

        db.session.rollback()

    def test_if_new_tag_added(self):
        """Check if new tag was added to tag list from form data"""
        data = {"tag_name": "sad"}
        with app.test_client() as client:
            resp = client.post("/tags/add-tag", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<a href="/tags/4" class="list-group-item list-group-item-action">sad</a>',
                html,
            )

    def test_if_edited_tag_added(self):
        """Check if tag was updated by edited info from form data"""
        data = {"tag_name": "angry"}
        with app.test_client() as client:
            resp = client.post(
                f"/tags/{self.tag_id}/edit", data=data, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<a href="/tags/{self.tag_id}" class="list-group-item list-group-item-action">angry</a>',
                html,
            )

    def test_delete_post(self):
        """Check if deletion is successful"""
        with app.test_client() as client:
            resp = client.get(
                f"/tags/{self.tag_id}/delete-tag",
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("happy", html)
