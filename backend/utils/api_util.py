def get_remote_addr(request):
    """
    Get remote ip address from request object
    """
    return request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
