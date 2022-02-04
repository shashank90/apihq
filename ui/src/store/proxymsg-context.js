// Store of all messages proxied through ZAP
import { createContext, useState, useEffect } from "react";
import { messages } from "./dummyData";

const ProxyMessagesContext = createContext({
  messages: [],
  totalMessages: 0,
  addMessage: (msg) => {},
  getMessage: (msgId) => {},
  getMessages: () => {},
  isMessagePresent: (msgId) => {},
});

export function ProxyMessagesContextProvider(props) {
  const [proxyMessages, setProxyMessages] = useState([]);
  const [isLoading, setIsLoading] = useState([]);

  function getMessgs() {
    setProxyMessages(messages);
  }

  useEffect(() => {
    console.log("Loading/Re-Loading proxied message data into context");
    setIsLoading(true);
    getMessgs();
    setIsLoading(false);
    console.log("Loaded/Re-Loaded proxied message data into context");
  }, []);

  function addMessageHandler(msg) {
    setProxyMessages((prevProxyMessages) => {
      return prevProxyMessages.concat(msg);
    });
  }

  function isLoadingComplete() {
    if (proxyMessages.length > 0) {
      console.log("Proxy Messages is Non-Empty");
      return true;
    }
    console.log("Proxy Messages EMPTY");
    return false;
  }

  function getMessageHandler(msgId) {
    if (isLoadingComplete()) {
      //// For Debugging
      console.log("TypeOf msgId " + typeof msgId);
      for (let x in proxyMessages) {
        let message = proxyMessages[x];
        console.log("message.id = " + message.id);
        console.log("TypeOf message.id " + typeof message.id);
        if (message.id === msgId) {
          console.log("MATCH !!!!");
          return message;
        }
      }
      ////
      //   setProxyMessages((proxyMessages) => {
      // return proxyMessages.filter((message) => message.id === msgId);
      //   });
    } else {
      console.log("Proxy Messages NOT loaded yet");
    }
    return null;
  }

  function getMessagesHandler() {
    return proxyMessages;
  }

  function isMessagePresentHandler(msgId) {
    return proxyMessages.some((message) => message.id === msgId);
  }

  const contextData = {
    messages: proxyMessages,
    totalMessages: proxyMessages.length,
    addMessage: addMessageHandler,
    getMessage: getMessageHandler,
    getMessages: getMessagesHandler,
    isMessagePresent: isMessagePresentHandler,
  };

  return (
    <ProxyMessagesContext.Provider value={{ contextData, isLoading }}>
      {props.children}
    </ProxyMessagesContext.Provider>
  );
}

export default ProxyMessagesContext;
