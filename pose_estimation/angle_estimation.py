import numpy as np
def calculate_angle(a, b, c):
    a = np.array(a)  # shoulder
    b = np.array(b)  # elbow
    c = np.array(c)  # wrist

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    return angle