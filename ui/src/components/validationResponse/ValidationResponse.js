import buttons from "../../components/common/buttons.module.css";
import styles from "./validationResponse.module.css";
import React, { useEffect, useState } from "react";
import AceEditor from "react-ace";

export default function ValidationResponse(props) {
  const [showExample, setShowExample] = useState(false);
  const [exampleData, setExampleData] = useState({
    description: "",
    example: "",
  });

  const validationResponse = props.response;
  // console.log(validationResponse);

  function backButtonHandler() {
    setShowExample(false);
  }

  function showExampleHandler(index) {
    setShowExample(true);
    const responseObject = validationResponse.messages[index];
    setExampleData(responseObject);
  }

  // Hide selected example if new validation response is received(upon hitting validate button)
  useEffect(() => {
    if (showExample) {
      setShowExample(false);
    }
  }, [validationResponse]);

  let content = <div></div>;

  content = validationResponse.messages.map((item, index) => (
    <li key={index + 1} onClick={() => showExampleHandler(index)}>
      <div className={styles.box}>
        <div>Message: {item.message}</div>
        <div>Path: {item.path}</div>
        <div>Line: {item.line}</div>
      </div>
    </li>
  ));

  if (showExample) {
    return (
      <div className={styles.example_container}>
        <div className={styles.example_head}>
          <div className={styles.example_heading}>Description</div>
          <div className={styles.example_back_btn}>
            <button
              className={buttons.action_btn}
              onClick={() => backButtonHandler()}
            >
              Back
            </button>
          </div>
        </div>
        <div className={styles.description_container}>
          {exampleData.description}
        </div>
        <div className={styles.example_heading}>Example</div>
        {/* <div className={styles.example_body}>{exampleData.example}</div> */}
        <div className={styles.example_body}>
          <AceEditor
            mode="yaml"
            theme="github"
            // onChange={onChange}
            readOnly={true}
            fontSize={18}
            width="495px"
            height="545px"
            tabSize={2}
            showPrintMargin
            showGutter={true}
            highlightActiveLine
            name="openapi-editor"
            value={exampleData.example}
            editorProps={{ $blockScrolling: true }}
          />
        </div>
      </div>
    );
  } else {
    return <div>{content}</div>;
  }
}
