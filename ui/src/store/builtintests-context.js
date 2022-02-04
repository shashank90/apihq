// Store of all Built-in tests(scan rules) from ZAP
import { createContext, useState, useEffect } from "react";
import { builtinTests } from "./dummyData";

const BuiltinTestsContext = createContext({
  builtinTests: [],
  totalBuiltinTests: 0,
  getBuiltinTest: (testId) => {},
  getBuiltinTests: () => {},
  isBuiltinTestPresent: (testId) => {},
});

export function BuiltinTestsContextProvider(props) {
  const [builtInTests, setBuiltInTests] = useState([]);
  const [isLoading, setIsLoading] = useState([]);

  useEffect(() => {
    console.log("Loading/Re-Loading built-in tests into context");
    setIsLoading(true);
    setBuiltInTests(builtinTests);
    console.log(builtInTests);
    setIsLoading(false);
    console.log("Loaded/Re-Loaded built-in tests into context");
  }, []);

  function isLoadingComplete() {
    if (builtInTests.length > 0) {
      console.log("Builtin Tests is Non-Empty");
      return true;
    }
    console.log("Builtin Tests is EMPTY");
    return false;
  }

  function getBuiltInTestHandler(testId) {
    if (isLoadingComplete()) {
      //// For Debugging
      console.log("TypeOf testId " + typeof testId);

      for (let x in builtInTests) {
        const builtInTest = builtInTests[x];
        console.log("builtInTest.id = " + builtInTest.id);
        console.log("TypeOf builtInTest.id " + typeof builtInTest.id);
        if (builtInTest.id === testId) {
          console.log("MATCH !!!!");
          return builtInTest;
        }
      }
      //// Check and uncomment for production
      //   setProxyMessages((proxyMessages) => {
      // return proxyMessages.filter((message) => message.id === msgId);
      //   });
    } else {
      console.log("Builtin Tests NOT loaded yet");
    }
    return null;
  }

  function getBuiltInTestsHandler() {
    return builtInTests;
  }

  function isBuiltInTestPresentHandler(testId) {
    return builtInTests.some((test) => test.id === testId);
  }

  const contextData = {
    builtinTests: builtInTests,
    totalBuiltinTests: builtInTests.length,
    getBuiltinTest: getBuiltInTestHandler,
    getBuiltinTests: getBuiltInTestsHandler,
    isBuiltinTestPresent: isBuiltInTestPresentHandler,
  };

  return (
    <BuiltinTestsContext.Provider value={{ contextData, isLoading }}>
      {props.children}
    </BuiltinTestsContext.Provider>
  );
}

export default BuiltinTestsContext;
