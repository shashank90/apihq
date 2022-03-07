import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import styles from "./addApiModal.module.css";
import modalStyle from "../common/modals.module.css";
import Buttons from "../common/Buttons";
import AuthContext from "../../store/auth-context";
import { TEMPLATE } from "../../store/constants";

const fileUploadURL = "/apis/v1/specs";
export default function AddApiModal(props) {
  const [addApiOption, setAddApiOption] = useState(0); // 0: no show, 1: show yes, 2: show no.
  const [collectionName, setCollectionName] = useState("");
  const [file, setFile] = useState();
  const [fileType, setFileType] = useState("");

  const authCtx = useContext(AuthContext);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const history = useHistory();

  const addApiHandler = (addApiOption) => {
    setAddApiOption(addApiOption);
  };

  const handleFileTypeChange = (category) => {
    setFileType(category);
  };

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

  function addApi(e) {
    e.preventDefault();
    if (addApiOption === 1) {
      // Start with spec template
      proceed(TEMPLATE);
    }
    if (addApiOption === 2) {
      //Upload file
      handleUpload(e);
    }
  }

  async function handleUpload(e) {
    e.preventDefault();

    if (file == undefined) {
      return;
    }
    console.log("Uploading file: " + file.name);

    setLoading(true);

    const formData = new FormData();

    formData.append("collection_name", collectionName);
    formData.append("file_type", fileType);
    formData.append("file", file);

    try {
      const response = await fetch(fileUploadURL, {
        method: "POST",
        body: formData,
        headers: {
          "x-access-token": authCtx.token,
        },
      });

      // Parse response data
      const data = await response.json();
      // console.log(data);

      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        // Mark success message and exit after timeout
        setMessage(data.message);
        const specId = data.spec_id;
        proceed(specId);
      }
    } catch (error) {
      setError(error.message);
    }
    setLoading(false);
  }

  function proceed(specId) {
    const timer = setTimeout(() => {
      // props.onCancel();
      history.push("/apis/spec/editor/" + specId);
    }, 1000);
    return () => clearTimeout(timer);
  }

  const isBackBtnVisible = true;
  const isActionBtnVisible = true;
  const isNextBtnVisible = false;
  const actionButtonLabel = "Add";

  const handleOnBack = () => {
    props.onCancel();
  };

  return (
    <div className={modalStyle.modal}>
      <form>
        <h3>Add API</h3>
        <label htmlFor="use_template">Use Template</label>
        <input
          id="use_template"
          type="radio"
          name="Use Template"
          checked={addApiOption === 1}
          onClick={(e) => addApiHandler(1)}
          onChange={(e) => {}}
        />
        <label htmlFor="upload_file">Upload File</label>
        <input
          id="upload_file"
          type="radio"
          name="Upload File"
          checked={addApiOption === 2}
          onClick={(e) => addApiHandler(2)}
          onChange={(e) => {}}
        />
        {addApiOption === 2 && (
          <div className={styles.file_details}>
            <div className={styles.collection_name_container}>
              <label
                htmlFor="collection_name_id"
                className={styles.collection_name_label}
              >
                Collection name
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
            <div className={styles.file_type_container}>
              <label htmlFor="fileOption" className={styles.file_type_label}>
                Select file type
              </label>
              <select
                id="fileOption"
                name="fileOption"
                value={fileType}
                onChange={(event) => handleFileTypeChange(event.target.value)}
              >
                <option id="0">OpenAPI</option>
                <option id="1">Postman Collection</option>
              </select>
            </div>
            <div className={styles.file_upload_container}>
              <label htmlFor="file_id" className={styles.file_selector_label}>
                Select file
              </label>
              <input
                id="file_id"
                type="file"
                onChange={handleFileChange}
                required
              />
            </div>
          </div>
        )}
        <section>{content}</section>
        <Buttons
          isBackBtnVisible={isBackBtnVisible}
          onBackHandle={handleOnBack}
          isActionBtnVisible={isActionBtnVisible}
          onActionHandle={addApi}
          actionButtonLabel={actionButtonLabel}
          isNextBtnVisible={isNextBtnVisible}
        />
      </form>
    </div>
  );
}
