import { useState, useEffect } from "react";
export default function Text({ textFile }) {
    console.log(textFile.video)
    const [textData, setTextData] = useState('');

    useEffect(() => {
        // Fetch the text file content from the URL
        fetch(textFile.video)
            .then((response) => response.text())
            .then((data) => setTextData(data))
            .catch((error) => console.error('Error fetching the text file:', error));
    }, [textFile]);
    return (
        <div style={{ width: '60vw' }}>
            {textFile.video && (
                <div>
                    <h3>File Content:</h3>
                    <pre>{textData}</pre>
                </div>
            )}
        </div>
    );

}