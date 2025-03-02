import os
from pathlib import Path
import json
from fastapi import HTTPException


class Post:
    def __init__(self, time: int, title: str, content: str):
        self.time = time
        self.title = title
        self.content = content

    time: int
    title: str
    content: str


class BlogManager():
    def __init__(self, config):

        self.config = config
        # Check data direoctry exists
        if not Path("./data").is_dir():
            os.mkdir("data")
        
        self.update_posts()

        # Open posts database
        self.posts_data = json.loads(open("./data/posts.json", "r").read())

    def update_posts(self):
        repo = self.config["blog_repo"]
        if not os.path.exists("data/.git"):
            os.system(f"git clone {repo} data")
        else:
            os.system(f"cd data; git pull; cd ..")

    def get_post(self, post_id: int):
        result: str = ""

        try:
            with open(f"./data/posts/{self.posts_data[post_id]['time']['year']}/{self.posts_data[post_id]['time']['month']}/{self.posts_data[post_id]['time']['day']}.md", "r") as post:
                for i in post.readlines():
                    result += i
        except:
            raise HTTPException(status_code=404, detail="Post not found")

        return result

    def get_post_list(self):
        result: list[dict] = []
        for i in self.posts_data:
            result.append({
                "title": i['title'],
                "time": {
                    "year": i["time"]["year"],
                    "month": i["time"]["month"],
                    "day": i["time"]["day"]
                }
            })
        return result
