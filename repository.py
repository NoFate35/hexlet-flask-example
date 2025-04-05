import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum

from faker import Faker
from flask import session

SEED = 1234


class CommentStatus(Enum):
    WAITING = "waiting"
    APPROVED = "approved"
    REJECTED = "rejected"

    def __str__(self):
        return self.value


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


@dataclass
class Comment:
    post_id: uuid.UUID
    text: str
    id: uuid.UUID = None
    status: CommentStatus = CommentStatus.WAITING
    created_at: datetime = datetime.now()

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()


class Repository:
    def _init_storage(self):
        if "posts" not in session:
            session["posts"] = []
        if "comments" not in session:
            session["comments"] = []

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

    def save_comment(self, comment):
        self._init_storage()
        comment_dict = asdict(comment)
        comment_dict["id"] = str(comment.id)
        comment_dict["post_id"] = str(comment.post_id)
        comment_dict["created_at"] = comment.created_at.isoformat()
        comment_dict["status"] = str(comment.status)

        comment_index = None
        for i, existing in enumerate(session["comments"]):
            if existing["id"] == comment_dict["id"]:
                comment_index = i
                break

        if comment_index is not None:
            session["comments"][comment_index] = comment_dict
        else:
            session["comments"].append(comment_dict)

    def get_comments_by_post(self, post_id):
        self._init_storage()
        post_id_str = str(post_id)
        comments = []
        for comment_dict in session["comments"]:
            if comment_dict["post_id"] == post_id_str:
                comment = Comment(
                    post_id=uuid.UUID(comment_dict["post_id"]),
                    text=comment_dict["text"],
                    id=uuid.UUID(comment_dict["id"]),
                    status=CommentStatus(comment_dict["status"]),
                    created_at=datetime.fromisoformat(comment_dict["created_at"]),
                )
                if comment.status == CommentStatus.APPROVED:
                    comments.append(comment)
        return comments

    def get_comment(self, comment_id):
        self._init_storage()
        comment_id_str = str(comment_id)
        for comment_dict in session["comments"]:
            if comment_dict["id"] == comment_id_str:
                return Comment(
                    post_id=uuid.UUID(comment_dict["post_id"]),
                    text=comment_dict["text"],
                    id=uuid.UUID(comment_dict["id"]),
                    status=CommentStatus(comment_dict["status"]),
                    created_at=datetime.fromisoformat(comment_dict["created_at"]),
                )
        return None

    def get_waiting_comments(self):
        self._init_storage()
        waiting = []
        for comment_dict in session["comments"]:
            if comment_dict["status"] == str(CommentStatus.WAITING):
                comment = Comment(
                    post_id=uuid.UUID(comment_dict["post_id"]),
                    text=comment_dict["text"],
                    id=uuid.UUID(comment_dict["id"]),
                    status=CommentStatus.WAITING,
                    created_at=datetime.fromisoformat(comment_dict["created_at"]),
                )
                waiting.append(comment)
        return waiting


ids = [
    "1de9ea66-70d3-4a1f-8735-df5ef7697fb9",
    "f149f542-e935-4870-9734-6b4501eaf614",
    "08f0ebd4-950c-4dd9-8e97-b5bdf073eed1",
    "19322fed-157c-49c6-b16e-2d5cabeb9592",
]


def generate_posts(repo, count):
    fake = Faker()
    fake.seed_instance(SEED)
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            content=fake.text(),
            author_id=fake.random_int(),
            id=ids[i],
            created_at=datetime.now(),
        )
        repo.save_post(post)
