import { useState, useRef, useContext } from "react";
import { useHistory } from "react-router-dom";

import AuthContext from "../../store/auth-context";
import classes from "./AuthForm.module.css";
import styles from "../common/errors.css";

const signupURL = "http://localhost:3000/signup";
const loginURL = "http://localhost:3000/login";

const AuthForm = () => {
  const nameInputRef = useRef();
  const emailInputRef = useRef();
  const passwordInputRef = useRef();
  const companyInputRef = useRef();
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const switchAuthModeHandler = () => {
    setIsLogin((prevState) => !prevState);
  };

  const submitHandler = async (event) => {
    event.preventDefault();

    let enteredName;
    let enteredEmail;
    let enteredPassword;
    let enteredCompanyName;

    if (nameInputRef.current) {
      enteredName = nameInputRef.current.value;
    }
    if (emailInputRef.current) {
      enteredEmail = emailInputRef.current.value;
    }
    if (passwordInputRef.current) {
      enteredPassword = passwordInputRef.current.value;
    }
    if (companyInputRef.current) {
      enteredCompanyName = companyInputRef.current.value;
    }

    // optional: Add validation
    setLoading(true);

    let message = "";
    let url;
    let body;
    if (isLogin) {
      url = loginURL;
      message = "Login";
      body = { email: enteredEmail, password: enteredPassword };
    } else {
      url = signupURL;
      message = "Signup";
      body = {
        name: enteredName,
        email: enteredEmail,
        password: enteredPassword,
        companyName: enteredCompanyName,
      };
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Parse response data
      const data = await response.json();
      console.log(data);
      setLoading(false);

      if (!response.ok) {
        console.log("Response status: " + response.status);
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        // Mark success message and exit after timeout
        console.log(message + " successful!");
        if ("token" in data) {
          authCtx.login(data.token);
          history.replace("/");
        }
      }
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className={classes.center}>
      <section className={classes.auth}>
        <h1>{isLogin ? "Login" : "Sign Up"}</h1>
        <form onSubmit={submitHandler}>
          {!isLogin && (
            <div className={classes.control}>
              <label htmlFor="name">Name</label>
              <input type="name" id="name" required ref={nameInputRef} />
            </div>
          )}
          <div className={classes.control}>
            <label htmlFor="email">Email</label>
            <input type="email" id="email" required ref={emailInputRef} />
          </div>
          <div className={classes.control}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              required
              ref={passwordInputRef}
            />
          </div>
          {!isLogin && (
            <div className={classes.control}>
              <label htmlFor="company">Company</label>
              <input type="company" id="company" ref={companyInputRef} />
            </div>
          )}
          <div className={classes.actions}>
            {!loading && (
              <button>{isLogin ? "Login" : "Create Account"}</button>
            )}
            {loading && <p>Sending request...</p>}
            <button
              type="button"
              className={classes.toggle}
              onClick={switchAuthModeHandler}
            >
              {isLogin ? "Create new account" : "Login with existing account"}
            </button>
          </div>
        </form>
        <div className={styles.error_text}>{error}</div>
      </section>
    </div>
  );
};

export default AuthForm;
