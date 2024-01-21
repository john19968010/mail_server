from flask import jsonify, Flask

# Note: Remove it when deploy on cloud function
from flask import request
import werkzeug

from exception import BaseException
from mail import Mail


def handle_exception(exception):
    message, status_code = "Internal Server Error", 500
    if isinstance(exception, werkzeug.exceptions.NotFound):
        message, status_code = "Path not found", 400
    # Custom exception
    elif isinstance(exception, BaseException):
        message, status_code = exception.message, exception.status_code

    response = jsonify({"error": message})
    response.status_code = status_code
    return response


app = Flask(__name__)
app.register_error_handler(Exception, handle_exception)


@app.route("/send_mail", methods=["POST"])
# Note: Uncomment it when deploy on cloud function
# def send_mail(request):
def send_mail():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    data = request.get_json()
    domain, port, acc, pwd, receiver, title, content = (
        data.get("domain"),
        data.get("port"),
        data.get("account"),
        data.get("password"),
        data.get("receiver"),
        data.get("title", ""),
        data.get("content", ""),
    )
    if domain is None or port is None or acc is None or pwd is None or receiver is None:
        raise BaseException("Missing parameters", 400)

    with Mail(domain, port, acc, pwd) as mail:
        mail.send(receiver, title, content)
    return "success", 200


"""
Note: 
The following code just for debug on local machine, 
Remove it when deploy on cloud function
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, debug=True, use_reloader=True)
