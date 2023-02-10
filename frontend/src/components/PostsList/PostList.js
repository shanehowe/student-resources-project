import { useAuth } from "../AuthProvider"
import { NoPostsYet } from "../NoPostsYet/NoPostsYet";
import { ResourcePost } from "../ResourcePost/ResourcePost";

export function PostsList({ posts, removePost }) {
    const auth = useAuth();
    if (posts.length === 0) {
        return <NoPostsYet />
    }
    return (
         <div className="posts-container">
            {posts.map((post) => {
                return <ResourcePost key={post._id} post={post} user={auth.user} handleDelete={removePost} />
            })}
        </div>
    )
}