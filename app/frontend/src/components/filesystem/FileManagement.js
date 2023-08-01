import { getAuthToken } from "../../util/auth";

export function FileDownloadButton({ fileUrl, fileName, path }) {
    console.log(path)

    const handleDownload = () => {
        let token = getAuthToken()
        fetch((fileUrl + `?path=${path}`), {
            method: 'POST',
            headers: {
                accept: "/",
                Authorization: "Bearer " + token
            },
            body: null
        })
        .then((response) => response.blob())
        .then((blob) => {
            console.log(blob)
            const url = window.URL.createObjectURL(blob);
            console.log(url)
            const link = document.createElement('a');
            link.href = url;
            console.log(url)
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
        });
    };

    return (
        <button onClick={handleDownload}>
            Download {fileName}
        </button>
    );
}

export function RemoveItem({ fileUrl, fileName, path }) {
    const handleDownload = () => {
        let token = getAuthToken()
        fetch((fileUrl + `?path=${path}`), {
            method: 'DELETE',
            headers: {
                accept: "/",
                Authorization: "Bearer " + token
            }
        })
            .then((response) => response.json());
    };
    return (
        <button onClick={handleDownload}>
            Remove {fileName}
        </button>
    )
}
