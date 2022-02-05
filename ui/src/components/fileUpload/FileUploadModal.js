import React, { useState } from "react";
import styles from "./fileUploadModal.module.css";
import modalStyle from "../common/modals.module.css";
import Buttons from "../common/Buttons";
import { useHistory } from "react-router";
import { DeleteOutline } from "@material-ui/icons";

export default function FileUploadModal(props) {
  const [collectionName, setCollectionName] = useState("");
  const [file, setFile] = useState();
  const fileUploadURL = "http://localhost:3000/apis/v1/specs";

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  let content = <p></p>;

  if (message) {
    content = <p>{message}</p>;
  }
  if (error) {
    content = <p className={styles.error_text}>{error}</p>;
  }
  if (loading) {
    content = <p>Loading...</p>;
  }

  function handleFileChange(event) {
    setFile(event.target.files[0]);
  }

  function handleCollectionNameChange(event) {
    setCollectionName(event.target.value);
  }

  async function handleUpload(e) {
    e.preventDefault();

    if (file == undefined) {
      // setShowError(true);
      return;
    }
    console.log("Uploading file: " + file.name);

    setLoading(true);

    const formData = new FormData();

    formData.append("collection_name", collectionName);
    formData.append("file", file);

    try {
      const response = await fetch(fileUploadURL, {
        method: "POST",
        body: formData,
        headers: {
          "x-access-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZjdhZDIyMTMtMTZiOS00MDE2LThhZGUtYjA3MjNmNDdlOWFkIiwiZXhwIjoxNjQ0MzE5NTczfQ.hgmY5tICsK8lSRL3FItm5-hbIe2lqQdmEOVs2RI2N5g",
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
        setMessage(data.message);
        exitOnTimeout();
      }
    } catch (error) {
      setError(error.message);
    }
    setLoading(false);
  }

  function exitOnTimeout() {
    const timer = setTimeout(() => {
      props.onCancel();
    }, 1000);
    return () => clearTimeout(timer);
  }

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Upload";

  const handleOnBack = () => {
    props.onCancel();
  };

  return (
    <div className={modalStyle.modal}>
      <form>
        <h3>API Upload</h3>
        <div className={styles.file_details}>
          <div>
            <label htmlFor="collection_name_id">Collection name:</label>
            <input
              id="collection_name_id"
              type="text"
              required
              size="30"
              value={collectionName}
              onChange={handleCollectionNameChange}
            ></input>
          </div>
          <div className={styles.file_upload_container}>
            <input type="file" onChange={handleFileChange} required />
          </div>
        </div>
        <section>{content}</section>
        <Buttons
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
          isActionBtnVisible={isActionBtnVisible}
          onActionHandle={handleUpload}
          actionButtonLabel={actionButtonLabel}
          isNextBtnVisible={isNextBtnVisible}
        />
      </form>
    </div>
  );
}
