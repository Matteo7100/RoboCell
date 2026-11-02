from moveit_msgs.msg import MoveItErrorCodes

def describe_moveit_error(code):
    names = {
            MoveItErrorCodes.SUCCESS: "SUCCESS", 
            MoveItErrorCodes.FAILURE : "FAILURE", 
            MoveItErrorCodes.PLANNING_FAILED : "PLANNING_FAILED", 
            MoveItErrorCodes.INVALID_GROUP_NAME : "INVALID_GROUP_NAME", 
            MoveItErrorCodes.INVALID_GOAL_CONSTRAINTS : "INVALID_GOAL_CONSTRAINTS", 
            MoveItErrorCodes.TIMED_OUT : "TIMED_OUT",

            MoveItErrorCodes.CONTROL_FAILED: "CONTROL_FAILED"
    }
    return names.get(code, "UNKNOWN")