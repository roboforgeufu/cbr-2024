from pybricks.parameters import Button

from core.omni_robot import OmniRobot


def open_claw(robot: OmniRobot):
    robot.motor_claw_gripper.run_target(300, target_angle=robot.claw_open_angle)


def close_claw(robot: OmniRobot):

    direction_sign = (
        -1 if robot.motor_claw_gripper.angle() - robot.claw_closed_angle > 0 else 1
    )

    while (
        abs(robot.motor_claw_gripper.angle() - robot.claw_closed_angle) > 10
        and not robot.motor_claw_gripper.stalled()
    ):
        robot.motor_claw_gripper.run(300 * direction_sign)
    robot.motor_claw_gripper.hold()


def raise_claw(robot: OmniRobot):
    robot.motor_claw_lift.run_target(200, target_angle=robot.claw_high_angle)


def lower_claw(robot: OmniRobot):
    robot.motor_claw_lift.run_target(200, target_angle=robot.claw_low_angle)


def mid_claw(robot: OmniRobot):
    robot.motor_claw_lift.run_target(200, target_angle=robot.claw_mid_angle)


def transmit_signal(robot: OmniRobot, signal_function):
    robot.ev3_print("Transmitindo:")
    robot.bluetooth.message(signal_function(), force_send=True)
    while robot.bluetooth.message(should_wait=False) != "STOP":
        robot.bluetooth.message(signal_function(), delay=10, force_send=True)
    robot.ev3_print("Transmissao encerrada")
