import { useState } from "react";
import styles from "../common/msgDetails.module.css";
import classes from "./requestEditor.module.css";
import { SPEC_STRING_MAX_LENGTH } from "../../store/constants";
import buttons from "../common/buttons.module.css";
import AceEditor from "react-ace";
import { DeleteOutline } from "@material-ui/icons";

export default function RequestEditor(props) {
  const msgDetails = {
    url: "https://apihome.io",
    reqHeader: "",
    reqBody: "",
    resHeader: [],
    resBody: "",
  };

  //   const msgDetails = props.msgDetails;
  const [headerPairs, setHeaderPairs] = useState([]);
  const [bodyKeyValuePairs, setBodyKeyValuePairs] = useState([]);
  const [url, setUrl] = useState(msgDetails.url);
  const [reqHeader, setReqHeader] = useState(msgDetails.reqHeader);
  const [reqBody, setReqBody] = useState(msgDetails.reqBody);
  const [resHeaders, setResHeaders] = useState(msgDetails.resHeader);
  const [resBody, setResBody] = useState(msgDetails.resBody);
  const [remarks, setRemarks] = useState();
  const [httpMethod, setHttpMethod] = useState("GET");
  const [contentType, setContentType] = useState("JSON");

  const editable = props.editable;

  const isBackBtnVisible = true;

  const handleOnBack = () => {
    props.showRequest(false);
  };

  function handleURLChange(event) {
    setUrl(event.target.value);
  }

  function handleHttpMethodChange(event) {
    setHttpMethod(event.target.value);
  }

  function handleReqHeaderChange(event) {
    setReqHeader(event.target.value);
  }

  function handleReqBodyChange(newValue) {
    // console.log(newValue);
    if (newValue.length > SPEC_STRING_MAX_LENGTH) {
      // setError(
      //   "Request body length cannot exceed " +
      //     SPEC_STRING_MAX_LENGTH +
      //     " characters."
      // );

      // TODO: Show Error pop-ups
      console.log(
        "Request body length cannot exceed " +
          SPEC_STRING_MAX_LENGTH +
          " characters"
      );
    }
    setReqBody(newValue);
  }

  async function sendRequest() {
    try {
      console.log("Sending request...");
      let headers = {};
      headers["Content-Type"] = contentType;
      headerPairs.map((item) => {
        headers[item.value["headerName"]] = item.value["headerValue"];
      });

      const response = await fetch(url, {
        method: httpMethod,
        headers: headers,
      });

      const data = await response.json();
      // console.log(data);
      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        //Extract response into headers and body
        const headerS = formHeaders(response.headers);
        // console.log(headerStr);
        setResHeaders(headerS);
        let body = "";
        setResBody(JSON.stringify(data));
      }
    } catch (error) {
      // setError(error.message);
      console.log(error.message);
      console.log("Error while hitting URL: " + url);
    }
  }

  function formHeaders(headers) {
    const headerS = [];
    for (var pair of headers.entries()) {
      const headerStr = pair[0] + "- " + pair[1];
      headerS.push(headerStr);
    }
    return headerS;
  }

  function handleResHeaderChange(event) {
    setResHeaders(event.target.value);
  }
  function handleResBodyChange(event) {
    setResBody(event.target.value);
  }
  function handleRemarksChange(event) {
    setRemarks(event.target.value);
  }

  const handleContentTypeChange = (contentType) => {
    setContentType(contentType);
  };

  const addHeaderPair = (e) => {
    e.preventDefault();
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
  const addBodyKeyValuePair = (e) => {
    e.preventDefault();
    setBodyKeyValuePairs((s) => {
      return [
        ...s,
        {
          type: "text",
          value: { formDataType: "text" },
        },
      ];
    });
  };

  const removeHeaderPair = (e, index) => {
    e.preventDefault();

    setHeaderPairs((s) => {
      const newArr = s.slice();
      // Remove header pair
      if (index > -1) {
        newArr.splice(index, 1);
      }
      return newArr;
    });
  };

  const removeBodyKeyValuePair = (e) => {
    e.preventDefault();

    const index = e.target.id;
    setBodyKeyValuePairs((s) => {
      const newArr = s.slice();
      // Remove header pair
      if (index > -1) {
        newArr.splice(index, 1);
      }
      return newArr;
    });
  };

  const handleHeaderNameChange = (e, index) => {
    e.preventDefault();

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

  function updateBodyKeyValuePairs(key, value, index) {
    setBodyKeyValuePairs((s) => {
      // Get copy of existing key value pair
      const new_pair = { ...s[index].value };
      new_pair[key] = value;
      // Create copy of existing array
      const newArr = s.slice();
      // Assign new value to new array(copied)
      newArr[index].value = new_pair;

      return newArr;
    });
  }

  const handleFormDataTypeChange = (val, index) => {
    // e.preventDefault();
    const key = "formDataType";
    updateBodyKeyValuePairs(key, val, index);
  };

  const handleFormDataKeyChange = (e, index) => {
    e.preventDefault();
    const key = "key";
    const val = e.target.value;
    updateBodyKeyValuePairs(key, val, index);
  };

  const handleFormDataValueChange = (e, index, type) => {
    e.preventDefault();
    const key = "value";
    let val = e.target.value;
    if (type === "file") {
      val = e.target.files[0];
    }
    updateBodyKeyValuePairs(key, val, index);
  };

  const handleHeaderValueChange = (e, index) => {
    e.preventDefault();

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

  let requestBody = (
    <div className={classes.requestBodyTextArea}>
      <AceEditor
        mode="json"
        theme="github"
        onChange={handleReqBodyChange}
        fontSize={14}
        width="700px"
        height="350px"
        tabSize={2}
        highlightActiveLine
        name="openapi-editor"
        value={reqBody}
        editorProps={{ $blockScrolling: true }}
      />
    </div>
  );

  if (contentType === "form-data" || contentType === "x-www-form-urlencoded") {
    requestBody = (
      <div>
        <div className={classes.header_btn}>
          <button onClick={addBodyKeyValuePair} className={buttons.green_btn}>
            Add Key Value Pair
          </button>
        </div>
        <div className={classes.formContainer}>
          <form id="formC">
            {bodyKeyValuePairs.map((item, i) => {
              return (
                <div className={classes.rows} key={i}>
                  <div className={classes.column}>
                    <label className={classes.theLabels}>Key:</label>
                    <input
                      className={`${classes.theInputs} ${classes.keyInput}`}
                      onChange={(event) => handleFormDataKeyChange(event, i)}
                      value={item.value["key"] || ""}
                      id={i}
                      key={i}
                      type="text"
                      size="44"
                      required
                    />
                    <span className={classes.deleteButton}>
                      <DeleteOutline
                        onClick={(event) => removeBodyKeyValuePair(event, i)}
                      />
                    </span>
                  </div>
                  <div className={classes.column}>
                    <label className={classes.theLabels}>Value:</label>
                    {item.value["formDataType"] === "text" ? (
                      <input
                        className={`${classes.theInputs} ${classes.valueInput}`}
                        type="text"
                        value={item.value["value"] || ""}
                        id={i}
                        key={i}
                        size="44"
                        onChange={(event) =>
                          handleFormDataValueChange(event, i, "text")
                        }
                        required
                      />
                    ) : (
                      <input
                        className={`${classes.theInputs} ${classes.valueInput}`}
                        id="file_id"
                        type="file"
                        onChange={(event) =>
                          handleFormDataValueChange(event, i, "file")
                        }
                        required
                      />
                    )}
                    {contentType === "form-data" && (
                      <div className={classes.formDataType}>
                        <select
                          id="formDataType"
                          name="formDataType"
                          value={item.value["formDataType"] || "text"}
                          onChange={(event) =>
                            handleFormDataTypeChange(event.target.value, i)
                          }
                        >
                          <option id="0">text</option>
                          <option id="1">file</option>
                        </select>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </form>
        </div>
      </div>
    );
  }

  // console.log(resHeaders);

  return (
    <div className={classes.container}>
      <div className={classes.headingContainer}>
        <div>
          <h2>Edit Request</h2>
        </div>
        <div>
          <nav>
            <ul className={classes.list}>
              <li className={classes.item}>
                <button className={buttons.action_btn} onClick={sendRequest}>
                  Send
                </button>
              </li>
              <li className={classes.item}>
                <button className={buttons.action_btn}>Add</button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <div>
        <label htmlFor="url" className={classes.urlLabel}>
          URL
        </label>
        <select
          id="method"
          name="method"
          value={httpMethod}
          onChange={handleHttpMethodChange}
        >
          <option id="0">GET</option>
          <option id="1">POST</option>
          <option id="2">PUT</option>
          <option id="2">DELETE</option>
        </select>
        <input
          className={classes.urlStyle}
          onChange={handleURLChange}
          type="text"
          id="url"
          size="75"
          required
        />
      </div>
      <div className={classes.requestResponseContainer}>
        <div className={classes.request}>
          <div className={classes.heading}>Request Header</div>
          <div className={classes.headerContainer}>
            <div className={classes.header_btn}>
              <button onClick={addHeaderPair} className={buttons.green_btn}>
                Add Headers
              </button>
            </div>
            <div className={classes.formContainer}>
              <form id="formC">
                {headerPairs.map((item, i) => {
                  return (
                    <div className={classes.rows} key={i}>
                      <div className={classes.column}>
                        <label htmlFor="headerNameInput">Header Name:</label>
                        <input
                          className={`${classes.theInputs} ${classes.headerNameInput}`}
                          onChange={(event) => handleHeaderNameChange(event, i)}
                          value={item.value["headerName"] || ""}
                          id="headerNameInput"
                          key={i}
                          type="text"
                          size="44"
                          required
                        />
                        <span className={classes.deleteButton}>
                          <DeleteOutline
                            onClick={(event) => removeHeaderPair(event, i)}
                          />
                        </span>
                      </div>
                      <div className={classes.column}>
                        <label className={classes.theLabels}>
                          Header Value:
                        </label>
                        <input
                          className={`${classes.theInputs} ${classes.headerValueInput}`}
                          onChange={(event) =>
                            handleHeaderValueChange(event, i)
                          }
                          type="text"
                          value={item.value["headerValue"] || ""}
                          id={i}
                          key={i}
                          size="44"
                          required
                        />
                      </div>
                    </div>
                  );
                })}
              </form>
            </div>
          </div>
          <div className={classes.heading}>Request Body</div>
          <div className={classes.requestBodyContainer}>
            <div>
              <label className={classes.contentTypeLabel} htmlFor="contentType">
                Content-Type
              </label>
              <select
                id="contentType"
                name="contentType"
                value={contentType}
                onChange={(event) =>
                  handleContentTypeChange(event.target.value)
                }
              >
                <option id="0">JSON</option>
                <option id="1">form-data</option>
                <option id="2">x-www-form-urlencoded</option>
              </select>
            </div>
            {requestBody}
          </div>
        </div>
        <div className={classes.response}>
          <div className={classes.heading}>Response Header</div>
          <div className={classes.responseBodyContainer}>
            {resHeaders}
            {/* {resHeaders.map((item) => {
              <li>{item}</li>;
            })} */}
          </div>
          <div className={classes.heading}>Response Body</div>
          <div className={classes.responseBodyContainer}>{resBody}</div>
        </div>
      </div>
    </div>
  );
}
