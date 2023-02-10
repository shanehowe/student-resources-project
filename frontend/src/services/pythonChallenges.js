import axios from "axios";

const baseUrl = process.env.REACT_APP_GET_CHALLENGES_URL;


export const getAll = async () => {
    const response = await axios.get(baseUrl);
    return response.data;
}