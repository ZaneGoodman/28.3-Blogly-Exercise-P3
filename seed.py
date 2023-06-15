from models import User, Post, Tag, PostTag, db
from app import app


db.drop_all()
db.create_all()


User.query.delete()

# Add users
john = User(
    first_name="John",
    last_name="Wintenburg",
    img_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80",
)

sally = User(
    first_name="Sally",
    last_name="Clara",
    img_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
)

fredrick = User(
    first_name="Fredrick",
    last_name="Geress",
    img_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
)
zane = User(
    first_name="zane",
    last_name="goodman",
    img_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80",
)

lexi = User(
    first_name="lexi",
    last_name="rossi",
    img_url="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
)

fred = User(
    first_name="fred",
    last_name="homes",
    img_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80",
)

p1 = Post(
    title="New cat",
    content="This is sally the cat",
    user_id=1,
    tags=[Tag(tag_name="Love"), Tag(tag_name="Happy"), Tag(tag_name="WTF")],
)

p2 = Post(
    title="Selling my car",
    content="I'm going on a 1 year camping trip!",
    user_id=2,
    tags=[Tag(tag_name="Seriously"), Tag(tag_name="Angry"), Tag(tag_name="Meme")],
)

p3 = Post(
    title="Uber",
    content="I'm starting to uber. Text me for details",
    user_id=3,
    tags=[Tag(tag_name="Yes!"), Tag(tag_name="Yall")],
)

p4 = Post(
    title="Selling house", content="This is what I learned about home owning", user_id=4
)
p5 = Post(title="Eating green", content="Why you shouldnt be a vegan", user_id=5)
p6 = Post(title="No animals", content="A list of reasons not to get a pet", user_id=6)
p7 = Post(
    title="Honda ridgeline",
    content="Reasons why the new honda truck is the most reliable",
    user_id=1,
)
p8 = Post(
    title="Touch grass",
    content="New study shows most kids don't know what grass feels like",
    user_id=2,
)
p9 = Post(
    title="Television's destruction",
    content="Just as candy does to your teeth, Tv does to your brain",
    user_id=3,
)
p10 = Post(title="Hot rod central", content="Look at this 1967 Shelby", user_id=1)
p11 = Post(
    title="Eating only bugs",
    content="Why the world economic forum wants to be a world dominating evil superpower, 'comply or die!'",
    user_id=4,
)
p12 = Post(
    title="Laugh out loud",
    content="The creation of english shorthands, are we dumber now?",
    user_id=5,
)


db.session.add_all([john, sally, fredrick, zane, lexi, fred])
db.session.commit()

db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])
db.session.commit()
