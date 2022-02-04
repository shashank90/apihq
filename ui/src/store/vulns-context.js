// Store of all Vulns per target
import { createContext, useState, useEffect } from "react";
import { vulns } from "./dummyData";

const VulnsContext = createContext({
  vulns: [],
  totalVulns: 0,
  getVuln: (vulnId) => {},
  getVulns: () => {},
  isVulnPresent: (vulnId) => {},
});

export function VulnsContextProvider(props) {
  const [vulNs, setVulNs] = useState([]);
  const [isLoading, setIsLoading] = useState([]);

  useEffect(() => {
    console.log("Loading/Re-Loading vulnerabilities into context");
    setIsLoading(true);
    setVulNs(vulns);
    console.log(vulNs);
    setIsLoading(false);
    console.log("Loaded/Re-Loaded vulnerabilities into context");
  }, []);

  function isLoadingComplete() {
    if (vulNs.length > 0) {
      console.log("User Tests is Non-Empty");
      return true;
    }
    console.log("User Tests is EMPTY");
    return false;
  }

  function getVulnHandler(vulnId) {
    if (isLoadingComplete()) {
      //// For Debugging
      console.log("TypeOf testId " + typeof vulnId);

      for (let x in vulNs) {
        const vuln = vulNs[x];
        console.log("vuln.id = " + vuln.id);
        console.log("TypeOf vuln.id " + typeof vuln.id);
        if (vuln.id === vulnId) {
          console.log("MATCH !!!!");
          return vuln;
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

  function getVulnsHandler() {
    return vulns;
  }

  function isVulnPresentHandler(vulnId) {
    return vulNs.some((vuln) => vuln.id === vulnId);
  }

  const contextData = {
    vulns: vulns,
    totalVulns: vulns.length,
    getVuln: getVulnHandler,
    getVulns: getVulnsHandler,
    isVulnPresent: isVulnPresentHandler,
  };

  return (
    <VulnsContext.Provider value={{ contextData, isLoading }}>
      {props.children}
    </VulnsContext.Provider>
  );
}

export default VulnsContext;
