from inference import InferencePipeline
import cv2
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")

def my_sink(result, video_frame):
    if result.get("keypoint_visualization"):
        cv2.imshow("Workflow Image", result["keypoint_visualization"].numpy_image)


# Predict off live footage with inference pipeline
pipeline = InferencePipeline.init_with_workflow(
    api_key=API_KEY,
    workspace_name=WORKSPACE_NAME,
    workflow_id=WORKFLOW_ID,
    video_reference=0,
    max_fps=30,
    on_prediction=my_sink
)
pipeline.start()
pipeline.join()
