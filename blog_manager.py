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
        self.blog_data= json.loads(open(platform_data.post_json_path, "r",encoding="utf-8").read())
        self.posts_data: List[Dict[str, Any]] = self.blog_data["posts"]

    def get_post(self, post_id: int) -> Dict[str, Any]:
        result: str = ""

        try:
            with open(f"{platform_data.post_data_path}{platform_data.sep}{self.posts_data[post_id]['file']}", "r",encoding="utf-8") as post:
                for i in post.readlines():
                    result += i
        except:
            raise HTTPException(status_code=404, detail="Post not found")

        return {
                "title": self.posts_data[post_id]['title'],
                "time": {
                    "year": self.posts_data[post_id]["time"]["year"],
                    "month": self.posts_data[post_id]["time"]["month"],
                    "day": self.posts_data[post_id]["time"]["day"]
                },
                "content": result
            }

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
    
    def get_website_info(self) -> Dict[str, Any]:
        return {
            "title": self.blog_data["website_info"]["title"],
            "description": self.blog_data["website_info"]["description"],
        }
    
    def get_special_pages_list(self) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for i in self.blog_data["special_pages"]:
            result.append({
                "title": i["title"],
                "file": i["file"]
            })
        return result
    
    def get_special_page(self, index: int) -> Dict[str, Any]:
        return {
            "title": self.blog_data["special_pages"][index]["title"],
            "time": {
                "year": self.blog_data["special_pages"][index]["time"]["year"],
                "month": self.blog_data["special_pages"][index]["time"]["month"],
                "day": self.blog_data["special_pages"][index]["time"]["day"]
            },
            "content": open(f"{platform_data.special_pages_path}{platform_data.sep}{self.blog_data['special_pages'][index]['file']}", "r",encoding="utf-8").read()
        }
