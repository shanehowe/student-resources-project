import axios from "axios";
const baseUrl = process.env.REACT_APP_RESOURCES_URL;

let token = null;

const setToken = (newToken) => {
    token = `bearer ${newToken}`;
}

const getAll = async () => {
    const request = axios.get(baseUrl);
    const response = await request;
    return response.data;
}

const getOne = async (id) => {
    const request = axios.get(`${baseUrl}/${id}`);
    const response = await request;
    return response.data;
}

const createPost = async (newObject) => {
    const config = {
        headers: { Authorization: token },
    }
    const request = axios.post(baseUrl, newObject, config);
    const response = await request;
    return response.data;
}

const updatePost = async (id, newObject) => {
    const config = {
        headers: { Authorization: token },
    }
    const request = axios.put(`${baseUrl}/${id}`, newObject, config);
    const response = await request;
    return response.data;
}

const deletePost = async (id) => {
    const config = {
        headers: { Authorization: token }
    }
    const request = axios.delete(`${baseUrl}/${id}`, config);
    const response = await request;
    return response.data;
}

const resourceServices = { getAll, getOne, setToken, createPost, updatePost, deletePost }
export default resourceServices
