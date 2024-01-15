#!/usr/bin/env bash

# go over all materials and motions
materials=(aerial_rocks brick carpet fabric grass lava lego water stripes)
motions=(x-slow x-medium x-fast y-slow y-medium y-fast z-slow z-medium z-fast nx-slow nx-medium nx-fast ny-slow ny-medium ny-fast r-slow r-medium r-fast nr-slow nr-medium nr-fast random-bezier)
for material in ${materials[@]}; do
    for motion in ${motions[@]}; do
        echo "Processing $material with $motion"

        # generate events
        # noisy slomo 1ms, noisy looks better than clean
        # TODO: getting error about timestamp/cutoff freq, but lowering to 0.0001 is very slow
        python v2e.py \
            -i ../BlenderProc/event_planar/output/$material/$motion/images \
            --overwrite \
            --timestamp_resolution 0.001 \
            --auto_timestamp_resolution true \
            --dvs_exposure source \
            --output_folder output/$material/$motion \
            --dvs_params noisy \
            --dvs_h5 events.h5 \
            --no_preview \
            --output_height 180 \
            --output_width 180 \
            --input_frame_rate 20
        
        # render video
        python render_video.py \
            ../BlenderProc/event_planar/output/$material/$motion/images \
            output/$material/$motion/events.h5
        
        # convert h5
        python convert_h5.py \
            output/$material/$motion/events.h5 \
            ../BlenderProc/event_planar/output/$material/$motion/hdf5 \
            output/compatible_h5

    done
done
