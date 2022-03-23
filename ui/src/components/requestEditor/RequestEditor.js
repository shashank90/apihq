import { useState } from "react";
import styles from "../common/msgDetails.module.css";
import classes from "./requestEditor.module.css";
import buttons from "../common/buttons.module.css";
import { DeleteOutline } from "@material-ui/icons";

export default function RequestEditor(props) {
  const msgDetails = {
    url: "https://apihome.io",
    reqHeader: "",
    reqBody: "",
    resHeader: "",
    resBody: "",
  };

  //   const msgDetails = props.msgDetails;
  const [headerPairs, setHeaderPairs] = useState([]);
  const [bodyKeyValuePairs, setBodyKeyValuePairs] = useState([]);
  const [uri, setUri] = useState(msgDetails.url);
  const [reqHeader, setReqHeader] = useState(msgDetails.reqHeader);
  const [reqBody, setReqBody] = useState(msgDetails.reqBody);
  const [resHeader, setResHeader] = useState(msgDetails.resHeader);
  const [resBody, setResBody] = useState(msgDetails.resBody);
  const [remarks, setRemarks] = useState();
  const [contentType, setContentType] = useState("raw");
  const [formDataType, setFormDataType] = useState("text");
  const [file, setFile] = useState();

  const editable = props.editable;

  const isBackBtnVisible = true;

  const handleOnBack = () => {
    props.showRequest(false);
  };

  function handleURIChange(event) {
    setUri(event.target.value);
  }
  function handleReqHeaderChange(event) {
    setReqHeader(event.target.value);
  }
  function handleReqBodyChange(event) {
    setReqBody(event.target.value);
  }
  function handleResHeaderChange(event) {
    setResHeader(event.target.value);
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

  function updateBodyKeyValuePairs(key, e, index) {
    setBodyKeyValuePairs((s) => {
      // Get copy of existing key value pair
      const new_pair = { ...s[index].value };
      if (
        key === "value" &&
        new_pair.hasOwnProperty("formDataType") &&
        new_pair.formDataType === "file"
      ) {
        new_pair[key] = e.target.files[0];
      } else {
        new_pair[key] = e;
      }
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

  const handleFormDataKeyChange = (e) => {
    e.preventDefault();
    const key = "key";
    const index = e.target.id;
    updateBodyKeyValuePairs(key, e, index);
  };

  const handleFormDataValueChange = (e) => {
    e.preventDefault();
    const key = "value";
    const index = e.target.id;
    updateBodyKeyValuePairs(key, e, index);
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

  let requestBody = (
    <textarea
      className={classes.requestBodyTextArea}
      value={reqBody}
      onChange={handleReqBodyChange}
    />
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
                      onChange={handleFormDataKeyChange}
                      value={item.value["key"] || ""}
                      id={i}
                      key={i}
                      type="text"
                      size="44"
                      required
                    />
                    <div className={classes.deleteButton}>
                      <DeleteOutline onClick={removeBodyKeyValuePair} />
                    </div>
                  </div>
                  <div className={classes.column}>
                    <label className={classes.theLabels}>Value:</label>
                    {item.value["formDataType"] === "text" ? (
                      <input
                        className={`${classes.theInputs} ${classes.valueInput}`}
                        type="text"
                        onChange={handleFormDataValueChange}
                        value={item.value["value"] || ""}
                        id={i}
                        key={i}
                        size="44"
                        required
                      />
                    ) : (
                      <input
                        className={`${classes.theInputs} ${classes.valueInput}`}
                        id="file_id"
                        type="file"
                        onChange={handleFormDataValueChange}
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
                <button>Send</button>
              </li>
              <li className={classes.item}>
                <button>Add</button>
              </li>
            </ul>
          </nav>
        </div>
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
            <div className={classes.header_pair}>
              {headerPairs.map((item, i) => {
                return (
                  <div className={classes.header_pair} key={i}>
                    <div>
                      <label htmlFor={i} className={classes.header_name_label}>
                        Header name:
                      </label>
                      <input
                        className={classes.header_value}
                        onChange={handleHeaderNameChange}
                        value={item.value["headerName"] || ""}
                        id={i}
                        key={i}
                        type="text"
                        size="45"
                        required
                      />
                      <DeleteOutline
                        className="TargetListDelete"
                        onClick={removeHeaderPair}
                      />
                    </div>
                    <div>
                      <label htmlFor={i} className={classes.header_label}>
                        Header value:
                      </label>
                      <input
                        className={classes.header_value}
                        onChange={handleHeaderValueChange}
                        value={item.value["headerValue"] || ""}
                        id={i}
                        key={i}
                        type="text"
                        size="45"
                        required
                      />
                    </div>
                  </div>
                );
              })}
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
                <option id="0">raw</option>
                <option id="1">form-data</option>
                <option id="2">x-www-form-urlencoded</option>
              </select>
            </div>
            {requestBody}
          </div>
        </div>
        <div className={classes.response}>
          <div className={classes.heading}>Response Header</div>
          <div className={classes.responseBodyContainer}></div>
          <div className={classes.heading}>Response Body</div>
          <div className={classes.responseBodyContainer}></div>
        </div>
      </div>
    </div>
  );
}
