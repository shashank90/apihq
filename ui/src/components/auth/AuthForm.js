import React, { useState, useRef, useContext } from "react";
import { useHistory } from "react-router-dom";

import AuthContext from "../../store/auth-context";
import classes from "./AuthForm.module.css";
import styles from "../common/errors.css";

const signupURL = "/signup";
const loginURL = "/login";

const AuthForm = () => {
  const nameInputRef = useRef();
  const emailInputRef = useRef();
  const passwordInputRef = useRef();
  const companyInputRef = useRef();
  const history = useHistory();

  const authCtx = useContext(AuthContext);

  const [isLogin, setIsLogin] = useState(true);
  const [agree, setAgree] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const switchAuthModeHandler = () => {
    if (error) {
      setError("");
    }
    setIsLogin((prevState) => !prevState);
  };

  const checkboxHandler = () => {
    // console.log("Toggle conditions checkbox");
    // if agree === true, it will be set to false
    // if agree === false, it will be set to true
    setAgree(!agree);
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
        agreeTerms: !agree,
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
        let successMsg = message + " successful!";
        console.log(successMsg);
        if ("token" in data && "expires_in" in data) {
          const expirationTime = new Date(
            new Date().getTime() + data.expires_in * 1000
          );
          authCtx.login(data.token, expirationTime.toISOString());
          history.replace("/");
        }
        // Signup successful
        if (!isLogin) {
          setMessage(successMsg);
          setIsLogin(true);
          setMessage("");
        }
      }
    } catch (error) {
      setError(error.message);
    }
  };

  let content = <div></div>;

  if (error) {
    content = <div className={styles.error_text}>{error}</div>;
  }
  if (message) {
    content = <div>{message}</div>;
  }

  return (
    <div className={classes.center}>
      <section className={classes.auth}>
        <h1>{isLogin ? "Login" : "Sign Up for free!"}</h1>
        <form onSubmit={submitHandler}>
          {!isLogin && (
            <div className={classes.control}>
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                required
                ref={nameInputRef}
                maxLength="40"
              />
            </div>
          )}
          <div className={classes.control}>
            <label htmlFor="email">Email</label>
            <input
              type="text"
              id="email"
              required
              ref={emailInputRef}
              maxLength="40"
            />
          </div>
          <div className={classes.control}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              required
              maxLength="40"
              ref={passwordInputRef}
            />
          </div>
          {!isLogin && (
            <React.Fragment>
              <div className={classes.control}>
                <label htmlFor="company">Company</label>
                <input
                  type="text"
                  id="company"
                  ref={companyInputRef}
                  maxLength="40"
                />
              </div>
              <div>
                <input
                  type="checkbox"
                  id="terms"
                  onChange={checkboxHandler}
                  required
                />
                <label htmlFor="terms" className={classes.termsLabel}>
                  I have read the terms under{"  "}
                  <a href="https://cymitra.com/faq" target="_blank">
                    FAQ
                  </a>
                </label>
              </div>
            </React.Fragment>
          )}
          {content}
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
      </section>
    </div>
  );
};

export default AuthForm;
