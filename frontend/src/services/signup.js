import axios from "axios";

const baseUrl = process.env.REACT_APP_SIGN_UP_URL;

const signUp = async (email, password, username, fullName) => {
    const user = {
        "email": email,
        "name": fullName,
        "password": password,
        "username": username
    }
    const response = await axios.post(baseUrl, user);
    return response.data;
}

const signUpService = { signUp }
export default signUpService