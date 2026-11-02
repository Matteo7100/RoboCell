from copy import deepcopy
from geometry_msgs.msg import Pose
from moveit_msgs.msg import (
    Constraints,
    PositionConstraint,
    OrientationConstraint,
)
from moveit_msgs.srv import GetMotionPlan
from shape_msgs.msg import SolidPrimitive


def build_plan_request(target_positions):
    # Crea un nuovo messaggio di richiesta del servizio GetMotionPlan.
    # I suoi campi vengono inizializzati con i valori predefiniti.
    request = GetMotionPlan.Request()

    # Recupera il messaggio interno che descrive la pianificazione.
    # Non crea una copia: modificare plan modifica questa parte di request.
    plan = request.motion_plan_request

    # Sceglie il gruppo di giunti da pianificare.
    plan.group_name = "panda_arm"
    # plan.group_name = "gruppo_inesistente_test"  # SOLO TEST

    # Imposta il numero di tentativi e il tempo disponibile per pianificare.
    plan.num_planning_attempts = 1
    plan.allowed_planning_time = 5.0

    # Riduce al 20% i limiti di velocità e accelerazione della traiettoria.
    plan.max_velocity_scaling_factor = 0.2
    plan.max_acceleration_scaling_factor = 0.2

    # Interpreta start_state come aggiornamento parziale.
    # Lasciando vuote le posizioni, usiamo lo stato corrente noto a MoveIt.
    plan.start_state.is_diff = True

    plan.goal_constraints = [
        build_goal_constraints(target_positions)
    ]
    # Restituisce la richiesta completa, ancora da inviare.
    return request
#----------------------------------------------#
def build_goal_constraints(target_positions):
    goal = Constraints()
    goal.name = "joint_goal"

    for joint_name, position in target_positions.items(): 
        constraint = JointConstraint()
        constraint.joint_name = joint_name
        constraint.position = position
        constraint.tolerance_above = 0.01
        constraint.tolerance_below = 0.01
        constraint.weight = 1.0
        goal.joint_constraints.append(constraint)

    return goal
#----------------------------------------------#
def build_pose_goal_constraints(target, link_name):
    # Costruisci i due vincoli mostrati sopra.
    # Inseriscili nello stesso Constraints e restituiscilo.
    goal = Constraints()
    goal.name = 'pose_goal'

    # --- POSITION CONSTRAINT ---#
    position_constraint = PositionConstraint()
    position_constraint.header.frame_id = target.header.frame_id
    position_constraint.link_name = link_name
    position_constraint.weight = 1.0

    sphere = SolidPrimitive()
    sphere.type = SolidPrimitive.SPHERE
    sphere.dimensions = [0.005]

    region_pose = Pose()
    region_pose.position = deepcopy(target.pose.position)
    region_pose.orientation.w = 1.0

    position_constraint.constraint_region.primitives = [sphere]
    position_constraint.constraint_region.primitive_poses = [region_pose]

    goal.position_constraints = [position_constraint]

    # --- ORIENTATION CONSTRAINT ---#
    orientation_constraint = OrientationConstraint()
    orientation_constraint.header.frame_id = target.header.frame_id
    orientation_constraint.link_name = link_name
    orientation_constraint.orientation = deepcopy(target.pose.orientation)

    orientation_constraint.parameterization = OrientationConstraint.ROTATION_VECTOR
    orientation_constraint.absolute_x_axis_tolerance = 0.05
    orientation_constraint.absolute_y_axis_tolerance = 0.05
    orientation_constraint.absolute_z_axis_tolerance = 0.05
    orientation_constraint.weight = 1.0

    goal.orientation_constraints = [orientation_constraint]

    return goal
    
#----------------------------------------------#
def build_pose_plan_request(target, link_name):
    # Costruisci GetMotionPlan.Request e restituiscila.
    request = GetMotionPlan.Request()

    plan = request.motion_plan_request

    plan.group_name = "panda_arm"

    plan.num_planning_attempts = 1
    plan.allowed_planning_time = 5.0

    plan.max_velocity_scaling_factor = 0.2
    plan.max_acceleration_scaling_factor = 0.2
 
    plan.start_state.is_diff = True

    plan.goal_constraints = [
    build_pose_goal_constraints(target, link_name)
    ]
    return request