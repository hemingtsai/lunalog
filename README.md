# Lunalog

## Brief

This is a part of *Project Luna*.

It's a modern blog system based Python and FastAPI.

***Warning***: It's only a backend. I like to call it "Blog System Core". You should compose a frontend website to use it.

## Technology Stack

|Item|Software|
|-----------|---------------|
|Programming Language|Python|
|Backend Framework|FastAPI|

We don't use any database system, we use filesystem and json to save blog data.

## How to use?

First, you should create a `.env` file, it can help you configure lunalog.

It should looks like this.

```text
BLOG_REPO="<your-blog-repo>"
```

Your blog repo should looks like this.

```test
.
├── posts
│   └── 2025
│       └── 1
│           └── 16.md
└── posts.json
```
