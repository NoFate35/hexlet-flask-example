import uuid
from dataclasses import asdict, dataclass
from datetime import datetime

from faker import Faker
from flask import session

SEED = 1234


@dataclass
class Post:
    title: str
    content: str
    author_id: int
    id: uuid.UUID = None
    created_at: datetime = datetime.now()

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()


class Repository:
    def _init_storage(self):
        if "posts" not in session:
            session["posts"] = []

    def save_post(self, post):
        self._init_storage()
        post_dict = asdict(post)
        post_dict["id"] = str(post.id)
        post_dict["created_at"] = post.created_at.isoformat()
        session["posts"].append(post_dict)

    def get_post(self, post_id):
        self._init_storage()
        post_id_str = str(post_id)
        for post_dict in session["posts"]:
            if post_dict["id"] == post_id_str:
                return Post(
                    title=post_dict["title"],
                    content=post_dict["content"],
                    author_id=post_dict["author_id"],
                    id=uuid.UUID(post_dict["id"]),
                    created_at=datetime.fromisoformat(post_dict["created_at"]),
                )
        return None

    def get_all_posts(self):
        self._init_storage()
        posts = []
        for post_dict in session["posts"]:
            post = Post(
                title=post_dict["title"],
                content=post_dict["content"],
                author_id=post_dict["author_id"],
                id=uuid.UUID(post_dict["id"]),
                created_at=datetime.fromisoformat(post_dict["created_at"]),
            )
            posts.append(post)
        return sorted(posts, key=lambda p: p.created_at, reverse=True)

    def search_posts(self, term):
        term = term.lower()
        matching_posts = []

        for post_dict in session.get("posts", []):
            if term in post_dict["title"].lower():
                post = Post(
                    title=post_dict["title"],
                    content=post_dict["content"],
                    author_id=post_dict["author_id"],
                    id=uuid.UUID(post_dict["id"]),
                    created_at=datetime.fromisoformat(post_dict["created_at"]),
                )
                matching_posts.append(post)

        return matching_posts


fake = Faker()

word_list = fake.words(30)


def generate_posts(repo, count):
    fake.seed_instance(SEED)
    for i in range(count - 3):
        post = Post(
            title=fake.sentence(ext_word_list=word_list),
            content=fake.text(),
            author_id=fake.random_int(),
            id=fake.uuid4(),
            created_at=datetime.now(),
        )
        repo.save_post(post)
    for i in range(3):
        post = Post(
            title=fake.sentence(ext_word_list=word_list).replace(".", " foobar."),
            content=fake.text(),
            author_id=fake.random_int(),
            id=fake.uuid4(),
            created_at=datetime.now(),
        )
        repo.save_post(post)
