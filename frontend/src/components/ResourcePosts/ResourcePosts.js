import { Navigation } from "../Navigation/Navigation"
import { useLocation, useNavigate } from "react-router-dom";
import { Heading } from "../Heading/Heading";
import { Notification } from "../Notification";
import { CreatePostForm } from "../CreatePostForm/CreatePostForm";
import { Togglable } from "../Togglable/Togglable"; 
import { PostsList } from "../PostsList/PostList";

import resourceServices from "../../services/resourcePosts";

import "./ResourcePosts.css";
import { useEffect, useState, useRef } from "react";



export function ResourcePosts({ notify, message, isError }) {
    const location = useLocation();
    
    const { moduleName } = location.state;
    const [title, setTitle] = useState("");
    const [description, setDescription]= useState("");
    const [url, setUrl] = useState("");
    const [posts, setPosts] = useState(null);
    useEffect(() => {
        resourceServices
            .getAll()
            .then(_posts => _posts = _posts.filter(p => p.moduleName === moduleName))
            .then(_posts => setPosts(_posts))
      }, [moduleName]);

    const navigate= useNavigate();
    const postFormRef = useRef();
    
    const handleTitleChange = ({ target }) => {
        setTitle(target.value);
    }

    const handleDescriptionChange = ({ target }) => {
        setDescription(target.value);
    }

    const handleUrlChange = ({ target }) => {
        setUrl(target.value);
    }

    const createNewPost = async (e) => {
        e.preventDefault();
        postFormRef.current.toggleVisibility();

        if (title.length > 30) {
            notify(`Title cannot be longer than 30 characters. Current length: ${title.length}`, true);
            return;
        }

        const postObject = {
            title: title,
            description: description,
            url: url,
            moduleName: moduleName,
            semester: Number(2), // Current semester
        }

        try {
            const post = await resourceServices.createPost(postObject);
            setPosts(posts.concat(post));
            setTitle("");
            setUrl("");
            setDescription("");
            notify(`New post ${post.title} created!`)
        } catch (error) {
            if (error.response.data.detail === "token has expired") {
                notify("Your session has expired. Log back in to continue", true);
                navigate("/login", {replace: true});
            } else {
                notify("An unexpected error occured. Try again later")
            }

        }
    }

    const removePost = async (id, postObj) => {
        if (window.confirm(`Delete ${postObj.title}?`)) {
            try {
                await resourceServices.deletePost(id);
                setPosts(posts.filter((p) => p._id !== id));
                notify("Post successfully deleted", false);
            } catch (error) {
                if (error.response.data.detail === "token has expired") {
                    notify("Your session has expired. Log back in to continue", true);
                    navigate("/login", {replace: true});
                }
            }
        }  
    }
    return (
        <>
        <Navigation/>
        <Heading message={"Posts for " + moduleName}/>
        {message && <div className="notifcation-section">
            <div className="notification-container">
                <Notification message={message} isError={isError}/>
            </div>
        </div>}
        
        <Togglable buttonLabel={"New Post"} ref={postFormRef}>
        <CreatePostForm 
            createNewPost={createNewPost} 
            title={title} 
            handleTitleChange={handleTitleChange}
            description={description}
            handleDescriptionChange={handleDescriptionChange}
            url={url}
            handleUrlChange={handleUrlChange}
            moduleName={moduleName}
            />
        </Togglable>
        {posts === null ? <h3 style={{textAlign: "center"}} >Loading...</h3>: <PostsList posts={posts} removePost={removePost} />}
        
        
        </>
    )
}