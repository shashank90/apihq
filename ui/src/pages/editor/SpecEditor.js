import React, { useState, useEffect } from "react";
import "./specEditor.css";
import jsyaml from "js-yaml";
import AceEditor from "react-ace";
import { defaultValue } from "./defaultTemplate.js";
import "ace-builds/src-noconflict/mode-yaml";
import "ace-builds/src-noconflict/theme-github";
import { useHistory } from "react-router";
import Buttons from "../../components/common/Buttons";
import { useParams, useLocation } from "react-router-dom";

function onChange(newValue) {
  // console.log("change", newValue);
  var obj = jsyaml.load(newValue);
  var jsonStr = JSON.stringify(obj);
  console.log(jsonStr);
}

const addSpecMessage =
  "Add new OpenAPI spec. Use below petstore sample as template";
const validateSpecMessage = "Validate spec";

export default function SpecEditor(props) {
  const [defValue, seDefValue] = useState(defaultValue);
  const [collectionName, setCollectionName] = useState();
  const [validationStatus, setValidationStatus] = useState();

  const location = useLocation();
  const prevPath = location.state.prevPath;
  console.log(prevPath);

  const params = useParams();
  console.log(params.specId);

  useEffect(() => {
    setCollectionName(props.collectionName);
  }, collectionName);

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const history = useHistory();
  const actionButtonLabel = "Validate";

  const handleOnBack = () => {
    if (prevPath.includes("validate")) {
      history.push("/apis/validate");
    } else {
      history.push("/apis");
    }
  };

  const handleOnAction = () => {
    //TODO: call validate api
  };

  // Render editor
  return (
    <div className="validator-container">
      <div className="header-container">
        <div className="btn-container">
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
        <div className="header-msg-container">
          <div className="msg-container">
            <h3>{addSpecMessage}</h3>
          </div>
          <div className="collection-status-container">
            <div className="collection-container">
              <h4>Collection name: {collectionName}</h4>
            </div>
            <div className="status-container">
              <h4>Status: {validationStatus}</h4>
            </div>
          </div>
        </div>
        <div className="desc-container">
          <div className="spec">
            <h5>Spec</h5>
          </div>
          <div className="result">
            <h5>Validation Result</h5>
          </div>
        </div>
      </div>
      <div className="body-container">
        <div className="editor-container">
          <div className="editor">
            <AceEditor
              mode="yaml"
              theme="github"
              onChange={onChange}
              fontSize={18}
              width="785px"
              height="700px"
              defaultValue={defValue}
              tabSize={2}
              showPrintMargin
              showGutter={true}
              highlightActiveLine
              name="openapi-editor"
              editorProps={{ $blockScrolling: true }}
            />
          </div>
        </div>
        <div className="validate-result-container">
          <div>Response</div>
        </div>
      </div>
    </div>
  );
}
