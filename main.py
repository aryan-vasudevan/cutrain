from inference import InferencePipeline
import cv2
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")

pipeline = None

def process(result, video_frame):
    if result.get("keypoint_visualization"):
        cv2.imshow("Workflow Image", result["keypoint_visualization"].numpy_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pipeline.terminate()

# Initialize and start the pipeline
pipeline = InferencePipeline.init_with_workflow(
    api_key=API_KEY,
    workspace_name=WORKSPACE_NAME,
    workflow_id=WORKFLOW_ID,
    video_reference=0,
    max_fps=30,
    on_prediction=process
)

pipeline.start()
pipeline.join()
cv2.destroyAllWindows()
