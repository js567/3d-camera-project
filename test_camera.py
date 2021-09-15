import cv2
import mediapipe


drawingModule = mediapipe.solutions.drawing_utils
faceModule = mediapipe.solutions.face_mesh

circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(255, 0, 0))

with faceModule.FaceMesh(static_image_mode=True) as face:

    image = cv2.imread("C:/Users/jack/PycharmProjects/opencv-recognition-project/2021.09.14_21.25.27/frame2.png")

    results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.multi_face_landmarks:

        for result in results.multi_face_landmarks:

            for id, lm in enumerate(result.landmark):

                h, w, c = image.shape

                if id == 1:
                    print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    print(cx, cy)

            drawingModule.draw_landmarks(image, result, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                                             lineDrawingSpec)

    cv2.imshow('Test image', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()