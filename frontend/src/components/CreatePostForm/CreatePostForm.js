import Proptypes from 'prop-types';
import "./CreatePostForm.css";

export function CreatePostForm({
    createNewPost, title, handleTitleChange, description, handleDescriptionChange, url, handleUrlChange, moduleName
}) {

    return (
        <>
            <div className="form-container">
                <form onSubmit={createNewPost}>
                    <div>
                        Title<br /> <input type="text" value={title} onChange={handleTitleChange} required />
                    </div>
                    <div>
                        Description<br /> <textarea value={description} onChange={handleDescriptionChange} required />
                    </div>
                    <div>
                        Url<br /> <input value={url} onChange={handleUrlChange} required />
                    </div>
                    <div>
                        Module Name<br /> <input defaultValue={moduleName} required />
                    </div>
                    <button id="create-post-button" type="submit">Create Post</button>
                </form>
            </div>
        </>
    );
}

CreatePostForm.propTypes = {
    createNewPost: Proptypes.func.isRequired,
    title: Proptypes.string.isRequired,
    handleTitleChange: Proptypes.func.isRequired,
    description: Proptypes.string.isRequired,
    handleDescriptionChange: Proptypes.func.isRequired,
    url: Proptypes.string.isRequired,
    handleUrlChange: Proptypes.func.isRequired,
    moduleName: Proptypes.string.isRequired
}