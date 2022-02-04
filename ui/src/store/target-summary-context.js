// Store of all Vulns per target
import { createContext, useState, useEffect } from "react";
import { targetSummary } from "./dummyData";

const TargetSummaryContext = createContext({
  getTargetSummary: () => {},
});

export function TargetSummaryContextProvider(props) {
  const [targeTSummary, setTargeTSummary] = useState([]);
  const [isLoading, setIsLoading] = useState([]);

  useEffect(() => {
    console.log("Loading/Re-Loading target summary into context");
    setIsLoading(true);
    setTargeTSummary(targetSummary);
    console.log(targeTSummary);
    setIsLoading(false);
    console.log("Loaded/Re-Loaded target summary into context");
  }, []);

  function isLoadingComplete() {
    if (targeTSummary.length > 0) {
      console.log("Target Summary is Non-Empty");
      return true;
    }
    console.log("Target Summary is EMPTY");
    return false;
  }

  function getTargetSummaryHandler() {
    if (isLoadingComplete()) {
      return targeTSummary;
    } else {
      console.log("Target summary NOT loaded yet");
    }
    return null;
  }

  const contextData = {
    targetSummary: targeTSummary,
    getTargetSummary: getTargetSummaryHandler,
  };

  return (
    <TargetSummaryContext.Provider value={{ contextData, isLoading }}>
      {props.children}
    </TargetSummaryContext.Provider>
  );
}

export default TargetSummaryContext;
