import React, { useState, useEffect, useCallback } from "react";
import apiStyles from "./apiSelectorModal.module.css";
import buttons from "../common/buttons.module.css";
import Buttons from "../common/Buttons";
import { useHistory } from "react-router";
import { DeleteOutline } from "@material-ui/icons";

const getApisURL = "http://localhost:3000/apis/v1/discovered";
const runAPIBaseURL = "http://localhost:3000/apis/v1/run";

export default function APIDropdownModal(props) {
  const defaultSelectMessage = "Select Endpoint URL";
  const [apis, setApis] = useState([]);
  const [dataLoading, setDataLoading] = useState(false);
  const [dataLoadingError, setDataLoadingError] = useState("");
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState("");
  const [actionMessage, setActionMessage] = useState("");
  const [apiPath, setApiPath] = useState("");
  const [headerName, setHeaderName] = useState("");
  const [headerValue, setHeaderValue] = useState("");
  const [headerPairs, setHeaderPairs] = useState([]);

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Run";

  const history = useHistory();

  const handleOnBack = () => {
    history.push("/apis/run");
  };

  function getApiId(apiPath) {
    if (apiPath == defaultSelectMessage) {
      return null;
    }
    console.log("api path: " + apiPath);
    for (let x in apis) {
      let api = apis[x];
      console.log(api.apiPath);
      if (api.apiPath == apiPath) {
        return api.apiId;
      }
    }
    console.log("Could not find apiId for path: " + apiPath);
  }

  const handleOnAction = async (e) => {
    e.preventDefault();

    setActionLoading();

    const apiId = getApiId(apiPath);
    if (apiId == null) {
      setActionError("Select API Endpoint URL");
      return;
    }

    const transformedHeaderPairs = headerPairs.map((item) => {
      const headerName = item.value["headerName"];
      const headerValue = item.value["headerValue"];
      return { headerName: headerName, headerValue: headerValue };
    });

    console.log(transformedHeaderPairs);

    const body = { api_path: apiPath, auth_headers: transformedHeaderPairs };
    const runAPIURL = runAPIBaseURL + "/" + apiId;

    try {
      const response = await fetch(runAPIURL, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
          "x-access-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZjdhZDIyMTMtMTZiOS00MDE2LThhZGUtYjA3MjNmNDdlOWFkIiwiZXhwIjoxNjQ0MzQzNzI4fQ.NhX65wQfzo0Mk4gwXBi-2l6SrpCH0CP35I9Uy_pp3uY",
        },
      });

      // Parse response data
      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        console.log("Response status: " + response.status);
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        // Mark success message and exit after timeout
        setActionMessage(data.message);
        exitOnTimeout();
      }
    } catch (error) {
      setActionError(error.message);
    }
    setActionLoading(false);
  };

  function exitOnTimeout() {
    const timer = setTimeout(() => {
      props.onCancel();
    }, 1000);
    return () => clearTimeout(timer);
  }

  const fetchApisHandler = useCallback(async () => {
    setDataLoading(true);
    setDataLoadingError(null);
    try {
      const response = await fetch(getApisURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZjdhZDIyMTMtMTZiOS00MDE2LThhZGUtYjA3MjNmNDdlOWFkIiwiZXhwIjoxNjQ0MzQzNzI4fQ.NhX65wQfzo0Mk4gwXBi-2l6SrpCH0CP35I9Uy_pp3uY",
        },
      });
      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      }

      // Set Api paths
      const transformedApis = data.apis.map((api, index) => {
        return { apiPath: api.api_path, apiId: api.spec_id };
        // endpointURL: api.endpoint_url,
      });
      // Add default entry
      transformedApis.unshift({ apiPath: defaultSelectMessage, apiId: "" });
      setApis(transformedApis);
    } catch (error) {
      setDataLoadingError(error.message);
    }
    setDataLoading(false);
  }, []);

  useEffect(() => {
    fetchApisHandler();
  }, [fetchApisHandler]);

  function handleApiPathChange(event) {
    event.preventDefault();
    setApiPath(event.target.value);
  }

  const addHeaderPair = (e) => {
    e.preventDefault();
    setHeaderName("");
    setHeaderValue("");
    setHeaderPairs((s) => {
      return [
        ...s,
        {
          type: "text",
          value: {},
        },
      ];
    });
  };

  const removeHeaderPair = (e) => {
    e.preventDefault();

    const index = e.target.id;
    setHeaderPairs((s) => {
      const newArr = s.slice();
      // Remove header pair
      if (index > -1) {
        newArr.splice(index, 1);
      }
      return newArr;
    });
  };

  const handleHeaderNameChange = (e) => {
    e.preventDefault();

    const index = e.target.id;
    setHeaderPairs((s) => {
      // Get copy of existing header pair
      const new_header_pair = { ...s[index].value };
      new_header_pair["headerName"] = e.target.value;
      // Create copy of existing array
      const newArr = s.slice();
      // Assign new value to new array(copied)
      newArr[index].value = new_header_pair;

      return newArr;
    });
  };

  const handleSubmit = (e) => {
    console.log("Form submitted");
    e.preventDefault();
  };

  const handleHeaderValueChange = (e) => {
    e.preventDefault();

    // setHeaderValue(e.target.value);
    const index = e.target.id;
    setHeaderPairs((s) => {
      // Get copy of existing header pair
      const new_header_pair = { ...s[index].value };
      new_header_pair["headerValue"] = e.target.value;
      // Create copy of existing array
      const newArr = s.slice();
      // Assign new value to new array(copied)
      newArr[index].value = new_header_pair;

      return newArr;
    });
  };

  let actionContent = <div></div>;

  if (actionError) {
    actionContent = <p className={apiStyles.error_text}>{actionError}</p>;
  }
  if (actionLoading) {
    actionContent = <p>Loading...</p>;
  }
  if (actionMessage) {
    actionContent = <p>{actionMessage}</p>;
  }

  let loadingContent = <div></div>;

  if (apis.length > 0) {
    loadingContent = (
      <form onSubmit={handleSubmit}>
        <h3>API Run</h3>
        <div>
          <label htmlFor="url_selector">API Endpoint URL: </label>
          <select
            className={apiStyles.url_value}
            id="url_selector"
            value={apiPath}
            onChange={handleApiPathChange}
          >
            {apis.map((api, index) => {
              return (
                <option key={index} value={api.apiPath}>
                  {api.apiPath}
                </option>
              );
            })}
          </select>
        </div>
        <div className={apiStyles.header}>
          <div className={apiStyles.header_btn}>
            <button onClick={addHeaderPair} className={buttons.green_btn}>
              Add Authorization Headers
            </button>
          </div>
          <div className={apiStyles.header_pair}>
            {headerPairs.map((item, i) => {
              return (
                <div className={apiStyles.header_pair} key={i}>
                  <div>
                    <label htmlFor={i} className={apiStyles.header_name_label}>
                      Header name:
                    </label>
                    <input
                      className={apiStyles.header_value}
                      onChange={handleHeaderNameChange}
                      value={item.value["headerName"] || ""}
                      id={i}
                      key={i}
                      type="text"
                      size="55"
                      required
                    />
                    <DeleteOutline
                      className="TargetListDelete"
                      onClick={removeHeaderPair}
                    />
                  </div>
                  <div>
                    <label htmlFor={i} className={apiStyles.header_label}>
                      Header value:
                    </label>
                    <input
                      className={apiStyles.header_value}
                      onChange={handleHeaderValueChange}
                      value={item.value["headerValue"] || ""}
                      id={i}
                      key={i}
                      type="text"
                      size="55"
                      required
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <div>{actionContent}</div>
        <div>
          <Buttons
            isBackBtnVisible={isBackBtnVisible}
            onBackHandle={handleOnBack}
            isActionBtnVisible={isActionBtnVisible}
            onActionHandle={handleOnAction}
            actionButtonLabel={actionButtonLabel}
            isNextBtnVisible={isNextBtnVisible}
            onNextHandle={handleOnAction}
          />
        </div>
      </form>
    );
  }

  if (dataLoadingError) {
    loadingContent = <p className={apiStyles.error_text}>{dataLoadingError}</p>;
  }
  if (dataLoading) {
    loadingContent = <p>Loading...</p>;
  }

  return <div className={apiStyles.modal}>{loadingContent}</div>;
}
