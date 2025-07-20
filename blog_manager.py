import os
from pathlib import Path
import json
from fastapi import HTTPException
from typing import List, Dict, Any
import platform_data


class Post:
    def __init__(self, time: int, title: str, content: str):
        self.time: int = time
        self.title: str = title
        self.content: str = content

class BlogManager:
    def __init__(self, config: Dict[str, Any]):
        self.config: Dict[str, Any] = config
        # Check data direoctry exists
        if not Path(platform_data.data_path).is_dir():
            os.mkdir("data")
        
        self.update_posts()


    def update_posts(self) -> None:
        repo: str = self.config["blog_repo"]
        if not os.path.exists(Path(platform_data.data_path).joinpath(".git")):
            os.system(f"git clone {repo} data")
        else:
            os.system(platform_data.update_posts)
        self.posts_data: List[Dict[str, Any]] = json.loads(open(platform_data.post_json_path, "r",encoding="utf-8").read())

    def get_post(self, post_id: int) -> str:
        result: str = ""

        try:
            with open(f"{platform_data.post_data_path}{platform_data.sep}{self.posts_data[post_id]['file']}", "r",encoding="utf-8") as post:
                for i in post.readlines():
                    result += i
        except:
            raise HTTPException(status_code=404, detail="Post not found")

        return result

    def get_post_list(self) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
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
