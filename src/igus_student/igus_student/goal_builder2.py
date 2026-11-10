from pymoveit2 import connect
from scipy.spatial.transform import Rotation
from .constants import END_EFFECTOR_LINK, PLANNING_GROUP, REFERENCE_FRAME
from math import pi


def main() -> int:
    with connect(group_name=PLANNING_GROUP, timeout_sec=30.0) as robot:
        robot.arm.pipeline_id = 'ompl' # PTP
        robot.arm.planner_id = 'RRTConnectkConfigDefault' # pilz_industrial_motion_planner
        robot.arm.max_velocity = 0.1
        robot.arm.max_acceleration = 0.1
        robot.arm.allowed_planning_time = 5.0
        roll = pi
        pitch = 0.0
        yaw = 0.0
        quat = Rotation.from_euler("xyz", [roll, pitch, yaw]).as_quat()
        trajectory = robot.arm.plan(
            position=(0.2, 0.0, 0.25),
            quat_xyzw=quat,
            frame_id=REFERENCE_FRAME,
            target_link=END_EFFECTOR_LINK,
            timeout_sec=60.0,
        )
        
        
        if trajectory is None:
            robot.node.get_logger().error('Planning failed; trajectory was not executed')
            return 1

        robot.node.get_logger().info(
            f'Plan succeeded with {len(trajectory.points)} points; not executing'
        )

        if not robot.arm.execute(trajectory):
            robot.node.get_logger().error(
                f'Execution was not accepted: {robot.last_failure()}'
            )
            return 1

        if not robot.arm.wait_until_executed(
            timeout_sec=60.0,
            cancel_on_timeout=True,
        ):
            robot.node.get_logger().error(
                f'Execution failed: {robot.last_failure()}'
            )
            return 1

        robot.node.get_logger().info('Execution succeeded')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
