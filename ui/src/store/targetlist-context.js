// Store of all User tests(Tests that require user input)
import { createContext, useState, useEffect } from "react";
import { targetList } from "./dummyData";

const TargetListContext = createContext({
  targetList: [],
  totalTargets: 0,
  getTarget: (testId) => {},
  getTargetList: () => {},
  isTargetPresent: (testId) => {},
});

export function TargetListContextProvider(props) {
  const [targeTList, setTargeTList] = useState([]);
  const [isLoading, setIsLoading] = useState([]);

  useEffect(() => {
    console.log("Loading/Re-Loading user tests into context");
    setIsLoading(true);
    setTargeTList(targetList);
    console.log(targeTList);
    setIsLoading(false);
    console.log("Loaded/Re-Loaded user tests into context");
  }, []);

  function isLoadingComplete() {
    if (targeTList.length > 0) {
      console.log("User Tests is Non-Empty");
      return true;
    }
    console.log("User Tests is EMPTY");
    return false;
  }

  function getTargetHandler(targetId) {
    if (isLoadingComplete()) {
      //// For Debugging
      console.log("TypeOf targetId " + typeof targetId);

      for (let x in targeTList) {
        const targeT = targeTList[x];
        console.log("targeTList.id = " + targeTList.id);
        console.log("TypeOf targeTList.id " + typeof targeTList.id);
        if (targeTList.id === targetId) {
          console.log("MATCH !!!!");
          return targeT;
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

  function getTargetListHandler() {
    return targeTList;
  }

  function isTargetPresentHandler(targetId) {
    return targeTList.some((target) => target.id === targetId);
  }

  const contextData = {
    targetList: targeTList,
    totalTargets: targeTList.length,
    getTarget: getTargetHandler,
    getTargetList: getTargetListHandler,
    isTargetPresent: isTargetPresentHandler,
  };

  return (
    <TargetListContext.Provider value={{ contextData, isLoading }}>
      {props.children}
    </TargetListContext.Provider>
  );
}

export default TargetListContext;
