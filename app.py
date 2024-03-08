from flask import Flask, render_template, request, Response
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Define your blob_service_client here
connection_string = "DefaultEndpointsProtocol=https;AccountName=blobstorageformp3player;AccountKey=Xb52Hg1E/N/FD+txtai3RMST9A91kwNacbQUqskC4ut3m54LT68kc+Xyl87lCi3VN5/6N4HTy78a+AStYNUcIg==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


@app.route("/", methods=["GET", "POST"])
def index():
    container_name = "files"
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs()

    selected_blob = None
    if request.method == "POST":
        selected_blob = request.form.get("selected_blob")

    return render_template(
        "index.html", blob_list=blob_list, selected_blob=selected_blob
    )


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    blob_name = filename
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)

    def generate():
        download_stream = blob_client.download_blob().readall()
        for i in range(0, len(download_stream), 1024):
            yield download_stream[i : i + 1024]

    response = Response(generate(), mimetype="audio/mpeg")
    response.headers["Content-Length"] = blob_client.get_blob_properties().size
    return response


if __name__ == "__main__":
    app.run(debug=True)
