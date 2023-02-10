from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import JSONResponse
from utils.JWTHelper import JwtHelper
from models.user import PyObjectId, UserOut
from models.resource_posts import ResourcePostIn, ResourcePostOut, UpdateResourcePost
from database.database import database
from utils import url_validator


resource_router = APIRouter()

@resource_router.get("/api/resources", response_model=None)
def get_all_posts() -> list[ResourcePostOut]:
    resource_collection = database.db.get_collection("resourcePosts")
    user_collection = database.db.get_collection("users")
    posts = []
    for post in resource_collection.find({}):
        post["user"] = user_collection.find_one({"_id": post["user"]})
        posts.append(ResourcePostOut(**post))

    return posts


@resource_router.get("/api/resources/{id}", response_model=None)
def get_post_by_id(id: PyObjectId) -> ResourcePostOut:
    resource_coll = database.db.get_collection("resourcePosts")
    user_coll = database.db.get_collection("users")
    post = resource_coll.find_one({"_id": id})

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    
    post["user"] = user_coll.find_one({"_id": post["user"]})
    return ResourcePostOut(**post)


@resource_router.post("/api/resources", status_code=status.HTTP_201_CREATED, response_model=None)
def create_post(request: Request, post: ResourcePostIn) -> ResourcePostOut:
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token"
        )
    
    token_data = JwtHelper.decode_token(token[7:])
    user_coll = database.db.get_collection("users")
    user = user_coll.find_one({"_id": PyObjectId(token_data["id"])})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only users are permitted to do this action"
        )
    
    post.url = url_validator.add_https_to_url(post.url)
    
    resource_coll = database.db.get_collection("resourcePosts")
    post.user = user["_id"]
    created_postid = resource_coll.insert_one(post.dict()).inserted_id

    user_coll.update_one(
        {"_id": user["_id"]}, {"$push": {"resourcePosts": created_postid}}
        )
    
    created_resource = resource_coll.find_one({"_id": created_postid})
    created_resource["user"] = user # type: ignore
    return ResourcePostOut(**created_resource) # type: ignore
    

@resource_router.put("/api/resources/{id}", status_code=status.HTTP_200_OK, response_model=None)
def update_post(id: PyObjectId, request: Request, post: UpdateResourcePost) -> ResourcePostOut:
    user_coll = database.db.get_collection("users")
    resource_coll = database.db.get_collection("resourcePosts")
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token"
        )

    token_data = JwtHelper.decode_token(token[7:]) 
    user = user_coll.find_one({"_id": PyObjectId(token_data["id"])})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only users are permitted to do this action"
        )
    
    post_to_update = resource_coll.find_one({"_id": PyObjectId(id)})
    if not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="post does not exist"
        )
    user_model = UserOut(**user)
    post_model = ResourcePostOut(**post_to_update)
    if user_model.id != post_model.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This action is only allowed by the owner of the post"
        )
    
    document = {k: v for k, v in post.dict().items() if v}
    result = resource_coll.update_one(
        {"_id": post_to_update["_id"]}, {"$set": document}
        )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing to update"
        )
    updated_post = resource_coll.find_one({"_id": post_to_update["_id"]})
    updated_post["user"] = user # type: ignore
    return ResourcePostOut(**updated_post) # type: ignore


@resource_router.delete("/api/resources/{id}", status_code=status.HTTP_200_OK, response_model=None)
def delete_post(id: PyObjectId, request: Request) -> JSONResponse:
    user_coll = database.db.get_collection("users")
    resource_coll = database.db.get_collection("resourcePosts")
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token"
        )

    token_data = JwtHelper.decode_token(token[7:])
    user = user_coll.find_one({"_id": PyObjectId(token_data["id"])})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only users are permitted to do this action"
        )
    
    post_to_delete = resource_coll.find_one({"_id": PyObjectId(id)})
    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="post does not exist"
        )
    user_model = UserOut(**user)
    post_model = ResourcePostOut(**post_to_delete)
    if user_model.id != post_model.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This action is only allowed by the owner of the post"
        )
    
    result = resource_coll.delete_one({"_id": post_to_delete["_id"]})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing to delete"
        )
    # Remove post from user's resourcePosts array
    user_coll.update_one(
        {"_id": user["_id"]}, {"$pull": {"resourcePosts": post_to_delete["_id"]}}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": "Post deleted successfully"}
        )