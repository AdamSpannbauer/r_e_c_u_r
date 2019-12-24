#!/bin/sh
echo "# Auto-generated Actions list"
echo
echo `date`
echo
echo "for branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')"
echo

echo "# Methods"
grep " def " actions.py | grep -v "^#" | sed -e 's/ def //' | sed -e 's/self//' | sed -e 's/(, /(/' | sed -e 's/()//' | sed -e 's/\(.*\)/  *\1/' | sed -e 's/://' | sort -n \
	| grep -v "check_if_should_start_openframeworks\|create_serial_port_process\|__init__\|persist_composite_setting\|receive_detour_info\|_refresh_frame_buffer\|refresh_frame_buffer_and_restart_openframeworks\|run_script\|setup_osc_server\|start_confirm_action\|stop_serial_port_process\|stop_openframeworks_process\|update_capture_settings\|update_config_settings\|update_video_settings"
echo 

echo "----"
echo
echo "Autogenerated by dotfiles/generate-list-actions.sh"

