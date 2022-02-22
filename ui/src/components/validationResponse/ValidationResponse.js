import buttons from "../../components/common/buttons.module.css";
import styles from "./validationResponse.module.css";
import React, { useState } from "react";

export default function ValidationResponse(props) {
  console.log("In Validation Response component...");
  const [showExample, setShowExample] = useState(false);
  const [exampleData, setExampleData] = useState({
    description: "",
    example: "",
  });

  console.log("props show example " + props.showExample);
  console.log("component showExample " + showExample);

  const validationResponse = props.response;
  console.log(validationResponse);

  function backButtonHandler() {
    setShowExample(false);
  }

  function showExampleHandler(index) {
    setShowExample(true);
    const responseObject = validationResponse.messages[index];
    setExampleData(responseObject);
  }

  // Hide example if validate button is hit freshly and if example is already being shown
  if (showExample && !props.showExample && exampleData.description) {
    setShowExample(false);
  }

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
        <div className={styles.example_body}>{exampleData.example}</div>
      </div>
    );
  } else {
    return <div>{content}</div>;
  }
}
