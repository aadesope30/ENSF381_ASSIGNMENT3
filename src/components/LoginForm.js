import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DisplayStatus from "./DisplayStatus";

const USERS_API = "https://jsonplaceholder.typicode.com/users";

function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [shouldFetch, setShouldFetch] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!shouldFetch) {
      return;
    }

    let ignore = false;

    const validateLogin = async () => {
      try {
        const response = await fetch(USERS_API);

        if (!response.ok) {
          throw new Error("Unable to reach login service.");
        }

        const users = await response.json();

        const matchedUser = users.find(
          (user) => user.username === username && user.email === password
        );

        if (ignore) {
          return;
        }

        if (matchedUser) {
          setMessage("Login successful");
          setMessageType("success");
        } else {
          setMessage("Invalid username or password.");
          setMessageType("error");
        }
      } catch (error) {
        if (!ignore) {
          setMessage(error.message || "Something went wrong. Please try again.");
          setMessageType("error");
        }
      } finally {
        if (!ignore) {
          setShouldFetch(false);
        }
      }
    };

    validateLogin();

    return () => {
      ignore = true;
    };
  }, [shouldFetch, username, password]);

  useEffect(() => {
    if (messageType !== "success") {
      return undefined;
    }

    const timer = setTimeout(() => {
      navigate("/flavors");
    }, 2000);

    return () => clearTimeout(timer);
  }, [messageType, navigate]);

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedUsername = username.trim();
    const trimmedPassword = password.trim();

    if (!trimmedUsername || !trimmedPassword) {
      setMessage("Username and password cannot be empty.");
      setMessageType("error");
      return;
    }

    if (trimmedPassword.length < 8) {
      setMessage("Password must be at least 8 characters.");
      setMessageType("error");
      return;
    }

    setUsername(trimmedUsername);
    setPassword(trimmedPassword);
    setMessage("");
    setMessageType("");
    setShouldFetch(true);
  };

  return (
    <div className="content login-wrapper">
      <form onSubmit={handleSubmit}>
        <h2>Login</h2>

        <div className="form-row">
          <label htmlFor="username">Username </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
        </div>

        <br/>

        <div className="form-row">
          <label htmlFor="password">Password </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        <button type="submit">Login</button>
        
        <br />
        
        <a href ="#">Forgot Password?</a>

        {message && <DisplayStatus type={messageType} message={message} />}
      </form>
    </div>
  );
}

export default LoginForm;