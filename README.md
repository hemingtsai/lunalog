# Lunalog

## Brief

This is a part of *Project Luna*.

It's a simple blog system based Python and FastAPI.

Frontend: [Lunapages](https://github.com/hemingtsai/lunapages)

## Technology Stack

|Item|Software|
|-----------|---------------|
|Programming Language|Python|
|Backend Framework|FastAPI|

We don't use any database system, we use filesystem and json to save blog data.

## How to use?

First, you should create a `config/config.json` file, it can help you configure lunalog.

It should looks like this.

```text
{
	"blog_repo":"...",
	"github_webhook_secret":"...",
	"cors_allow_origin": "..."
}
```

Your blog repo should looks like this.

```test
.
├── posts
│   └── hello_world.md
└── posts.json
```
