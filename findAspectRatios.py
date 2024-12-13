#!/usr/bin/env python3
from mackee import main, get_cms
from threading import Lock
from csv import Error as CSVError
from mackee import main, get_args
from brightcove.utils import list_to_csv, eprint
from brightcove.utils import SimpleProgressDisplay, SimpleTimer
import csv
from mackee import main, get_cms
from brightcove.utils import aspect_ratio, eprint
#=============================================
# callback to find the aspect ratio of videos
#=============================================
data_lock = Lock()
show_progress = SimpleProgressDisplay(steps=100, add_info='videos processed')
row_list=[('Video ID', 'Aspect Ratio X', 'Aspect Ratio Y')]

def find_aspect_ratios(video: dict) -> None:
    """
    This will print out the aspectratio of a video.
    """
    video_id = video.get('id')
    delivery_type = video.get('delivery_type')
    source_w, source_h, response = None, None, None

    if delivery_type == 'static_origin':
        response = get_cms().GetRenditionList(video_id=video_id)
    elif delivery_type == 'dynamic_origin':
        response = get_cms().GetDynamicRenditions(video_id=video_id)
    else:
        print(f'No video dimensions found for video ID {video_id} (delivery type: {delivery_type}).')
        return

    if response.status_code in get_cms().success_responses:
        renditions = response.json()
        print(renditions)
        for rendition in renditions:
            if rendition.get('media_type') == 'video' or rendition.get('audio_only') == False:
                source_w = rendition.get('frame_width')
                source_h = rendition.get('frame_height')
                break

        if source_h and source_w:
            x, y = aspect_ratio(source_w, source_h)
            row=[video_id,x,y]
            with data_lock:
                row_list.append(row)
                show_progress()
        else:
           print(f'No video renditions found for video ID {video_id}.')

    else:
        print(f'Could not get renditions for video ID {video_id}.')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    with SimpleTimer():
        # generate the report
        main(find_aspect_ratios)
        show_progress(force_display=True)
        try:
            list_to_csv(row_list,'report_aspectRatio.csv')
        except (OSError, CSVError) as e:
            eprint(f'\n{e}')

        
