from fastapi import APIRouter, Depends, HTTPException, status


async def get_posts_by_tag(tag_name: str):
    # Пошук постів за тегом
    matching_posts = []
    for post in ImageRepository:
        if tag_name in post.tags:
            matching_posts.append(post)
    
    if not matching_posts:
        raise HTTPException(status_code=404, detail=f"Пости з тегом '{tag_name}' не знайдені")
    
    return matching_posts