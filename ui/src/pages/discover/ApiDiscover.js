import styles from "./apiDiscover.module.css";
import topbarStyles from "../../components/common/topbarstyles.module.css";
import buttons from "../../components/common/buttons.module.css";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import ReactDOM from "react-dom";
import Backdrop from "../../components/common/Backdrop";
import AddApiModal from "../../components/addApi/AddApiModal";
import { DeleteOutline } from "@material-ui/icons";
import AuthContext from "../../store/auth-context";
import DataTable from "../../components/dataTable/DataTable";
import { DATA_REFRESH_FREQUENCY } from "../../store/constants";

const getApisURL = "/apis/v1/discovered";
const baseDeleteAPIURL = "/apis/v1/apis/";

export default function APIInventory() {
  const [apis, setApis] = useState([]);
  const [uploadModalIsOpen, setUploadModalIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const location = useLocation();
  const authCtx = useContext(AuthContext);

  function showModalHandler() {
    setUploadModalIsOpen(true);
  }

  function closeModalHandler() {
    setUploadModalIsOpen(false);
  }

  async function handleDelete(apiId) {
    try {
      const deleteAPIURL = baseDeleteAPIURL + apiId;
      const response = await fetch(deleteAPIURL, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });
      const data = await response.json();
      // console.log(data);
      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        fetchApiInventoryDataFirstTime();
      }
    } catch (error) {
      setError(error.message);
    }
  }

  function updateApis(fetchedApis) {
    if (apis.length > 0) {
      if (JSON.stringify(apis) === JSON.stringify(fetchedApis)) {
      } else {
        setApis(fetchedApis);
      }
    } else {
      setApis(fetchedApis);
    }
  }

  async function fetchApiInventoryDataFirstTime() {
    setIsLoading(true);
    setError(null);
    fetchApiInventoryDataPeriodic();
    setIsLoading(false);
  }

  async function fetchApiInventoryDataPeriodic() {
    try {
      const response = await fetch(getApisURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });
      const data = await response.json();
      // console.log(data);
      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      }

      const transformedApis = data.apis.map((api, index) => {
        return {
          id: index + 1,
          apiId: api.api_id,
          specId: api.spec_id,
          // apiPath: api.api_path,
          apiEndpointURL: api.api_endpoint_url,
          httpMethod: api.http_method,
          collectionName: api.collection_name,
          updated: api.updated,
          // status: api.status,
          // addedBy: api.added_by,
        };
      });
      updateApis(transformedApis);
    } catch (error) {
      setError(error.message);
    }
  }

  useEffect(() => {
    // console.log("Fetch Api Inventory data on first load...");
    fetchApiInventoryDataFirstTime();
    const interval = setInterval(() => {
      fetchApiInventoryDataPeriodic();
    }, DATA_REFRESH_FREQUENCY);
    return () => clearInterval(interval);
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 50 },
    {
      field: "Api Id",
      headerName: "Api Id",
      width: 200,
      renderCell: (params) => {
        return <div className={styles.TargetListItem}>{params.row.apiId}</div>;
      },
    },
    {
      field: "Api Endpoint URL",
      headerName: "Api Endpoint URL",
      width: 350,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>
            {params.row.apiEndpointURL}
          </div>
        );
      },
    },
    {
      field: "HTTP Method",
      headerName: "HTTP Method",
      width: 180,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.httpMethod}</div>
        );
      },
    },
    {
      field: "Collection Name",
      headerName: "Collection Name",
      width: 180,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>
            {params.row.collectionName}
          </div>
        );
      },
    },
    {
      field: "OpenAPI Spec",
      headerName: "OpenAPI Spec",
      width: 200,
      renderCell: (params) => {
        return (
          <>
            <Link
              to={{
                pathname: `/apis/spec/editor/${params.row.specId}`,
                state: { prevPath: location.pathname },
              }}
            >
              <button className={buttons.green_btn}>View</button>
            </Link>
          </>
        );
      },
    },
    {
      field: "Updated",
      headerName: "Updated",
      width: 200,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.updated}</div>
        );
      },
    },
    // {
    //   field: "Added by",
    //   headerName: "Added by",
    //   width: 200,
    //   renderCell: (params) => {
    //     return (
    //       <div className={styles.TargetListItem}>{params.row.addedBy}</div>
    //     );
    //   },
    // },
    {
      field: "Delete",
      headerName: "Delete",
      width: 150,
      renderCell: (params) => {
        return (
          <>
            <DeleteOutline
              className={styles.TargetListDelete}
              onClick={() => handleDelete(params.row.apiId)}
            />
          </>
        );
      },
    },
  ];

  let content = <DataTable data={apis} columns={columns} />;

  if (error) {
    content = <p>{error}</p>;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
  }

  if (uploadModalIsOpen) {
    return (
      <div className="card">
        {ReactDOM.createPortal(
          <Backdrop onCancel={closeModalHandler} />,
          document.getElementById("backdrop-root")
        )}
        {ReactDOM.createPortal(
          <AddApiModal
            onCancel={closeModalHandler}
            onConfirm={closeModalHandler}
          />,
          document.getElementById("overlay-root")
        )}
      </div>
    );
  } else {
    return (
      <div className={styles.TargetList}>
        <div className={topbarStyles.new_action_container}>
          <h1 className={styles.TargetTitle}>Discover</h1>
          <div className={styles.import_api_options}>
            <button
              className={buttons.new_action_btn}
              onClick={() => showModalHandler()}
            >
              Import API
            </button>
          </div>
        </div>
        {content}
      </div>
    );
  }
}
