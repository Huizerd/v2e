#!/usr/bin/env bash

# clean slomo 1ms
python v2e.py \
    -i input/lava \
    --overwrite \
    --timestamp_resolution 0.001 \
    --auto_timestamp_resolution true \
    --dvs_exposure source \
    --output_folder output/lava_slomo_clean_1ms \
    --dvs_params clean \
    --dvs_h5 lava.h5 \
    --dvs_aedat4 lava.aedat4 \
    --dvs_vid lava.avi \
    --no_preview \
    --output_height 180 \
    --output_width 180 \
    --input_frame_rate 20 \
    --avi_frame_rate 20

# noisy slomo 1ms
python v2e.py \
    -i input/lava \
    --overwrite \
    --timestamp_resolution 0.001 \
    --auto_timestamp_resolution true \
    --dvs_exposure source \
    --output_folder output/lava_slomo_noisy_1ms \
    --dvs_params noisy \
    --dvs_h5 lava.h5 \
    --dvs_aedat4 lava.aedat4 \
    --dvs_vid lava.avi \
    --no_preview \
    --output_height 180 \
    --output_width 180 \
    --input_frame_rate 20 \
    --avi_frame_rate 20
