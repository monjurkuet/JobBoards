import mitmproxy
from mitmproxy.net.http.http1.assemble import assemble_request

def response(flow):
    if 'https://www.linkedin.com/company/' in flow.request.pretty_url:
        htmldata=flow.response.text
        with open("companyhtmldata.html","w") as f:
            f.write(htmldata)
