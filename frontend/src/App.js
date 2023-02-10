import { useEffect, useState } from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import { LoginForm } from "./components/LoginForm";
import { SignupForm } from "./components/SignupForm";
import { ResourceCenter } from "./components/ResourceCenter";
import { ResourcePosts } from "./components/ResourcePosts/ResourcePosts";
import { HomePage } from "./components/HomePage/HomePage";
import { NotFound } from "./components/NotFound/NotFound";
import { PythonChallenges } from "./components/PythonChallengs/PythonChallenges";
import { AuthProvider, useAuth } from "./components/AuthProvider";
import { getAll } from "./services/pythonChallenges";

function RequireAuth({ children }){
  let auth = useAuth();

  if (!auth.user) {
    return <Navigate to="/login" replace />
  }
  return children;
}

function App() { 
  const [message, setMessage] = useState(null);
  const [isError, setIsError] = useState(false);
  const [challenge, setChallenge] = useState(null);
  const [challenges, setChallenges] = useState([]);

  useEffect(() => {
    async function getChallenges() {
      try {
        const challenges_ = await getAll();
        setChallenges(challenges_);
      } catch (error) {
        console.error(error)
      }
    }
    getChallenges();
  }, [])

  const handleSettingChallenge = (challenge) => {
    setChallenge(challenge);
  }


  const notify = (msg, isAnError) => {
    setMessage(msg);
    setIsError(isAnError);

    setTimeout(() => {
      setMessage(null);
      setIsError(false);
    }, 5000);
  }

  return (
    <AuthProvider>        
      <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login/" 
          element={<LoginForm 
                        message={message}
                        isError={isError}
                        notify={notify}
                        />} />
          <Route path="/signup/" 
          element={<SignupForm 
                        message={message}
                        isError={isError}
                        notify={notify}
                        />} />
          <Route path="/resource-center" 
          element={
            <RequireAuth>
              <ResourceCenter />
            </RequireAuth> } />
          <Route path="/resource-center/:moduleName" 
          element={
            <RequireAuth>
              <ResourcePosts 
                notify={notify} 
                message={message} 
                isError={isError}/>
            </RequireAuth>}/>
          <Route path="/python-challenges" 
            element={
              <RequireAuth>
                <PythonChallenges 
                  challenges={challenges}
                  challenge={challenge}
                  handleSettingChallenge={handleSettingChallenge}
                  notify={notify}
                />
              </RequireAuth>} />
            <Route path="*" element={ 
              <RequireAuth>
                <NotFound/>
              </RequireAuth> } />
      </Routes>
    </AuthProvider>
  );
}

export default App;
