import sys

if sys.platform == "win32":
    update_posts = "cd data && git pull && cd .."
    data_path = ".\\data"
    post_json_path = ".\\data\\posts.json"
    post_data_path = ".\\data\\posts"
    sep="\\"
else:
    update_posts = "cd data; git pull; cd .."
    data_path = "./data"
    post_json_path = "./data/posts.json"
    post_data_path = "./data/posts"
    sep="/"