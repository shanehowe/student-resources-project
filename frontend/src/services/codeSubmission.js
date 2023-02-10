import axios from "axios"

const baseUrl = process.env.REACT_APP_CHALLENGES_URL;

let token = null;

const setToken = (newToken) => {
    token = `bearer ${newToken}`;
}

const submitCode = async (sourceCode, functionName) => {
    const config = {
        headers: { Authorization: token },
    }
    const response = await axios.post(`${baseUrl}/code-submission`, {sourceCode, functionName}, config);
    return response.data;
}

const runCodeWithSampleInput = async (sourceCode, functionName, sampleInput) => {
    const config = {
        headers: { Authorization: token },
    }
    const response = await axios.post(`${baseUrl}/sampleInput`, {sourceCode, functionName, sampleInput}, config)
    return response.data;
}


const codeServices = { setToken, submitCode, runCodeWithSampleInput }

export default codeServices;