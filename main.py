import sys
import threading

import pynput
from PyQt5.QtWidgets import QApplication

import apex_yolov5_main
import apex_yolov5_main_asyn
from apex_recoils.core import SelectGun, ReaSnowSelectGun, GameWindowsStatus
from apex_recoils.core.image_comparator.NetImageComparator import NetImageComparator
from apex_recoils.core.screentaker.LocalMssScreenTaker import LocalMssScreenTaker
from apex_yolov5 import check_run, auxiliary
from apex_yolov5.KeyAndMouseListener import apex_mouse_listener, apex_key_listener
from apex_yolov5.RecoildsCore import RecoilsConfig, RecoilsListener
from apex_yolov5.job_listener import JoyListener
from apex_yolov5.job_listener.JoyToKey import JoyToKey
from apex_yolov5.log import LogFactory
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.mouse_mover.Win32ApiMover import Win32ApiMover
from apex_yolov5.socket.config import global_config
from apex_yolov5.windows.DisclaimerWindow import DisclaimerWindow
from apex_yolov5.windows.aim_show_window import get_aim_show_window
from apex_yolov5.windows.circle_window import get_circle_window
from apex_yolov5.windows.config_window import ConfigWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    LogFactory.init_logger()
    JoyListener.joy_listener = JoyListener.JoyListener(logger=LogFactory.logger())
    log_window = ConfigWindow(global_config)
    dis = DisclaimerWindow(log_window)
    check_run.check(validate_type='ai', main_windows=log_window)

    GameWindowsStatus.init(logger=LogFactory.logger())
    MoverFactory.init_mover(
        mouse_model=global_config.mouse_model,
        mouse_mover_params=global_config.available_mouse_models)
    SelectGun.select_gun = SelectGun.SelectGun(logger=LogFactory.logger(),
                                               bbox=global_config.select_gun_bbox,
                                               image_path=global_config.image_path,
                                               scope_bbox=global_config.select_scope_bbox,
                                               scope_path=global_config.scope_path,
                                               refresh_buttons=global_config.refresh_button,
                                               has_turbocharger=global_config.has_turbocharger,
                                               hop_up_bbox=global_config.select_hop_up_bbox,
                                               hop_up_path=global_config.hop_up_path,
                                               image_comparator=NetImageComparator(LogFactory.logger(),
                                                                                   global_config.image_base_path),
                                               screen_taker=LocalMssScreenTaker(LogFactory.logger()),
                                               game_windows_status=GameWindowsStatus.get_game_status())

    if global_config.rea_snow_gun_config_name != "" or global_config.joy_move:
        rea_snow_select_gun = ReaSnowSelectGun.ReaSnowSelectGun(logger=LogFactory.logger(),
                                                                config_name=global_config.rea_snow_gun_config_name)
        SelectGun.get_select_gun().connect(rea_snow_select_gun.trigger_button)

        jtk = JoyToKey(logger=LogFactory.logger(), joy_to_key_map=global_config.joy_to_key_map,
                       c1_mouse_mover=Win32ApiMover(LogFactory.logger(), {}))
        JoyListener.joy_listener.connect_axis(jtk.axis_to_key)
        JoyListener.joy_listener.start(None)
    else:
        # 压枪
        recoils_listener = RecoilsListener(logger=LogFactory.logger(),
                                           mouse_listener=apex_mouse_listener,
                                           select_gun=SelectGun.select_gun, config=global_config)
        recoils_listener.start()

    SelectGun.get_select_gun().test()
    if global_config.mouse_model != 'km_box_net':
        listener = pynput.mouse.Listener(
            on_click=apex_mouse_listener.on_click, on_move=apex_mouse_listener.on_move)
        listener.start()

    key_listener = pynput.keyboard.Listener(
        on_press=apex_key_listener.on_press, on_release=apex_key_listener.on_release
    )
    key_listener.start()

    threading.Thread(target=auxiliary.start).start()

    if global_config.show_config:
        log_window.show()

    if global_config.show_circle:
        get_circle_window().show()

    if global_config.show_aim:
        get_aim_show_window().show()

    if global_config.joy_move:
        JoyListener.joy_listener.start(log_window)

    if global_config.screenshot_frequency_mode == "asyn":
        threading.Thread(target=apex_yolov5_main_asyn.main).start()
        threading.Thread(target=apex_yolov5_main_asyn.handle, args=(log_window,)).start()
    else:
        threading.Thread(target=apex_yolov5_main.main, args=(log_window,)).start()

    # KMCallBack.connect(KMCallBack('k', 'p', save_screen_to_file))
    sys.exit(app.exec_())
