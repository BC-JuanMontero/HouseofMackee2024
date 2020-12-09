#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# function to get size of master
#===========================================
def get_master_storage(video):
	master_size = 0
	if video.get('has_digital_master'):
		shared = video.get('sharing')
		if shared and shared.get('by_external_acct'):
			return 0
		response = get_cms().GetDigitalMasterInfo(video_id=video.get('id'))
		if response.status_code == 200:
			master_size = response.json().get('size')

	return master_size

#===========================================
# function to get size of all renditions
#===========================================
def get_rendition_sizes(video):
	ren_size = 0

	response = get_cms().GetDynamicRenditions(video_id=video.get('id'))
	if response.status_code in get_cms().success_responses:
		renditions = response.json()
		for rendition in renditions:
			ren_size += rendition.get('size')

	return ren_size

#===========================================
# callback getting storage sizes
#===========================================
def find_storage_size(video):
	total_size = get_master_storage(video) + get_rendition_sizes(video)
	print(f'{video.get("id")}, {total_size}')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_storage_size)
