import os
from org.parosproxy.paros.model import HistoryReference
from org.parosproxy.paros.model import Model


def sendingRequest(msg, initiator, helper):

    # print("sendingRequest called for url=" + msg.getRequestHeader().getURI().toString())

    historyRef = HistoryReference(Model.getSingleton().getSession(), 1, msg)
    msg.setHistoryRef(historyRef)
    msg_id = msg.getHistoryRef().getHistoryId()
    # This is the actual msg id that gets shown in proxy tab of ZAP
    msg_id = msg_id + 1

    headers = msg.getRequestHeader()
    data_dir = headers.getHeader("data_dir")
    request_id = headers.getHeader("request_id")
    file_name = request_id + "_" + str(msg_id)

    zap_msg_dir = data_dir + "/har/zap_message_ids"
    try:
        os.makedirs(zap_msg_dir)
    except OSError:
        print(zap_msg_dir + " already exists...")

    file_path = zap_msg_dir + "/" + file_name

    with open(file_path.encode("ascii"), "w") as fp:
        pass

    # Remove additional request headers
    headers.setHeader("request_id", None)
    headers.setHeader("data_dir", None)


def responseReceived(msg, initiator, helper):
    pass
