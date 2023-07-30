export default function Video({ videoUrl }) {
    console.log("Hallo")
    return (
        <div>
            {/* Render the video player */}
            <video controls>
                <source src={videoUrl} type="video/mp4" />
                {/* You can add more source elements for different video formats */}
                {/* For example, <source src={videoUrl} type="video/webm" /> */}
                Your browser does not support the video tag.
            </video>
        </div>
    )
}