import React, { useState, useCallback, useEffect, useContext } from "react";
import styles from "./specEditor.module.css";
import AceEditor from "react-ace";
import { defaultValue } from "./defaultTemplate.js";
import "ace-builds/src-noconflict/mode-yaml";
import "ace-builds/src-noconflict/theme-github";
import { useHistory } from "react-router";
import Buttons from "../../components/common/Buttons";
import ValidationResponse from "../../components/validationResponse/ValidationResponse";
import { useParams } from "react-router-dom";
import AuthContext from "../../store/auth-context";
import { TEMPLATE } from "../../store/constants";
import { SPEC_STRING_MAX_LENGTH } from "../../store/constants";

const fileSaveBaseURL = "/apis/v1/spec_strings";
const getSpecBaseURL = "/apis/v1/specs";

const addSpecMessage = "Validate Spec";

export default function SpecEditor(props) {
  const [spec, setSpec] = useState(defaultValue);
  const [collectionName, setCollectionName] = useState("");
  const [validationStatus, setValidationStatus] = useState(
    "Hit Validate to get started!"
  );
  const [validationResponse, setValidationResponse] = useState("");
  const [validationLoading, setValidationLoading] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const [specLoading, setSpecLoading] = useState(false);
  const [specError, setSpecError] = useState(null);
  const isBackBtnVisible = true;
  let isActionBtnVisible = true;
  const history = useHistory();
  const actionButtonLabelSteady = "Validate";
  const actionButtonLabelRunning = "Validating";
  const authCtx = useContext(AuthContext);

  const params = useParams();
  let specId = params.specId;
  // console.log(specId);

  function onChange(newValue) {
    // console.log(newValue);
    if (newValue.length > SPEC_STRING_MAX_LENGTH) {
      setSpecError(
        "Spec length cannot exceed " + SPEC_STRING_MAX_LENGTH + " characters"
      );
    }
    setSpec(newValue);
  }

  function handleCollectionNameChange(event) {
    setCollectionName(event.target.value);
  }

  const fetchSpecHandler = useCallback(async () => {
    setSpecLoading(true);
    setSpecError(null);
    const getSpecURL = getSpecBaseURL + "/" + specId;
    try {
      const response = await fetch(getSpecURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });
      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        console.log("Response status: " + response.status);
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      }
      if ("spec_string" in data) {
        setSpec(data.spec_string);
      }
      if ("collection_name" in data) {
        setCollectionName(data.collection_name);
      }
      if ("validate_output" in data) {
        setValidationResponse(JSON.parse(data.validate_output));
      }
      if ("status" in data) {
        setValidationStatus(data.status);
      }
    } catch (error) {
      setSpecError(error.message);
    }
    setSpecLoading(false);
  }, []);

  useEffect(() => {
    if (specId != TEMPLATE) {
      fetchSpecHandler();
    } else {
      console.log("Load default template...");
    }
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

  if (validationError) {
    validationContent = <p className={styles.error_text}>{validationError}</p>;
  }
  if (validationLoading) {
    validationContent = <p>Loading...</p>;
  }
  if (validationResponse) {
    // console.log(validationResponse);
    validationContent = (
      <div className={styles.validate_content}>
        <ValidationResponse response={validationResponse} />
      </div>
    );
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
    isActionBtnVisible = false;

    const spec_object = { collection_name: collectionName, spec_string: spec };

    // Create spec
    let fileSaveURL = fileSaveBaseURL;
    let http_method = "POST";
    // Update spec string for existing spec, else create new one
    if (specId && specId != TEMPLATE) {
      fileSaveURL = fileSaveBaseURL + "/" + specId;
      http_method = "PUT";
    }

    try {
      const response = await fetch(fileSaveURL, {
        method: http_method,
        body: JSON.stringify(spec_object),
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });

      // Parse response data
      const data = await response.json();
      // console.log(data);
      if (!response.ok) {
        console.log("Response status: " + response.status);
        if ("error" in data) {
          if ("status" in data.error) {
            setValidationStatus(data.error.status);
          }
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        if ("status" in data) {
          setValidationStatus(data.status);
        }
        if ("validate_output" in data) {
          const validate_output = data.validate_output;
          setValidationResponse(validate_output);
        }
      }
    } catch (error) {
      setValidationError(error.message);
      setValidationResponse("");
    }

    setValidationLoading(false);
  };

  // Render editor
  return (
    <div className={styles.validator_container}>
      <div className={styles.header_container}>
        <form>
          <div className={styles.btn_container}>
            {!validationLoading && (
              <Buttons
                isBackBtnVisible={isBackBtnVisible}
                onBackHandle={handleOnBack}
                isActionBtnVisible={isActionBtnVisible}
                onActionHandle={handleOnAction}
                actionButtonLabel={actionButtonLabelSteady}
              />
            )}
            {validationLoading && (
              <Buttons
                isBackBtnVisible={isBackBtnVisible}
                onBackHandle={handleOnBack}
                isActionBtnVisible={isActionBtnVisible}
                onActionHandle={handleOnAction}
                actionButtonLabel={actionButtonLabelRunning}
              />
            )}
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
                  maxLength="30"
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
              width="675px"
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
