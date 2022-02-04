import React, { useState } from "react";
import styles from "./fileUploadModal.module.css";
import modalStyle from "../common/modals.module.css";
import Buttons from "../common/Buttons";
import { useHistory } from "react-router";
import { DeleteOutline } from "@material-ui/icons";

export default function FileUploadModal(props) {
  const [file, setFile] = useState();
  const [showError, setShowError] = useState();

  function handleChange(event) {
    setFile(event.target.files[0]);
  }

  function handleUpload() {
    if (file == undefined) {
      // setShowError(true);
      return;
    }
    console.log("Uploading file: " + file.name);
    const url = "http://localhost:3000/uploadFile";
    const formData = new FormData();
    formData.append("file", file);
    formData.append("fileName", file.name);
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };
    // axios.post(url, formData, config).then((response) => {
    // console.log(response.data);
    // });
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
            <label htmlFor="collection_name">Collection name:</label>
            <input id="collection_name" type="text" required size="30"></input>
          </div>
          <div className={styles.file_upload_container}>
            <input type="file" onChange={handleChange} required />
          </div>
        </div>
        {showError && (
          <p className={styles.error_text}>Please select a file for upload</p>
        )}
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
