from apex_yolov5.log.Logger import Logger


class JoyToKey:
    """
        jtk
    """

    def __init__(self, logger: Logger, joy_to_key_map, c1_mouse_mover):
        self.logger = logger
        self.c1_mouse_mover = c1_mouse_mover
        self.joy_to_key_map = joy_to_key_map
        self.joy_to_key_last_status_map = {}
        self.init_status_map()

    def init_status_map(self):
        """
            初始化状态
        """
        for joy_to_key in self.joy_to_key_map:
            for joy in self.joy_to_key_map[joy_to_key]:
                self.joy_to_key_last_status_map[joy_to_key + joy] = False

    def axis_to_key(self, axis, value):
        """

        :param axis:
        :param value:
        """
        if "axis" not in self.joy_to_key_map:
            return
        axis = str(axis)
        axis_joy_to_key_map = self.joy_to_key_map["axis"]

        hold_status = value > -1.0
        key = "axis" + axis
        if key not in self.joy_to_key_last_status_map:
            return

        toggle_key_status = self.joy_to_key_last_status_map[key]
        joy_to_key = axis_joy_to_key_map[axis]

        if not toggle_key_status and hold_status:
            self.logger.print_log(f"joy to key [{joy_to_key['key_type']}.{joy_to_key['key']}] down")
            if joy_to_key['key_type'] == "mouse":
                self.c1_mouse_mover.mouse_click(joy_to_key['key'], True)
        if toggle_key_status and not hold_status:
            self.logger.print_log(f"joy to key [{joy_to_key['key_type']}.{joy_to_key['key']}] up")
            if joy_to_key['key_type'] == "mouse":
                self.c1_mouse_mover.mouse_click(joy_to_key['key'], False)

        self.joy_to_key_last_status_map[key] = hold_status
