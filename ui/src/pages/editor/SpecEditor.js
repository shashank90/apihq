import React, { useState, useCallback, useEffect } from "react";
import styles from "./specEditor.module.css";
import AceEditor from "react-ace";
import { defaultValue } from "./defaultTemplate.js";
import jsyaml from "js-yaml";
import "ace-builds/src-noconflict/mode-yaml";
import "ace-builds/src-noconflict/theme-github";
import { useHistory } from "react-router";
import Buttons from "../../components/common/Buttons";
import buttons from "../../components/common/buttons.module.css";
import ValidationResponse from "../../components/validationResponse/ValidationResponse";
import { useParams } from "react-router-dom";

const fileSaveBaseURL = "http://localhost:3000/apis/v1/spec_strings";
const getSpecBaseURL = "http://localhost:3000/apis/v1/specs";

const addSpecMessage =
  "Add new OpenAPI spec. Use below petstore sample as template";
const validateSpecMessage = "Validate spec";

export default function SpecEditor(props) {
  const [spec, setSpec] = useState(defaultValue);
  const [collectionName, setCollectionName] = useState("");
  const [validationStatus, setValidationStatus] = useState("");
  const [validationResponse, setValidationResponse] = useState("");
  const [validationLoading, setValidationLoading] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const [specLoading, setSpecLoading] = useState(false);
  const [specError, setSpecError] = useState(null);

  // Use this to go back to appropriate previous page
  // const location = useLocation();
  // const prevPath = location.state.prevPath;
  // console.log(prevPath);

  const params = useParams();
  let specId = params.specId;
  console.log(specId);

  function onChange(newValue) {
    setSpec(newValue);
    // var obj = jsyaml.load(newValue);
    // var jsonStr = JSON.stringify(obj);
    // console.log(jsonStr);
  }

  function handleCollectionNameChange(event) {
    setCollectionName(event.target.value);
  }

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const history = useHistory();
  const actionButtonLabel = "Validate";

  const fetchSpecHandler = useCallback(async () => {
    setSpecLoading(true);
    setSpecError(null);
    const getSpecURL = getSpecBaseURL + "/" + specId;
    try {
      const response = await fetch(getSpecURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZjdhZDIyMTMtMTZiOS00MDE2LThhZGUtYjA3MjNmNDdlOWFkIiwiZXhwIjoxNjQ0NDk3NDA4fQ.pdHYNUYa9jHzYzcgNyK45VN0iYRCcx60kvNsp-PMy20",
        },
      });
      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        throw new Error("Something went wrong!");
      }
      if ("spec_string" in data) {
        // convert json object to yaml
        setSpec(jsyaml.dump(data.spec_string));
      }
      if ("collection_name" in data) {
        setCollectionName(data.collection_name);
      }
      if ("validate_output" in data) {
        setValidationResponse(JSON.parse(data.validate_output));
      }
    } catch (error) {
      setSpecError(error.message);
    }
    setSpecLoading(false);
  }, []);

  useEffect(() => {
    fetchSpecHandler();
  }, [fetchSpecHandler]);

  // Spec String
  let specString = spec;

  if (specError) {
    specString = specError;
  }
  if (specLoading) {
    specString = "Loading...";
  }

  //Validation response content
  let validationContent = <div></div>;

  if (validationResponse) {
    validationContent = (
      <div className={styles.validate_content}>
        <ValidationResponse response={validationResponse} />
      </div>
    );
  }
  if (validationError) {
    validationContent = <p className={styles.error_text}>{validationError}</p>;
  }
  if (validationLoading) {
    validationContent = <p>Loading...</p>;
  }

  const handleOnBack = () => {
    history.push("/apis");
  };

  const handleOnAction = async (e) => {
    if (
      collectionName == undefined ||
      collectionName == null ||
      collectionName == ""
    ) {
      console.log("Collection name cannot be empty");
      return;
    }

    e.preventDefault();
    setValidationLoading(true);

    const spec_object = { collection_name: collectionName, spec_string: spec };

    // Create spec
    let fileSaveURL = fileSaveBaseURL;
    let http_method = "POST";
    if (specId) {
      fileSaveURL = fileSaveBaseURL + "/" + specId;
      http_method = "PUT";
    }
    try {
      const response = await fetch(fileSaveURL, {
        method: http_method,
        body: JSON.stringify(spec_object),
        headers: {
          "Content-Type": "application/json",
          "x-access-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZjdhZDIyMTMtMTZiOS00MDE2LThhZGUtYjA3MjNmNDdlOWFkIiwiZXhwIjoxNjQ0NDk3NDA4fQ.pdHYNUYa9jHzYzcgNyK45VN0iYRCcx60kvNsp-PMy20",
        },
      });

      // Parse response data
      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        console.log("Response status: " + response.status);
        throw new Error(data.message);
      } else {
        if ("validate_output" in data) {
          setValidationResponse(data.validate_output);
        }
      }
    } catch (error) {
      setValidationError(error.message);
    }

    setValidationLoading(false);
  };

  // Render editor
  return (
    <div className={styles.validator_container}>
      <div className={styles.header_container}>
        <form>
          <div className={styles.btn_container}>
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
          <div className={styles.header_msg_container}>
            <div className={styles.msg_container}>
              <h3>{addSpecMessage}</h3>
            </div>
            <div className={styles.collection_status_container}>
              <div className={styles.collection_container}>
                <label
                  htmlFor="collection_name_id"
                  className={styles.collection_label}
                >
                  Collection name:
                </label>
                <input
                  id="collection_name_id"
                  type="text"
                  required
                  size="30"
                  value={collectionName}
                  onChange={handleCollectionNameChange}
                ></input>
              </div>
              <div className={styles.status_container}>
                Status: {validationStatus}
              </div>
            </div>
          </div>
        </form>
        <div className={styles.desc_container}>
          <div className={styles.spec}>
            <h5>Spec</h5>
          </div>
          <div className={styles.result}>
            <h5>Validation Result</h5>
          </div>
        </div>
      </div>
      <div className={styles.body_container}>
        <div className={styles.editor_container}>
          <div className={styles.editor}>
            <AceEditor
              mode="yaml"
              theme="github"
              onChange={onChange}
              fontSize={18}
              width="785px"
              height="700px"
              tabSize={2}
              showPrintMargin
              showGutter={true}
              highlightActiveLine
              name="openapi-editor"
              value={specString}
              editorProps={{ $blockScrolling: true }}
            />
          </div>
        </div>
        <div className={styles.validate_result_container}>
          {validationContent}
        </div>
      </div>
    </div>
  );
}
