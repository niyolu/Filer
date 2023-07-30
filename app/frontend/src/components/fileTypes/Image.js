import { useState, useEffect } from "react";
export default function Image({ image }) {
    console.log(image.startsWith('data:image/'))
    return (
        <div style={{ width: '60vw' }}>
            {image && (
                <div>
                    <h3>File Content:</h3>
                    {image.startsWith('data:image/') ? (
                        <img src={image} alt="Uploaded File" style={{ maxWidth: '60vw' }} />
                    ) : (
                            <pre>{image}</pre>
                    )}
                </div>
            )}
        </div>
    );

}