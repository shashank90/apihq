import os
from org.parosproxy.paros.model import HistoryReference
from org.parosproxy.paros.model import Model


def sendingRequest(msg, initiator, helper):

    # print("sendingRequest called for url=" + msg.getRequestHeader().getURI().toString())

    historyRef = HistoryReference(Model.getSingleton().getSession(), 1, msg)
    msg.setHistoryRef(historyRef)
    msg_id = msg.getHistoryRef().getHistoryId()

    header = msg.getRequestHeader()
    data_dir = header.getHeader("request_id")
    file_name = str(msg_id)

    har_dir = data_dir + "/har"
    try:
        os.makedirs(har_dir)
    except OSError:
        print(har_dir + " already exists...")

    file_path = har_dir + "/" + file_name

    with open(file_path.encode("ascii"), "w") as fp:
        pass

    # Remove additional request headers
    msg.getRequestHeader().setHeader("request_id", None)


def responseReceived(msg, initiator, helper):
    pass
