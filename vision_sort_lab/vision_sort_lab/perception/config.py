"""Parametri della ricostruzione RGB-D."""

# Topic ROS e riferimento delle misure.
IMAGE = "/sort_camera/image_raw"
DEPTH = "/sort_camera/depth_image"
CAMERA_INFO = "/sort_camera/camera_info"
WORLD = "world"

# Campionamento della profondità.
PATCH_RADIUS = 3
MIN_DEPTH_SAMPLES = 9
MAX_DEPTH_SPREAD = 0.005

# Selezione e stima del piano superiore.
FACE_RANSAC_TRIALS = 200
FACE_PLANE_TOLERANCE = 0.0003
MIN_FACE_POINTS = 100
MIN_FACE_FRACTION = 0.35
MAX_FACE_TILT_DEG = 15.0

# Ricerca del piano d'appoggio.
SUPPORT_GAP_PX = 3
SUPPORT_OUTER_PX = 24
SUPPORT_MIN_SECTOR_POINTS = 20
SUPPORT_MIN_SECTORS = 3
SUPPORT_MAX_ANGLE_DEG = 5.0

# Verifica del bordo inferiore.
MIN_CONTACT_SAMPLES = 20
MAX_CONTACT_P10_GAP = 0.003

# Distinzione fra facce rettangolari e quasi quadrate.
SQUARE_REL_TOL = 0.05