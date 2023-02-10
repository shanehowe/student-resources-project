import { useEffect, useState } from "react";
import AnimateHeight from 'react-animate-height';
import Proptypes from 'prop-types';

import "./ResourcePost.css";

export function ResourcePost({ post, user, handleDelete }) {
    const [toggle, setToggle] = useState(false);
    const [height, setHeight] = useState(0);
    const [postLength, setPostLength] = useState(0);

    useEffect(() => {
        if (post) {
            const cutOff = Math.floor(post.description.length / 4);
            setPostLength(cutOff);
        }
    }, [post]);

    const showMore = () => {
        setToggle(!toggle);
        setHeight(height === 0 ? 'auto' : 0);
    };

    return (

        <div className="post-container" key={post._id}>
            <div className="title-and-button">
                <p>{post.title}</p> <button onClick={showMore}>{!toggle ? "Show" : "Hide"}</button>
            </div>
            <div className="post-description">
                <p>{toggle ? post.description : post.description.substring(0, postLength) + "..."}</p>
            </div>
            <AnimateHeight className="full-width" duration={500} height={height}>
                {toggle &&
                    <>
                        <div className="post-url">
                            <p>
                                Url: <a className="post-link" target="_blank" rel="noopener noreferrer" href={post.url}>{post.url}</a>
                            </p>
                        </div>
                        <div className="post-user">
                            <p>Posted by: <span id="name">{post.user.username}</span></p>
                            {user.username === post.user.username && <button onClick={() => handleDelete(post._id, post)} id="delete-button">Delete</button>}
                        </div>
                    </>}
            </AnimateHeight>
        </div>
    );
}

ResourcePost.propTypes = {
    post: Proptypes.object.isRequired,
    user: Proptypes.object.isRequired,
    handleDelete: Proptypes.func.isRequired
}