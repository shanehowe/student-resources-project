import axios from "axios";

const baseUrl = process.env.REACT_APP_LOGIN_URL;

const login = async (username, password) => {
    const response = await axios.post(baseUrl, { username, password });
    return response.data;
}

const loginService = { login }
export default loginService;