// Store of all User tests(Tests that require user input)
import { createContext, useState, useEffect } from "react";
import { userTests } from "./dummyData";

const UserTestsContext = createContext({
  userTests: [],
  totalUserTests: 0,
  getUserTest: (testId) => {},
  getUserTests: () => {},
  isUserTestPresent: (testId) => {},
});

export function UserTestsContextProvider(props) {
  const [usrTests, setUsrTests] = useState([]);
  const [isLoading, setIsLoading] = useState([]);

  useEffect(() => {
    console.log("Loading/Re-Loading user tests into context");
    setIsLoading(true);
    setUsrTests(userTests);
    console.log(usrTests);
    setIsLoading(false);
    console.log("Loaded/Re-Loaded user tests into context");
  }, []);

  function isLoadingComplete() {
    if (usrTests.length > 0) {
      console.log("User Tests is Non-Empty");
      return true;
    }
    console.log("User Tests is EMPTY");
    return false;
  }

  function getUserTestHandler(testId) {
    if (isLoadingComplete()) {
      //// For Debugging
      console.log("TypeOf testId " + typeof testId);

      for (let x in usrTests) {
        const usrTest = usrTests[x];
        console.log("usrTest.id = " + usrTest.id);
        console.log("TypeOf usrTest.id " + typeof usrTest.id);
        if (usrTest.id === testId) {
          console.log("MATCH !!!!");
          return usrTest;
        }
      }
      //// Check and uncomment for production
      //   setProxyMessages((proxyMessages) => {
      // return proxyMessages.filter((message) => message.id === msgId);
      //   });
    } else {
      console.log("User Tests NOT loaded yet");
    }
    return null;
  }

  function getUserTestsHandler() {
    return usrTests;
  }

  function isUserTestPresentHandler(testId) {
    return usrTests.some((test) => test.id === testId);
  }

  const contextData = {
    userTests: usrTests,
    totalUserTests: usrTests.length,
    getUserTest: getUserTestHandler,
    getUserTests: getUserTestsHandler,
    isUserTestPresent: isUserTestPresentHandler,
  };

  return (
    <UserTestsContext.Provider value={{ contextData, isLoading }}>
      {props.children}
    </UserTestsContext.Provider>
  );
}

export default UserTestsContext;
