import cv2
import mediapipe as mp
from pose.rep_counter import RepCounter

from pose_estimation.angle_estimation import calculate_angle
class Bench:
    def __init__(self):
        self.counter = RepCounter()
        # self.cap = cv2.VideoCapture(camera_index)
        # self.cap.set(3, 1280)
        # self.cap.set(4, 720)
        self.pose = mp.solutions.pose.Pose()
        self.drawing = mp.solutions.drawing_utils

        self.angle_down = 75
        self.angle_threshold = 85
        self.put_down = 65

    def calculate_shoulder_elbow_hip_angle(self, shoulder, elbow, hip):
        """Calculate the angle between shoulder, elbow, and hip."""
        return calculate_angle(elbow, shoulder, hip)

    def track_bench(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
        # Right arm landmarks (shoulder, elbow, hip, wrist)
            shoulder_right = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
            elbow_right = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
            hip_right = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
            wrist_right = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

            # Left arm landmarks (shoulder, elbow, hip, wrist)
            shoulder_left = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
            elbow_left = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
            hip_left = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
            wrist_left = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]
            # Calculate the angle for counting (elbow flexion angle)
            angle_right = self.calculate_shoulder_elbow_hip_angle(shoulder_right, elbow_right, hip_right)
            angle_left = self.calculate_shoulder_elbow_hip_angle(shoulder_left, elbow_left, hip_left)

            cv2.putText(frame, f'Right Angle: {int(angle_right)}', (elbow_right[0] + 10, elbow_right[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Left Angle: {int(angle_left)}', (elbow_left[0] + 10, elbow_left[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if abs(angle_right) > self.angle_threshold:
                warning_message_right = f"Right Shoulder-Elbow-Hip Misalignment! Angle: {angle_right:.2f}°"
                cv2.putText(frame, warning_message_right, (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if abs(angle_left) > self.angle_threshold:
                warning_message_left = f"Left Shoulder-Elbow-Hip Misalignment! Angle: {angle_left:.2f}°"
                cv2.putText(frame, warning_message_left, (10, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            angle_wrist_arm_shoulder = self.calculate_shoulder_elbow_hip_angle(elbow_right, shoulder_right, wrist_right)
            cv2.putText(frame, f'arm_angle: {int(angle_wrist_arm_shoulder)}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            count = self.counter.counter(angle_wrist_arm_shoulder)
            cv2.putText(frame, f'counter: {int(count)}', (10, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    # def run(self):
    #     while self.cap.isOpened():
    #         ret, frame = self.cap.read()
    #         if not ret:
    #             break
    #
    #         frame = cv2.flip(frame, 1)
    #         output = self.track_bench(frame)
    #
    #         cv2.imshow('Bench Press Tracker', output)
    #         if cv2.waitKey(5) & 0xFF == 27:  # ESC to exit
    #             break
    #
    #     self.cap.release()
    #     cv2.destroyAllWindows()
