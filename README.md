# [Memento](https://memento.onrender.com/) <span><img align="right" width="32px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg"/><span> </span><img align="right" width="32px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"/></span>

The project is available online at [https://Memento.onrender.com](https://memento.onrender.com/)

![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Table of contents

- [Using Technologies](#using-technologies)
- [Description](#description)
- [Project Installation](#project-installation)
- [Implementation](#implementation)
  - [API routes](#api-routes)
  - [Server side rendering](#server-side-rendering)
  - [Chat](#chat)
- [Information for Developers](#information-for-developers)
- [License](#license)
  - [MIT License](#mit-license)

## Using Technologies

![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.3-blue.svg)
![asyncio](https://img.shields.io/badge/asyncio-included-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.20-blue.svg)
![Alembic](https://img.shields.io/badge/Alembic-1.7.3-blue.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)
![Redis](https://img.shields.io/badge/Database-Redis-red.svg)

## Description

Our program provides the user with the ability to upload, edit and delete images. There is a convenient tag system that allows you to narrow your search according to your interests. It is possible to comment on the image. There is also a rating system based on user ratings. In short, everything you need to save and share memories.

## Project Installation

To manage project dependencies, `pipenv` is used.

- Make sure you have `pipenv` installed
- Clone the repository `git clone https://github.com/NightSpring1/InstaLike_PhotoSharing`
- To install the dependencies, use the `pipenv install` or `pipenv sync` command.

Detailed steps in your terminal a following:

```bash
$ git clone https://github.com/NightSpring1/InstaLike_PhotoSharing
$ cd InstaLike_PhotoSharing
$ pipenv install
$ python main.py
```

## Implementation

Once the application is running _locally_, you can browse to run it on your local host using the following links[^1]:

- To view detailed information on our project [http://localhost:8000/views/info](http://localhost:8000/views/info)
- To view detailed information on our project in `JSON` format [http://localhost:8000/](http://localhost:8000)
- To test the connection to the database and server time information [http://localhost:8000/api/healthchecker](http://localhost:8000/api/healthchecker)

For comfortable viewing of `JSON` respone in your browser we recommend to install the extension for Google Chrome
[JSON Viewer](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh/related?hl=ru) or
[JSON Formatter](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=ru) (according to your taste)

### API routes

The main task of the project was to implement a REST API, which plays a key role in ensuring effective interaction between interface developers (React, View, Angular) and our service.

All documentation on interacting with our API is available at the following links:

- To view swagger documentation [http://localhost:8000/docs](http://localhost:8000/docs)
- To view redoc documentation [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Information for Developers

Our project is equipped with Sphinx documentation, which you can find at [https://github.com/NightSpring1/InstaLike_PhotoSharingExchange/](https://github.com/NightSpring1/InstaLike_PhotoSharingExchange/). The documentation may be useful to other developers who
can use it to develop our project.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

### MIT License

Copyright © [FastTrack Codes]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
